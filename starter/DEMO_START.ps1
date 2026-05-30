# DEMO_START.ps1
# One-click launcher: opens four PowerShell windows for the voice demo.
# Usage: Right-click -> Run with PowerShell, or from a terminal:
#   Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
#   .\DEMO_START.ps1

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

Write-Host 'Opening demo terminals (MCP, Actions, Rasa, Voice)...' -ForegroundColor Cyan

Start-DemoTerminal 'Demo — MCP' 'python agentic/servers/ops_mcp_server/server.py'
Start-Sleep -Seconds 1
Start-DemoTerminal 'Demo — Actions' 'python -m rasa run actions'
Start-Sleep -Seconds 1
Start-DemoTerminal 'Demo — Rasa' 'python -m rasa run --enable-api --cors "*" --sub-agents agentic/sub_agents'

Write-Host 'Waiting 15 seconds for servers to start...' -ForegroundColor Yellow
Start-Sleep -Seconds 15

Start-DemoTerminal 'Demo — Voice' 'python -m voice.demo'

Write-Host 'Done. Use the Voice window after Rasa shows it is ready.' -ForegroundColor Green
Write-Host 'Text-only demo instead: python -m voice.demo --text' -ForegroundColor DarkGray
