using UnrealBuildTool;

public class MatterRuntimeEditorTarget : TargetRules
{
	public MatterRuntimeEditorTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Editor;
		DefaultBuildSettings = BuildSettingsVersion.Latest;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		ExtraModuleNames.Add("MatterRuntime");
	}
}
