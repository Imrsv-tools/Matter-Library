#include "MatterRuntimeGameMode.h"

#include "Components/DirectionalLightComponent.h"
#include "Components/SceneCaptureComponent2D.h"
#include "Components/SkyLightComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Dom/JsonObject.h"
#include "Engine/DirectionalLight.h"
#include "Engine/SceneCapture2D.h"
#include "Engine/SkyLight.h"
#include "Engine/StaticMesh.h"
#include "Engine/StaticMeshActor.h"
#include "Engine/Texture2D.h"
#include "Engine/TextureRenderTarget2D.h"
#include "HAL/FileManager.h"
#include "ImageUtils.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "MaterialShared.h"
#include "Misc/CommandLine.h"
#include "Misc/FileHelper.h"
#include "Misc/Parse.h"
#include "Misc/Paths.h"
#include "ProceduralMeshComponent.h"
#include "RenderingThread.h"
#include "RHIGlobals.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"
#include "ShaderCompiler.h"
#include "TextureResource.h"

DEFINE_LOG_CATEGORY_STATIC(LogMatter, Log, All);

namespace
{
	FVector Vec(const TSharedPtr<FJsonObject>& Obj, const FString& Key, const FVector& Default = FVector::ZeroVector)
	{
		const TArray<TSharedPtr<FJsonValue>>* A = nullptr;
		if (!Obj->TryGetArrayField(Key, A) || A->Num() < 3)
		{
			return Default;
		}
		return FVector((*A)[0]->AsNumber(), (*A)[1]->AsNumber(), (*A)[2]->AsNumber());
	}

	FLinearColor Colour(const TArray<TSharedPtr<FJsonValue>>& A)
	{
		const double R = A.Num() > 0 ? A[0]->AsNumber() : 0.0;
		const double G = A.Num() > 1 ? A[1]->AsNumber() : R;
		const double B = A.Num() > 2 ? A[2]->AsNumber() : R;
		const double W = A.Num() > 3 ? A[3]->AsNumber() : 1.0;
		return FLinearColor(R, G, B, W);
	}
}

AMatterRuntimeGameMode::AMatterRuntimeGameMode()
{
	PrimaryActorTick.bCanEverTick = true;
	PrimaryActorTick.bStartWithTickEnabled = true;
	DefaultPawnClass = nullptr;
}

void AMatterRuntimeGameMode::StartPlay()
{
	Super::StartPlay();
	FString JobPath;
	if (!FParse::Value(FCommandLine::Get(), TEXT("MatterJob="), JobPath))
	{
		UE_LOG(LogMatter, Error, TEXT("MATTER no -MatterJob=<path>"));
		Finish(2);
		return;
	}
	if (!LoadJob(JobPath) || !BuildWorld() || !ApplySetting(0))
	{
		Finish(2);
	}
}

bool AMatterRuntimeGameMode::LoadJob(const FString& Path)
{
	FString Text;
	if (!FFileHelper::LoadFileToString(Text, *Path))
	{
		UE_LOG(LogMatter, Error, TEXT("MATTER cannot read job %s"), *Path);
		return false;
	}
	const TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(Text);
	if (!FJsonSerializer::Deserialize(Reader, Job) || !Job.IsValid())
	{
		UE_LOG(LogMatter, Error, TEXT("MATTER job is not JSON: %s"), *Path);
		return false;
	}
	OutDir = Job->GetStringField(TEXT("out_dir"));
	Width = Job->GetIntegerField(TEXT("width"));
	Job->TryGetNumberField(TEXT("settle_frames"), SettleFrames);
	UE_LOG(LogMatter, Display, TEXT("MATTER job=%s width=%d out=%s"), *Path, Width, *OutDir);
	return true;
}

