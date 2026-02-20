# EU AI Act Compliance — Mobile PWA Launcher
# ============================================
# - Starts the API server on ALL network interfaces (0.0.0.0)
# - Shows your local IP + QR code for instant mobile access
# - Opens the app in your default browser
#
# USAGE: .\launch_mobile.ps1

Write-Host ""
Write-Host "  ==========================================" -ForegroundColor Cyan
Write-Host "   EU AI Act Compliance - Mobile PWA" -ForegroundColor White
Write-Host "  ==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if the server is already running
$existing = Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "  [!] Port 8080 is already in use. Stopping existing process..." -ForegroundColor Yellow
    $pid = $existing.OwningProcess | Select-Object -First 1
    Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
}

# Get local IP
$localIp = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {
    $_.IPAddress -ne "127.0.0.1" -and $_.PrefixOrigin -ne "WellKnown"
} | Select-Object -First 1).IPAddress

if (-not $localIp) { $localIp = "127.0.0.1" }

$mobileUrl = "http://${localIp}:8080"

Write-Host "  Starting server..." -ForegroundColor Gray

# Start the server in background
$serverJob = Start-Process python -ArgumentList "`"$PSScriptRoot\eu_ai_act_server.py`"" -PassThru -WindowStyle Normal

Start-Sleep -Seconds 3

# Verify server is running
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8080/api/stats" -Method GET -TimeoutSec 5 -ErrorAction Stop
    Write-Host "  [OK] Server is running!" -ForegroundColor Green
} catch {
    Write-Host "  [ERROR] Server failed to start!" -ForegroundColor Red
    Write-Host "  Try: python eu_ai_act_server.py" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "  ==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  PC:      http://localhost:8080" -ForegroundColor White
Write-Host "  MOBILE:  $mobileUrl" -ForegroundColor Yellow
Write-Host ""
Write-Host "  HOW TO INSTALL ON YOUR PHONE:" -ForegroundColor Cyan
Write-Host "  ─────────────────────────────" -ForegroundColor DarkGray
Write-Host "  1. Connect your phone to the same WiFi" -ForegroundColor White
Write-Host "  2. Open $mobileUrl in Chrome" -ForegroundColor Yellow
Write-Host "  3. Chrome: tap menu ... > 'Install app'" -ForegroundColor White
Write-Host "     Safari: tap share > 'Add to Home Screen'" -ForegroundColor White
Write-Host ""
Write-Host "  ==========================================" -ForegroundColor Cyan

# Open in browser
Start-Process $mobileUrl

# Generate QR code image if Python is available
python -c "
import qrcode
qr = qrcode.QRCode(version=1, box_size=1, border=1)
qr.add_data('$mobileUrl')
qr.make(fit=True)
print()
print('  Scan this QR code on your phone:')
print()
qr.print_ascii(invert=True)
print()
" 2>$null

Write-Host ""
Write-Host "  Press Ctrl+C to stop the server" -ForegroundColor DarkGray
Write-Host ""

# Wait for server process to exit (or Ctrl+C)
try {
    $serverJob | Wait-Process
} catch {
    Write-Host "`n  Server stopped." -ForegroundColor Yellow
    $serverJob | Stop-Process -Force -ErrorAction SilentlyContinue
}
