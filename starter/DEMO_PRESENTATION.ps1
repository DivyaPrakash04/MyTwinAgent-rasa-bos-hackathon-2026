# DEMO_PRESENTATION.ps1
# Launch servers and run the full 2-act presentation demo with a saved transcript.
# Record the "Demo — Presentation" window with Win+G (Xbox Game Bar) or OBS.
#
# Usage: Right-click -> Run with PowerShell

$base = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $base

$recordDir = Join-Path $base 'recordings'
New-Item -ItemType Directory -Force -Path $recordDir | Out-Null
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$transcript = Join-Path $recordDir "presentation_$stamp.md"
$consoleLog = Join-Path $recordDir "presentation_$stamp.log"

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

Clear-Host
Write-Host ''
Write-Host '  MyTwinAgent (RxTwin) — Presentation Recording' -ForegroundColor Magenta
Write-Host '  =============================================' -ForegroundColor Magenta
Write-Host ''
Write-Host '  BEFORE the demo starts:' -ForegroundColor Yellow
Write-Host '    1. Press Win+G to open Xbox Game Bar (or start OBS).'
Write-Host '    2. Turn ON system audio / game audio in the recorder settings.'
Write-Host '       (Game Bar often records mic only — see RECORDING.md if voice is silent.)'
Write-Host '    3. Choose "Capture" and record the Presentation window.'
Write-Host ''
Write-Host '  Output files will be saved to:' -ForegroundColor Cyan
Write-Host "    $transcript"
Write-Host "    $consoleLog"
Write-Host ''
Read-Host 'Press Enter to start servers and the scripted demo'

Write-Host 'Stopping any leftover demo servers...' -ForegroundColor Yellow
& (Join-Path $base 'STOP_DEMO.ps1')

Write-Host 'Resetting ticket store for a clean Act 1...' -ForegroundColor Yellow
& (Join-Path $base '.venv\Scripts\python.exe') -c "from actions.tickets import reset_demo_tickets; reset_demo_tickets(); print('tickets cleared')"

Write-Host 'Training assistant (picks up new Act 2 flows)...' -ForegroundColor Yellow
& (Join-Path $base '.venv\Scripts\python.exe') -m rasa train --data data agentic/flows --sub-agents agentic/sub_agents --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host 'Training failed — fix errors above, then re-run.' -ForegroundColor Red
    Read-Host 'Press Enter to exit'
    exit 1
}

Write-Host 'Starting servers...' -ForegroundColor Cyan
Start-DemoTerminal 'Demo — MCP' 'python agentic/servers/ops_mcp_server/server.py'
Start-Sleep -Seconds 1
Start-DemoTerminal 'Demo — Actions' 'python -m rasa run actions'
Start-Sleep -Seconds 1
Start-DemoTerminal 'Demo — Rasa' 'python -m rasa run --enable-api --cors "*" --endpoints endpoints.demo.yml --sub-agents agentic/sub_agents'

Write-Host 'Waiting 20 seconds for Rasa to be ready...' -ForegroundColor Yellow
Start-Sleep -Seconds 20

# Pre-generate user voice clips if missing or script changed (needs SPEECHMATICS_API_KEY)
Write-Host 'Refreshing pharmacist voice clips for updated script...' -ForegroundColor Yellow
& (Join-Path $base '.venv\Scripts\python.exe') -m voice.generate_audio

Write-Host 'Starting presentation demo (spoken audio)...' -ForegroundColor Green

$demoCmd = @"
Set-Location '$base'
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
`$Host.UI.RawUI.WindowTitle = 'Demo — Presentation'
Write-Host ''
Write-Host '>>> START SCREEN RECORDING NOW (Win+G or OBS) <<<' -ForegroundColor Yellow
Write-Host ''
Start-Sleep -Seconds 5
Start-Transcript -Path '$consoleLog'
python -m voice.demo --presentation --pause 4 --transcript '$transcript'
Stop-Transcript
Write-Host ''
Write-Host 'Recording complete.' -ForegroundColor Green
Write-Host 'Transcript: $transcript' -ForegroundColor Cyan
Write-Host 'Console log: $consoleLog' -ForegroundColor Cyan
Write-Host 'Stop your screen recorder and share the video + transcript.' -ForegroundColor Yellow
Read-Host 'Press Enter to close'
"@

Start-Process powershell -ArgumentList @('-NoExit', '-Command', $demoCmd) -WindowStyle Maximized

Write-Host ''
Write-Host 'Presentation window opened. Record it, then share the video and transcript.' -ForegroundColor Green