bool AMatterRuntimeGameMode::BuildWorld()
{
	UWorld* World = GetWorld();

	for (const TSharedPtr<FJsonValue>& M : Job->GetArrayField(TEXT("meshes")))
	{
		if (!LoadMesh(M->AsObject()))
		{
			return false;
		}
	}

	// The sun: a directional light along the job's direction (the way the light travels),
	// its intensity the rig's irradiance times the driver's calibration; never a shadow.
	const TSharedPtr<FJsonObject> Sun = Job->GetObjectField(TEXT("sun"));
	const FVector SunDir = Vec(Sun, TEXT("direction"), FVector(0, 0, -1)).GetSafeNormal();
	ADirectionalLight* SunActor = World->SpawnActor<ADirectionalLight>(FVector::ZeroVector, FRotationMatrix::MakeFromX(SunDir).Rotator());
	SunComp = Cast<UDirectionalLightComponent>(SunActor->GetLightComponent());
	SunComp->SetMobility(EComponentMobility::Movable);
	SunIntensity = Sun->GetNumberField(TEXT("intensity"));
	SunComp->SetIntensity(SunIntensity);
	SunComp->SetLightColor(FLinearColor::White);
	SunComp->SetCastShadows(false);
	SunComp->SetLightSourceAngle(Sun->GetNumberField(TEXT("angle")));

	// The dome: an unlit sphere of constant radiance far outside the set (the visible
	// background), and a sky light that captures it. Nothing nearer than the threshold is
	// captured, so the subjects never light themselves.
	const TSharedPtr<FJsonObject> Sky = Job->GetObjectField(TEXT("sky"));
	UMaterialInterface* SkyMaster = LoadMaster(TEXT("Sky"));
	UStaticMesh* Sphere = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Sphere.Sphere"));
	if (!SkyMaster || !Sphere)
	{
		UE_LOG(LogMatter, Error, TEXT("MATTER sky master=%d sphere=%d"), SkyMaster != nullptr, Sphere != nullptr);
		return false;
	}
	AStaticMeshActor* SkyActor = World->SpawnActor<AStaticMeshActor>(FVector::ZeroVector, FRotator::ZeroRotator);
	SkySphere = SkyActor->GetStaticMeshComponent();
	SkySphere->SetMobility(EComponentMobility::Movable);
	SkySphere->SetStaticMesh(Sphere);
	SkySphere->SetWorldScale3D(FVector(1000.0));      // the basic sphere's radius is 50 cm: 500 m
	SkySphere->SetCastShadow(false);
	UMaterialInstanceDynamic* SkyMid = UMaterialInstanceDynamic::Create(SkyMaster, this);
	const TArray<TSharedPtr<FJsonValue>>* Radiance = nullptr;
	if (Sky->TryGetArrayField(TEXT("radiance"), Radiance))
	{
		SkyMid->SetVectorParameterValue(TEXT("radiance"), Colour(*Radiance));
	}
	SkySphere->SetMaterial(0, SkyMid);
	Mids.Add(SkyMid);

	ASkyLight* SkyActorLight = World->SpawnActor<ASkyLight>(FVector::ZeroVector, FRotator::ZeroRotator);
	SkyComp = SkyActorLight->GetLightComponent();
	SkyComp->SetMobility(EComponentMobility::Movable);
	SkyComp->SourceType = ESkyLightSourceType::SLS_CapturedScene;
	SkyComp->SkyDistanceThreshold = 10000.f;          // 100 m: the set is inside, the sphere outside
	SkyComp->bLowerHemisphereIsBlack = false;
	SkyComp->SetCastShadows(false);
	SkyIntensity = Sky->GetNumberField(TEXT("intensity"));
	SkyComp->SetIntensity(SkyIntensity);

	// The capture: linear scene colour into a float target, exposure fixed, every effect that
	// would add light the rig's other tools do not have turned off.
	Target = NewObject<UTextureRenderTarget2D>(this);
	Target->ClearColor = FLinearColor::Black;
	Target->InitCustomFormat(Width, Width, PF_A32B32G32R32F, true);
	Target->UpdateResourceImmediate(true);

	ASceneCapture2D* Cam = World->SpawnActor<ASceneCapture2D>(FVector::ZeroVector, FRotator::ZeroRotator);
	CaptureComp = Cam->GetCaptureComponent2D();
	CaptureComp->SetMobility(EComponentMobility::Movable);
	CaptureComp->TextureTarget = Target;
	CaptureComp->CaptureSource = ESceneCaptureSource::SCS_SceneColorHDR;
	CaptureComp->bCaptureEveryFrame = false;
	CaptureComp->bCaptureOnMovement = false;
	CaptureComp->bAlwaysPersistRenderingState = true;
	FPostProcessSettings& PP = CaptureComp->PostProcessSettings;
	PP.bOverride_AutoExposureMethod = true;
	PP.AutoExposureMethod = EAutoExposureMethod::AEM_Manual;
	PP.bOverride_AutoExposureBias = true;
	PP.AutoExposureBias = 0.f;
	PP.bOverride_AutoExposureApplyPhysicalCameraExposure = true;
	PP.AutoExposureApplyPhysicalCameraExposure = false;
	PP.bOverride_AmbientOcclusionIntensity = true;
	PP.AmbientOcclusionIntensity = 0.f;
	CaptureComp->PostProcessBlendWeight = 1.f;
	FEngineShowFlags& SF = CaptureComp->ShowFlags;
	SF.SetAmbientOcclusion(false);
	SF.SetScreenSpaceAO(false);
	SF.SetDistanceFieldAO(false);
	SF.SetScreenSpaceReflections(false);
	SF.SetLumenReflections(false);
	SF.SetLumenGlobalIllumination(false);
	SF.SetContactShadows(false);
	SF.SetDynamicShadows(false);
	SF.SetFog(false);
	SF.SetVolumetricFog(false);
	SF.SetAtmosphere(false);
	SF.SetBloom(false);
	SF.SetMotionBlur(false);
	SF.SetEyeAdaptation(false);
	SF.SetTemporalAA(false);
	SF.SetAntiAliasing(false);    // the driver supersamples instead
	return true;
}

