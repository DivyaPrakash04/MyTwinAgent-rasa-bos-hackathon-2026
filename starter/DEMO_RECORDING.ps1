# DEMO_RECORDING.ps1
# Opens server windows and a text-mode demo that saves a transcript log.
# Usage: Right-click -> Run with PowerShell, or from a terminal:
#   Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
#   .\DEMO_RECORDING.ps1

$base = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $base

function Start-DemoTerminal {
    param(
        [string]$Title,
        [string]$Command
    )

    $inner = @"
Set-Location '$base'
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
`$Host.UI.RawUI.WindowTitle = '$Title'
Write-Host '=== $Title ===' -ForegroundColor Cyan
$Command
"@

    Start-Process powershell -ArgumentList @('-NoExit', '-Command', $inner) -WindowStyle Normal
}

Write-Host 'Starting demo helper — opening server windows...' -ForegroundColor Cyan

Start-DemoTerminal 'Demo — MCP' 'python agentic/servers/ops_mcp_server/server.py'
Start-Sleep -Seconds 1
Start-DemoTerminal 'Demo — Actions' 'python -m rasa run actions'
Start-Sleep -Seconds 1
Start-DemoTerminal 'Demo — Rasa' 'python -m rasa run --enable-api --cors "*" --sub-agents agentic/sub_agents'

Write-Host 'Waiting 15 seconds for servers to start...' -ForegroundColor Yellow
Start-Sleep -Seconds 15

$log = Join-Path $base ("demo_recording_{0}.log" -f (Get-Date -Format 'yyyyMMdd-HHmmss'))
Write-Host "Opening recording terminal (log: $log)" -ForegroundColor Green

$recordCmd = @"
Set-Location '$base'
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
`$Host.UI.RawUI.WindowTitle = 'Demo — Recording'
Start-Transcript -Path '$log'
python -m voice.demo --text
Stop-Transcript
Write-Host 'Transcript saved to $log' -ForegroundColor Green
"@

Start-Process powershell -ArgumentList @('-NoExit', '-Command', $recordCmd) -WindowStyle Normal

Write-Host 'All windows launched. Type messages in the Recording terminal.' -ForegroundColor Yellow
