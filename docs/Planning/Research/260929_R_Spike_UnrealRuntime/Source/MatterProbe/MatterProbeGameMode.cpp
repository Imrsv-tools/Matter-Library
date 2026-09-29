#include "MatterProbeGameMode.h"

#include "Components/DirectionalLightComponent.h"
#include "Components/SceneCaptureComponent2D.h"
#include "Components/SkyLightComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/DirectionalLight.h"
#include "Engine/SceneCapture2D.h"
#include "Engine/SkyLight.h"
#include "Engine/StaticMesh.h"
#include "Engine/StaticMeshActor.h"
#include "Engine/TextureCube.h"
#include "Engine/TextureRenderTarget2D.h"
#include "HAL/FileManager.h"
#include "ImageCore.h"
#include "ImageUtils.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "MaterialShared.h"
#include "RHIGlobals.h"
#include "Misc/CommandLine.h"
#include "Misc/FileHelper.h"
#include "Misc/Parse.h"
#include "Misc/Paths.h"
#include "RenderingThread.h"
#include "ShaderCompiler.h"
#include "TextureResource.h"

DEFINE_LOG_CATEGORY_STATIC(LogMatterProbe, Log, All);

AMatterProbeGameMode::AMatterProbeGameMode()
{
	PrimaryActorTick.bCanEverTick = true;
	PrimaryActorTick.bStartWithTickEnabled = true;
	DefaultPawnClass = nullptr;
}

void AMatterProbeGameMode::StartPlay()
{
	Super::StartPlay();
	const TCHAR* Cmd = FCommandLine::Get();
	FParse::Value(Cmd, TEXT("MatterOut="), OutPath);
	FParse::Value(Cmd, TEXT("MatterMaster="), MasterPath);
	FParse::Value(Cmd, TEXT("MatterWidth="), Width);
	FParse::Value(Cmd, TEXT("MatterSettle="), SettleFrames);
	if (OutPath.IsEmpty())
	{
		OutPath = FPaths::ProjectSavedDir() / TEXT("MatterProbe/capture.pfm");
	}
	BuildScene();
}

void AMatterProbeGameMode::BuildScene()
{
	UWorld* World = GetWorld();
	const TCHAR* Cmd = FCommandLine::Get();

	UMaterialInterface* Master = LoadObject<UMaterialInterface>(nullptr, *MasterPath);
	UStaticMesh* Sphere = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Sphere.Sphere"));
	UE_LOG(LogMatterProbe, Display, TEXT("MATTERPROBE master=%s loaded=%d sphere=%d"), *MasterPath, Master != nullptr, Sphere != nullptr);

	if (Master)
	{
		Mid = UMaterialInstanceDynamic::Create(Master, this);
#if WITH_EDITOR
		// Editor-hosted: the master's shaders may still be loading or compiling; block until done.
		if (FMaterialResource* Res = Master->GetMaterialResource(GMaxRHIShaderPlatform))
		{
			Res->FinishCompilation();
			UE_LOG(LogMatterProbe, Display, TEXT("MATTERPROBE finished master compilation"));
		}
#endif
		FString Color;
		if (FParse::Value(Cmd, TEXT("MatterColor="), Color))
		{
			TArray<FString> Parts;
			Color.ParseIntoArray(Parts, TEXT(","));
			if (Parts.Num() == 3)
			{
				Mid->SetVectorParameterValue(TEXT("base_color"),
					FLinearColor(FCString::Atof(*Parts[0]), FCString::Atof(*Parts[1]), FCString::Atof(*Parts[2])));
			}
		}
		float Rough = 0.f;
		if (FParse::Value(Cmd, TEXT("MatterRough="), Rough))
		{
			Mid->SetScalarParameterValue(TEXT("specular_roughness"), Rough);
		}
	}

	// Sphere: engine basic shape, 100 cm diameter, at the origin.
	AStaticMeshActor* SphereActor = World->SpawnActor<AStaticMeshActor>(FVector::ZeroVector, FRotator::ZeroRotator);
	UStaticMeshComponent* SM = SphereActor->GetStaticMeshComponent();
	SphereComp = SM;
	SM->SetMobility(EComponentMobility::Movable);
	SM->SetStaticMesh(Sphere);
	SM->SetCastShadow(false);
	if (Mid)
	{
		SM->SetMaterial(0, Mid);
	}

	// Sun: 1.5 (irradiance), no shadows, rotated like the rig's sun.
	ADirectionalLight* Sun = World->SpawnActor<ADirectionalLight>(FVector::ZeroVector, FRotator(-40.f, 35.f, 0.f));
	UDirectionalLightComponent* SunComp = Cast<UDirectionalLightComponent>(Sun->GetLightComponent());
	SunComp->SetMobility(EComponentMobility::Movable);
	SunComp->SetIntensity(1.5f);
	SunComp->SetCastShadows(false);
	SunComp->SetLightSourceAngle(0.53f);

	// Sky: a constant dome from a cubemap built by the commandlet.
	UTextureCube* Dome = LoadObject<UTextureCube>(nullptr, TEXT("/Game/Env/T_Dome.T_Dome"));
	UE_LOG(LogMatterProbe, Display, TEXT("MATTERPROBE dome loaded=%d"), Dome != nullptr);
	ASkyLight* Sky = World->SpawnActor<ASkyLight>(FVector::ZeroVector, FRotator::ZeroRotator);
	USkyLightComponent* SkyComp = Sky->GetLightComponent();
	SkyComp->SetMobility(EComponentMobility::Movable);
	SkyComp->SourceType = ESkyLightSourceType::SLS_SpecifiedCubemap;
	SkyComp->SetCubemap(Dome);
	SkyComp->SetIntensity(1.f);
	SkyComp->bLowerHemisphereIsBlack = false;
	SkyComp->SetCastShadows(false);
	SkyComp->RecaptureSky();

	// Capture: linear scene colour (before the tonemapper), float target, fixed exposure 1.
	Target = NewObject<UTextureRenderTarget2D>(this);
	Target->ClearColor = FLinearColor::Black;
	Target->InitCustomFormat(Width, Width, PF_A32B32G32R32F, true);
	Target->UpdateResourceImmediate(true);

	const float FOV = FMath::RadiansToDegrees(2.f * FMath::Atan(18.f / 50.f)); // 50 mm lens, 36 mm aperture
	ASceneCapture2D* Cam = World->SpawnActor<ASceneCapture2D>(FVector(-190.f, 0.f, 0.f), FRotator::ZeroRotator);
	CaptureComp = Cam->GetCaptureComponent2D();
	CaptureComp->SetMobility(EComponentMobility::Movable);
	CaptureComp->FOVAngle = FOV;
	CaptureComp->TextureTarget = Target;
	CaptureComp->CaptureSource = ESceneCaptureSource::SCS_SceneColorHDR;
	CaptureComp->bCaptureEveryFrame = false;
	CaptureComp->bCaptureOnMovement = false;
	CaptureComp->bAlwaysPersistRenderingState = true;
	CaptureComp->PostProcessSettings.bOverride_AutoExposureMethod = true;
	CaptureComp->PostProcessSettings.AutoExposureMethod = EAutoExposureMethod::AEM_Manual;
	CaptureComp->PostProcessSettings.bOverride_AutoExposureBias = true;
	CaptureComp->PostProcessSettings.AutoExposureBias = 0.f;
	CaptureComp->PostProcessSettings.bOverride_AutoExposureApplyPhysicalCameraExposure = true;
	CaptureComp->PostProcessSettings.AutoExposureApplyPhysicalCameraExposure = false;
	CaptureComp->PostProcessBlendWeight = 1.f;
}