bool AMatterRuntimeGameMode::LoadMesh(const TSharedPtr<FJsonObject>& Spec)
{
	// <file>: float32 positions (3N), normals (3N), tangents (3N), uv0 (2N), then int32 indices (M)
	const FString Name = Spec->GetStringField(TEXT("name"));
	const FString File = Spec->GetStringField(TEXT("file"));
	const int32 N = Spec->GetIntegerField(TEXT("verts"));
	const int32 M = Spec->GetIntegerField(TEXT("indices"));
	TArray<uint8> Bytes;
	const int64 Want = int64(N) * 11 * 4 + int64(M) * 4;
	if (!FFileHelper::LoadFileToArray(Bytes, *File) || Bytes.Num() != Want)
	{
		UE_LOG(LogMatter, Error, TEXT("MATTER mesh %s: %s is %d bytes, want %lld"), *Name, *File, Bytes.Num(), Want);
		return false;
	}
	const float* F = reinterpret_cast<const float*>(Bytes.GetData());
	const int32* I = reinterpret_cast<const int32*>(Bytes.GetData() + int64(N) * 11 * 4);
	TArray<FVector> P, Nrm;
	TArray<FProcMeshTangent> T;
	TArray<FVector2D> UV;
	P.SetNumUninitialized(N);
	Nrm.SetNumUninitialized(N);
	T.SetNumUninitialized(N);
	UV.SetNumUninitialized(N);
	for (int32 k = 0; k < N; ++k)
	{
		P[k] = FVector(F[3 * k], F[3 * k + 1], F[3 * k + 2]);
		Nrm[k] = FVector(F[3 * N + 3 * k], F[3 * N + 3 * k + 1], F[3 * N + 3 * k + 2]);
		T[k] = FProcMeshTangent(FVector(F[6 * N + 3 * k], F[6 * N + 3 * k + 1], F[6 * N + 3 * k + 2]), false);
		UV[k] = FVector2D(F[9 * N + 2 * k], F[9 * N + 2 * k + 1]);
	}
	TArray<int32> Tris(I, M);

	AActor* Owner = GetWorld()->SpawnActor<AActor>(FVector::ZeroVector, FRotator::ZeroRotator);
	UProceduralMeshComponent* PMC = NewObject<UProceduralMeshComponent>(Owner, *Name);
	Owner->SetRootComponent(PMC);
	PMC->RegisterComponent();
	PMC->SetMobility(EComponentMobility::Movable);
	PMC->CreateMeshSection(0, P, Tris, Nrm, UV, TArray<FColor>(), T, false);
	PMC->SetCastShadow(false);
	PMC->bVisibleInReflectionCaptures = false;
	PMC->bVisibleInRealTimeSkyCaptures = false;
	Meshes.Add(Name, PMC);
	MeshMaterial.Add(Name, Spec->GetStringField(TEXT("material")));
	UE_LOG(LogMatter, Display, TEXT("MATTER mesh %s verts=%d tris=%d material=%s"), *Name, N, M / 3, *MeshMaterial[Name]);
	return true;
}

