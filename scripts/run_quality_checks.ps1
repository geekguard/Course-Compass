$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$LogPath = Join-Path $ProjectRoot "quality_check_results.txt"

if (-not (Test-Path $Python)) {
    throw "Project virtual environment was not found at $Python. Create .venv and install requirements.txt first."
}

"Course Compass Quality Checks" | Set-Content -Path $LogPath -Encoding UTF8
"Run time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" | Add-Content -Path $LogPath -Encoding UTF8
"Python: $Python" | Add-Content -Path $LogPath -Encoding UTF8

function Invoke-QualityCheck {
    param(
        [Parameter(Mandatory=$true)][string]$Label,
        [Parameter(Mandatory=$true)][string[]]$Arguments
    )
    "`r`n===== $Label =====" | Tee-Object -FilePath $LogPath -Append
    & $Python @Arguments 2>&1 | Tee-Object -FilePath $LogPath -Append
    $Code = $LASTEXITCODE
    if ($Code -ne 0) {
        "FAILED: $Label (exit code $Code)" | Tee-Object -FilePath $LogPath -Append
        throw "$Label failed. See $LogPath for details."
    }
    "PASSED: $Label" | Tee-Object -FilePath $LogPath -Append
}

Invoke-QualityCheck -Label "Automated unit, integration and regression tests" -Arguments @("-m", "unittest", "discover", "-s", "tests", "-v")
Invoke-QualityCheck -Label "Synthetic labelled parser benchmark" -Arguments @("evaluation\run_evaluation.py")
Invoke-QualityCheck -Label "Python compilation check" -Arguments @("-m", "compileall", "-q", "app.py", "chatbot", "data", "models", "tests", "evaluation", "server_session.py")

"`r`nOVERALL RESULT: ALL QUALITY CHECKS PASSED" | Tee-Object -FilePath $LogPath -Append
Write-Host "All checks passed. Log saved to $LogPath" -ForegroundColor Green
