#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "MatterRuntimeGameMode.generated.h"

class FJsonObject;
class UDirectionalLightComponent;
class UMaterialInstanceDynamic;
class UMaterialInterface;
class UProceduralMeshComponent;
class USceneCaptureComponent2D;
class USkyLightComponent;
class UStaticMeshComponent;
class UTexture2D;
class UTextureRenderTarget2D;

/**
 * Renders one "Unreal job" (written by tools/parity/drivers/unreal.py) and exits.
 *
 *   MatterRuntime -MatterJob=<abs path to unreal_job.json> -RenderOffscreen -unattended -nosound
 *
 * The job carries everything in Unreal's units (centimetres, Z up, left-handed): the meshes as
 * raw buffers (the driver converts the rig's scene; nothing is imported at run time), one
 * material per mesh slot per setting (a master plus its parameter values and texture files),
 * the views, and the lights. For every setting and view the app writes one linear float image,
 * <out_dir>/<setting id><view suffix>.pfm: scene colour before the tonemapper, exposure fixed.
 * The driver applies the view's exposure, box-filters the supersampling and encodes sRGB.
 *
 * Lighting is matched to the rig (JOB_FORMAT.md): a sun with no shadows, and a sky light
 * captured from a large unlit sphere of constant radiance, which is also the visible
 * background. So the dome is never read from a file (Phase06 D10; Storm learning S2).
 */
UCLASS()
class AMatterRuntimeGameMode : public AGameModeBase
{
	GENERATED_BODY()

public:
	AMatterRuntimeGameMode();
	virtual void StartPlay() override;
	virtual void Tick(float DeltaSeconds) override;

private:
	enum class EPhase : uint8 { Settle, SkyWait, Done };

	bool LoadJob(const FString& Path);
	bool BuildWorld();
	bool LoadMesh(const TSharedPtr<FJsonObject>& Spec);
	bool ApplySetting(int32 Index);
	UMaterialInterface* LoadMaster(const FString& Token);
	UTexture2D* LoadTexture(const TSharedPtr<FJsonObject>& Spec);
	bool IsReady() const;
	bool CaptureSetting();
	bool CaptureView(const TSharedPtr<FJsonObject>& View, const FString& OutPath);
	void Finish(int32 Code);
	void Note(const FString& Line, bool bError = false);

	UPROPERTY() TObjectPtr<USceneCaptureComponent2D> CaptureComp;
	UPROPERTY() TObjectPtr<UTextureRenderTarget2D> Target;
	UPROPERTY() TObjectPtr<USkyLightComponent> SkyComp;
	UPROPERTY() TObjectPtr<UDirectionalLightComponent> SunComp;
	UPROPERTY() TObjectPtr<UStaticMeshComponent> SkySphere;
	UPROPERTY() TMap<FString, TObjectPtr<UProceduralMeshComponent>> Meshes;
	UPROPERTY() TMap<FString, TObjectPtr<UMaterialInterface>> Masters;
	UPROPERTY() TMap<FString, TObjectPtr<UTexture2D>> Textures;
	UPROPERTY() TArray<TObjectPtr<UMaterialInstanceDynamic>> Mids;

	// 2 (6.3): mesh buffers carry a tangent sign; 3 (Phase09 9.3): the masters' own
	// base_color_map_tex, which an older master would silently leave white
	static constexpr int32 JobFormat = 3;

	TSharedPtr<FJsonObject> Job;
	TMap<FString, FString> MeshMaterial;     // mesh name -> the material slot id it takes
	FString OutDir;
	int32 Width = 512;
	int32 SettleFrames = 120;
	int32 SkyWaitFrames = 30;
	int32 MaxFrames = 20000;
	float SunIntensity = 1.f;
	float SkyIntensity = 1.f;

	EPhase Phase = EPhase::Settle;
	int32 SettingIndex = 0;
	int32 ReadyFrames = 0;
	int32 WaitFrames = 0;
	int32 Frames = 0;
	bool bSkyCaptured = false;
};