UMaterialInterface* AMatterRuntimeGameMode::LoadMaster(const FString& Token)
{
	if (TObjectPtr<UMaterialInterface>* Hit = Masters.Find(Token))
	{
		return *Hit;
	}
	const FString Path = FString::Printf(TEXT("/Game/Masters/M_Matter_%s.M_Matter_%s"), *Token, *Token);
	UMaterialInterface* Master = LoadObject<UMaterialInterface>(nullptr, *Path);
	if (!Master)
	{
		UE_LOG(LogMatter, Error, TEXT("MATTER no master %s"), *Path);
		return nullptr;
	}
#if WITH_EDITOR
	// Editor-hosted: the master's shaders may still be compiling; block until they are done
	// (UR-F7). A cooked package ships them compiled.
	if (FMaterialResource* Res = Master->GetMaterialResource(GMaxRHIShaderPlatform))
	{
		Res->FinishCompilation();
	}
#endif
	Masters.Add(Token, Master);
	return Master;
}

UTexture2D* AMatterRuntimeGameMode::LoadTexture(const FString& File, bool bSRGB)
{
	const FString Key = File + (bSRGB ? TEXT("|srgb") : TEXT("|linear"));
	if (TObjectPtr<UTexture2D>* Hit = Textures.Find(Key))
	{
		return *Hit;
	}
	UTexture2D* Tex = FImageUtils::ImportFileAsTexture2D(File);
	if (!Tex)
	{
		UE_LOG(LogMatter, Error, TEXT("MATTER cannot load texture %s"), *File);
		return nullptr;
	}
	// The colour flag must match the master's sampler type, or Unreal draws its default
	// material with every check green (platform learning); the masters sample data as linear.
	Tex->SRGB = bSRGB;
	Tex->AddressX = TA_Wrap;
	Tex->AddressY = TA_Wrap;
	Tex->Filter = TF_Bilinear;
	Tex->UpdateResource();
	Textures.Add(Key, Tex);
	return Tex;
}

