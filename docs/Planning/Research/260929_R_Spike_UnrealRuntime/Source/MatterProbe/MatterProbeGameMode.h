#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "MatterProbeGameMode.generated.h"

class USceneCaptureComponent2D;
class UTextureRenderTarget2D;
class UMaterialInstanceDynamic;

// Probe: spawn a sphere on a master, a sun and a sky, capture linear scene colour once, write it, exit.
UCLASS()
class AMatterProbeGameMode : public AGameModeBase
{
	GENERATED_BODY()

public:
	AMatterProbeGameMode();
	virtual void StartPlay() override;
	virtual void Tick(float DeltaSeconds) override;

private:
	void BuildScene();
	bool CaptureAndWrite();

	UPROPERTY() TObjectPtr<USceneCaptureComponent2D> CaptureComp;
	UPROPERTY() TObjectPtr<UTextureRenderTarget2D> Target;
	UPROPERTY() TObjectPtr<UMaterialInstanceDynamic> Mid;
	UPROPERTY() TObjectPtr<class UStaticMeshComponent> SphereComp;

	FString OutPath;
	FString MasterPath = TEXT("/Game/Masters/M_Matter_Opaque.M_Matter_Opaque");
	int32 Width = 512;
	int32 SettleFrames = 600;
	int32 ReadyFrames = 0;
	int32 Frames = 0;
	bool bDone = false;
};
