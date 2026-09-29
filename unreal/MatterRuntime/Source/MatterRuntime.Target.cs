using UnrealBuildTool;

public class MatterRuntimeTarget : TargetRules
{
	public MatterRuntimeTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Game;
		DefaultBuildSettings = BuildSettingsVersion.Latest;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		ExtraModuleNames.Add("MatterRuntime");
	}
}