bool AMatterRuntimeGameMode::ApplySetting(int32 Index)
{
	const TArray<TSharedPtr<FJsonValue>>& Settings = Job->GetArrayField(TEXT("settings"));
	const TSharedPtr<FJsonObject> S = Settings[Index]->AsObject();
	double SunScale = 1.0, SkyScale = 1.0;
	S->TryGetNumberField(TEXT("sun_scale"), SunScale);
	S->TryGetNumberField(TEXT("sky_scale"), SkyScale);
	SunComp->SetIntensity(SunIntensity * SunScale);
	SkyComp->SetIntensity(SkyIntensity * SkyScale);

	TMap<FString, UMaterialInstanceDynamic*> Built;
	const TSharedPtr<FJsonObject> Mats = S->GetObjectField(TEXT("materials"));
	for (const auto& Pair : Mats->Values)
	{
		const TSharedPtr<FJsonObject> Spec = Pair.Value->AsObject();
		UMaterialInterface* Master = LoadMaster(Spec->GetStringField(TEXT("master")));
		if (!Master)
		{
			return false;
		}
		UMaterialInstanceDynamic* Mid = UMaterialInstanceDynamic::Create(Master, this);
		const TSharedPtr<FJsonObject>* Obj = nullptr;
		if (Spec->TryGetObjectField(TEXT("scalars"), Obj))
		{
			for (const auto& V : (*Obj)->Values)
			{
				Mid->SetScalarParameterValue(*V.Key, V.Value->AsNumber());
			}
		}
		if (Spec->TryGetObjectField(TEXT("vectors"), Obj))
		{
			for (const auto& V : (*Obj)->Values)
			{
				Mid->SetVectorParameterValue(*V.Key, Colour(V.Value->AsArray()));
			}
		}
		if (Spec->TryGetObjectField(TEXT("textures"), Obj))
		{
			for (const auto& V : (*Obj)->Values)
			{
				const TSharedPtr<FJsonObject> Tx = V.Value->AsObject();
				UTexture2D* Tex = LoadTexture(Tx->GetStringField(TEXT("file")), Tx->GetBoolField(TEXT("srgb")));
				if (!Tex)
				{
					return false;
				}
				Mid->SetTextureParameterValue(*V.Key, Tex);
			}
		}
		Mids.Add(Mid);
		Built.Add(Pair.Key, Mid);
	}
	for (const auto& Pair : Meshes)
	{
		UMaterialInstanceDynamic** Mid = Built.Find(MeshMaterial[Pair.Key]);
		if (!Mid)
		{
			UE_LOG(LogMatter, Error, TEXT("MATTER setting %s has no material %s for mesh %s"),
				*S->GetStringField(TEXT("id")), *MeshMaterial[Pair.Key], *Pair.Key);
			return false;
		}
		Pair.Value->SetMaterial(0, *Mid);
	}
	SettingIndex = Index;
	ReadyFrames = 0;
	Phase = EPhase::Settle;
	UE_LOG(LogMatter, Display, TEXT("MATTER setting %d/%d %s"), Index + 1, Settings.Num(), *S->GetStringField(TEXT("id")));
	return true;
}

bool AMatterRuntimeGameMode::IsReady() const
{
	// No shader jobs pending and no mesh still precaching its pipeline states, held for
	// SettleFrames frames in a row. (The master's IsGameThreadShaderMapComplete() read false
	// while it rendered, UR-F7, so it is not used.)
	if (GShaderCompilingManager && GShaderCompilingManager->GetNumRemainingJobs() > 0)
	{
		return false;
	}
	for (const auto& Pair : Meshes)
	{
		if (Pair.Value->IsPSOPrecaching())
		{
			return false;
		}
	}
	return !SkySphere->IsPSOPrecaching();
}

void AMatterRuntimeGameMode::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	if (Phase == EPhase::Done)
	{
		return;
	}
	++Frames;
	if (Frames > MaxFrames)
	{
		UE_LOG(LogMatter, Error, TEXT("MATTER not ready after %d frames (setting %d); nothing captured"), Frames, SettingIndex);
		Finish(3);
		return;
	}
	if (Phase == EPhase::Settle)
	{
		ReadyFrames = IsReady() ? ReadyFrames + 1 : 0;
		if (ReadyFrames < SettleFrames)
		{
			return;
		}
		if (!bSkyCaptured)
		{
			// the sky is captured once its sphere's material is ready, then given time to land
			SkyComp->RecaptureSky();
			bSkyCaptured = true;
			WaitFrames = SkyWaitFrames;
			Phase = EPhase::SkyWait;
			return;
		}
	}
	else if (Phase == EPhase::SkyWait && --WaitFrames > 0)
	{
		return;
	}
	if (!CaptureSetting())
	{
		Finish(1);
		return;
	}
	if (SettingIndex + 1 >= Job->GetArrayField(TEXT("settings")).Num())
	{
		Finish(0);
	}
	else if (!ApplySetting(SettingIndex + 1))
	{
		Finish(2);
	}
}

