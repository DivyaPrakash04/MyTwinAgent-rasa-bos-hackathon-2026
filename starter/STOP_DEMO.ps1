# STOP_DEMO.ps1 — free ports used by the demo (5005 Rasa, 5055 actions, 8000 MCP)
# Usage: Right-click -> Run with PowerShell, or: .\STOP_DEMO.ps1

$ports = @(5005, 5055, 8000)
$names = @{5005 = 'Rasa'; 5055 = 'Actions'; 8000 = 'MCP'}

Write-Host 'Stopping demo servers...' -ForegroundColor Cyan

foreach ($port in $ports) {
    $conns = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if (-not $conns) {
        Write-Host "  Port $port ($($names[$port])) — not in use" -ForegroundColor DarkGray
        continue
    }
    foreach ($pid in ($conns.OwningProcess | Select-Object -Unique)) {
        $proc = Get-Process -Id $pid -ErrorAction SilentlyContinue
        if ($proc) {
            Write-Host "  Stopping $($names[$port]) on port $port (PID $pid)..." -ForegroundColor Yellow
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
        }
    }
}

Start-Sleep -Seconds 2

$still = @()
foreach ($port in $ports) {
    if (Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue) {
        $still += $port
    }
}

if ($still.Count -gt 0) {
    Write-Host "Some ports still in use: $($still -join ', '). Close those terminal windows manually." -ForegroundColor Red
} else {
    Write-Host 'All demo ports free. You can run DEMO_START.ps1 or DEMO_PRESENTATION.ps1 again.' -ForegroundColor Green
}
