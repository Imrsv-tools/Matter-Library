# Build the Matter Unreal runtime's editor target and masters on Windows: the twin of build.sh's
# two CPU steps (2026-11-12). Needs Unreal Engine 5.8.
#
#   $env:UE = '<an Unreal 5.8 install>'; powershell -File unreal/build.ps1 [editor|masters|all]
#
#   editor   the C++ editor target (capped jobs, below-normal priority)    — CPU
#   masters  the masters, by commandlet with no GPU (-nullrhi)             — CPU
#   all      editor, then masters (default)
#
# No package step: the published test runtime is built on Linux only (build.sh package), and a
# master change made on Windows writes a dated "runtime owed" line instead (Phase31 RD-P31-1).
# The rig on Windows runs editor mode on this project (tools/parity/drivers/unreal.py).
#
# The masters step reads the MATTER_MASTERS_* switches exactly as build.sh's does (the head of
# Scripts/build_masters.py lists them). Every Unreal asset is generated here; none is committed.
param([ValidateSet('editor', 'masters', 'all')][string]$Step = 'all')
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

switch ($Step) {
    'editor' { Build-Editor }
    'masters' { Build-Masters }
    'all' { Build-Editor; Build-Masters }
}