bool AMatterRuntimeGameMode::CaptureSetting()
{
	const FString Id = Job->GetArrayField(TEXT("settings"))[SettingIndex]->AsObject()->GetStringField(TEXT("id"));
	for (const TSharedPtr<FJsonValue>& V : Job->GetArrayField(TEXT("views")))
	{
		const TSharedPtr<FJsonObject> View = V->AsObject();
		if (!CaptureView(View, OutDir / (Id + View->GetStringField(TEXT("suffix")) + TEXT(".pfm"))))
		{
			return false;
		}
	}
	return true;
}

bool AMatterRuntimeGameMode::CaptureView(const TSharedPtr<FJsonObject>& View, const FString& OutPath)
{
	const FVector Loc = Vec(View, TEXT("location"));
	const FVector Fwd = Vec(View, TEXT("forward"), FVector(1, 0, 0));
	const FVector Up = Vec(View, TEXT("up"), FVector(0, 0, 1));
	CaptureComp->SetWorldLocationAndRotation(Loc, FRotationMatrix::MakeFromXZ(Fwd, Up).Rotator());
	CaptureComp->FOVAngle = View->GetNumberField(TEXT("fov"));
	CaptureComp->bOverride_CustomNearClippingPlane = true;
	CaptureComp->CustomNearClippingPlane = View->GetNumberField(TEXT("near"));
	CaptureComp->HiddenComponents.Reset();
	for (const TSharedPtr<FJsonValue>& H : View->GetArrayField(TEXT("hide")))
	{
		if (TObjectPtr<UProceduralMeshComponent>* Mesh = Meshes.Find(H->AsString()))
		{
			CaptureComp->HiddenComponents.Add(Mesh->Get());
		}
	}
	CaptureComp->CaptureScene();
	FlushRenderingCommands();

	FTextureRenderTargetResource* Res = Target->GameThread_GetRenderTargetResource();
	TArray<FLinearColor> Px;
	if (!Res || !Res->ReadLinearColorPixels(Px, FReadSurfaceDataFlags(RCM_MinMax)) || Px.Num() != Width * Width)
	{
		UE_LOG(LogMatter, Error, TEXT("MATTER readback failed for %s"), *OutPath);
		return false;
	}
	// Portable float map (PFM): a text header, then bottom-to-top rows of little-endian float RGB.
	TArray<uint8> Bytes;
	const FString Header = FString::Printf(TEXT("PF\n%d %d\n-1.0\n"), Width, Width);
	const FTCHARToUTF8 H(*Header);
	Bytes.Append(reinterpret_cast<const uint8*>(H.Get()), H.Length());
	Bytes.Reserve(Bytes.Num() + Width * Width * 12);
	for (int32 Y = Width - 1; Y >= 0; --Y)
	{
		for (int32 X = 0; X < Width; ++X)
		{
			const FLinearColor& C = Px[Y * Width + X];
			const float RGB[3] = { C.R, C.G, C.B };
			Bytes.Append(reinterpret_cast<const uint8*>(RGB), sizeof(RGB));
		}
	}
	IFileManager::Get().MakeDirectory(*FPaths::GetPath(OutPath), true);
	const bool bOk = FFileHelper::SaveArrayToFile(Bytes, *OutPath);
	UE_LOG(LogMatter, Display, TEXT("MATTER wrote=%d %s frame=%d centre=%s"), bOk, *OutPath, Frames,
		*Px[(Width / 2) * Width + Width / 2].ToString());
	return bOk;
}

void AMatterRuntimeGameMode::Finish(int32 Code)
{
	Phase = EPhase::Done;
	UE_LOG(LogMatter, Display, TEXT("MATTER exit=%d"), Code);
	FPlatformMisc::RequestExitWithStatus(false, Code);
}
