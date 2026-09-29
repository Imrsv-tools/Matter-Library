using UnrealBuildTool;

public class MatterProbeEditorTarget : TargetRules
{
	public MatterProbeEditorTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Editor;
		DefaultBuildSettings = BuildSettingsVersion.Latest;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		ExtraModuleNames.Add("MatterProbe");
	}
}
