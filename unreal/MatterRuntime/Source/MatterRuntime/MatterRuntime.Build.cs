using UnrealBuildTool;

public class MatterRuntime : ModuleRules
{
	public MatterRuntime(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
		PublicDependencyModuleNames.AddRange(new string[] {
			"Core", "CoreUObject", "Engine", "RenderCore", "RHI", "ImageCore", "Json", "ProceduralMeshComponent" });
	}
}
