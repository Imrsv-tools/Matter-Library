using UnrealBuildTool;

public class MatterProbeTarget : TargetRules
{
	public MatterProbeTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Game;
		DefaultBuildSettings = BuildSettingsVersion.Latest;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		ExtraModuleNames.Add("MatterProbe");
	}
}
