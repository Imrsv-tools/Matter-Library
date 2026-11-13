# Build the Matter Unreal runtime on Windows: the twin of build.sh (2026-11-12; package 2026-11-13).
# Needs Unreal Engine 5.8.
#
#   $env:UE = '<an Unreal 5.8 install>'; powershell -File unreal/build.ps1 [editor|masters|package|all]
#
#   editor   the C++ editor target (capped jobs, below-normal priority)    — CPU
#   masters  the masters, by commandlet with no GPU (-nullrhi)             — CPU
#   package  cook + a Shipping build, symbols removed, archived to
#            unreal/dist/MatterRuntime-Win64.zip                           — CPU
#   all      editor, masters, package (default)
#
# The package is published by unreal/publish.sh N Win64. (Phase31 RD-P31-1 first ruled no package
# from Windows; the lead revised it 2026-11-13: "we should be able to publish with a windows build".)
# The rig on Windows still runs editor mode on this project by default (tools/parity/drivers/unreal.py).
#
# The masters step reads the MATTER_MASTERS_* switches exactly as build.sh's does (the head of
# Scripts/build_masters.py lists them). Every Unreal asset is generated here; none is committed.
param([ValidateSet('editor', 'masters', 'package', 'all')][string]$Step = 'all')
$ErrorActionPreference = 'Stop'

if (-not $env:UE) { Write-Error 'set UE to an Unreal Engine 5.8 install' }
$Project = Join-Path $PSScriptRoot 'MatterRuntime\MatterRuntime.uproject'
$Jobs = if ($env:MATTER_UE_JOBS) { $env:MATTER_UE_JOBS } else { 8 }   # never uncapped

# build.sh's `nice -n 19`: this process, and every process it starts, runs below normal.
(Get-Process -Id $PID).PriorityClass = 'BelowNormal'

function Build-Editor {
    & (Join-Path $env:UE 'Engine\Build\BatchFiles\Build.bat') MatterRuntimeEditor Win64 Development `
        "-Project=$Project" "-MaxParallelActions=$Jobs" -WaitMutex
    if ($LASTEXITCODE -ne 0) { Write-Error "editor: FAILED (Build.bat exited $LASTEXITCODE)" }
}

function Build-Masters {
    # A good build is BOTH an exit code of 0 and the builder's own "MATTER RESULT ok" line;
    # neither alone is enough (build.sh's masters step says when each one caught a failure).
    $log = New-TemporaryFile
    $ErrorActionPreference = 'Continue'      # the commandlet's stderr is output, not a throw
    & (Join-Path $env:UE 'Engine\Binaries\Win64\UnrealEditor-Cmd.exe') $Project -run=pythonscript `
        "-script=$(Join-Path $PSScriptRoot 'MatterRuntime\Scripts\build_masters.py')" `
        '-EnablePlugins=PythonScriptPlugin,EditorScriptingUtilities' -unattended -nullrhi -stdout `
        -FullStdOutLogOutput 2>&1 | ForEach-Object { "$_" } | Tee-Object -FilePath $log
    $status = $LASTEXITCODE
    $ErrorActionPreference = 'Stop'
    $text = Get-Content -Raw $log
    Remove-Item $log
    $result = if ($text -match 'MATTER RESULT ok') { 'reported' } else { 'did not report' }
    if ($status -ne 0 -or $result -ne 'reported') {
        Write-Error "masters: FAILED. The commandlet exited $status and the builder $result 'MATTER RESULT ok' (its output is above)."
    }
    $told = [regex]::Matches($text, 'MATTER told .*') | Select-Object -Last 1
    Write-Output "masters: ok. $told"
}

function Build-Package {
    $Staged = Join-Path $PSScriptRoot 'MatterRuntime\Packaged'
    $Dist = Join-Path $PSScriptRoot 'dist'
    if (Test-Path $Staged) { Remove-Item -Recurse -Force $Staged }
    & (Join-Path $env:UE 'Engine\Build\BatchFiles\RunUAT.bat') BuildCookRun "-project=$Project" -noP4 `
        -platform=Win64 -clientconfig=Shipping -build -cook -stage -pak -iostore -archive `
        "-archivedirectory=$Staged" -nodebuginfo -unattended -nocompileeditor `
        "-ubtargs=-MaxParallelActions=$Jobs"
    if ($LASTEXITCODE -ne 0) { Write-Error "package: FAILED (RunUAT exited $LASTEXITCODE)" }
    # What a run does not need (build.sh's UR-F8 strip): debug symbols
    Get-ChildItem -Recurse -File (Join-Path $Staged 'Windows') -Include '*.pdb', '*.debug', '*.sym' |
        Remove-Item -Force
    New-Item -ItemType Directory -Force $Dist | Out-Null
    $Zip = Join-Path $Dist 'MatterRuntime-Win64.zip'
    if (Test-Path $Zip) { Remove-Item -Force $Zip }
    & "$env:SystemRoot\System32\tar.exe" -a -c -f $Zip -C $Staged Windows      # Windows' bsdtar writes a zip
    if ($LASTEXITCODE -ne 0) { Write-Error "package: the zip FAILED (tar exited $LASTEXITCODE)" }
    $mb = [math]::Round((Get-Item $Zip).Length / 1MB)
    Write-Output "package: ok. $Zip ($mb MB)"
}

switch ($Step) {
    'editor' { Build-Editor }
    'masters' { Build-Masters }
    'package' { Build-Package }
    'all' { Build-Editor; Build-Masters; Build-Package }
}