void AMatterProbeGameMode::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	if (bDone)
	{
		return;
	}
	++Frames;
	// Ready = no shader jobs pending, the master's shader map complete, the sphere's PSOs precached,
	// and all three still true for SettleFrames frames in a row (a captured default material is the trap).
	const int32 Remaining = GShaderCompilingManager ? GShaderCompilingManager->GetNumRemainingJobs() : 0;
	const FMaterialResource* Resource = Mid ? Mid->GetMaterialResource(GMaxRHIShaderPlatform) : nullptr;
	const bool bShaderMap = Resource && Resource->IsGameThreadShaderMapComplete();
	const bool bPSO = SphereComp && !SphereComp->IsPSOPrecaching();
	const bool bReady = Remaining == 0 && bPSO; // shadermap is logged only: it read 0 even once the master rendered (probe 2)
	ReadyFrames = bReady ? ReadyFrames + 1 : 0;
	if (Frames % 300 == 0)
	{
		UE_LOG(LogMatterProbe, Display, TEXT("MATTERPROBE frame=%d shaderjobs=%d shadermap=%d pso=%d ready=%d"), Frames, Remaining, int32(bShaderMap), int32(bPSO), ReadyFrames);
	}
	if (ReadyFrames < SettleFrames && Frames < 20000)
	{
		return;
	}
	UE_LOG(LogMatterProbe, Display, TEXT("MATTERPROBE capture at frame=%d ready=%d (timeout=%d)"), Frames, ReadyFrames, int32(ReadyFrames < SettleFrames));
	bDone = true;
	const bool bOk = CaptureAndWrite();
	FPlatformMisc::RequestExitWithStatus(false, bOk ? 0 : 1);
}

bool AMatterProbeGameMode::CaptureAndWrite()
{
	CaptureComp->CaptureScene();
	FlushRenderingCommands();

	FTextureRenderTargetResource* Res = Target->GameThread_GetRenderTargetResource();
	TArray<FLinearColor> Px;
	if (!Res || !Res->ReadLinearColorPixels(Px, FReadSurfaceDataFlags(RCM_MinMax)) || Px.Num() != Width * Width)
	{
		UE_LOG(LogMatterProbe, Error, TEXT("MATTERPROBE readback failed"));
		return false;
	}

	// Portable float map (PFM): a text header, then bottom-to-top rows of little-endian float RGB.
	TArray<uint8> Bytes;
	const FString Header = FString::Printf(TEXT("PF\n%d %d\n-1.0\n"), Width, Width);
	const FTCHARToUTF8 H(*Header);
	Bytes.Append(reinterpret_cast<const uint8*>(H.Get()), H.Length());
	double Sum = 0.0;
	for (int32 Y = Width - 1; Y >= 0; --Y)
	{
		for (int32 X = 0; X < Width; ++X)
		{
			const FLinearColor& C = Px[Y * Width + X];
			const float RGB[3] = { C.R, C.G, C.B };
			Bytes.Append(reinterpret_cast<const uint8*>(RGB), sizeof(RGB));
			Sum += (C.R + C.G + C.B) / 3.0;
		}
	}
	IFileManager::Get().MakeDirectory(*FPaths::GetPath(OutPath), true);
	const bool bOk = FFileHelper::SaveArrayToFile(Bytes, *OutPath);
	UE_LOG(LogMatterProbe, Display, TEXT("MATTERPROBE wrote=%d path=%s frames=%d mean=%.6f centre=%s"),
		bOk, *OutPath, Frames, Sum / Px.Num(), *Px[(Width / 2) * Width + Width / 2].ToString());
	return bOk;
}
