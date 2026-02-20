# ============================================================
#  Deploy EU AI Act App to VPS — Run from your Windows PC
#  Usage: .\deploy_to_vps.ps1 -VpsIp "YOUR_VPS_IP"
# ============================================================

param(
    [Parameter(Mandatory=$true)]
    [string]$VpsIp,
    
    [string]$VpsUser = "root",
    [string]$RemotePath = "/root/eu-ai-act"
)

$ProjectDir = Split-Path -Parent $PSScriptRoot  # C:\Users\Mr Robot\YBE
$DeployDir  = $PSScriptRoot                      # C:\Users\Mr Robot\YBE\deploy

Write-Host ""
Write-Host "  ==========================================" -ForegroundColor Cyan
Write-Host "   EU AI Act — Deploy to VPS" -ForegroundColor White
Write-Host "  ==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Target: $VpsUser@$VpsIp" -ForegroundColor Yellow
Write-Host ""

# ── Step 1: Upload deployment files ──
Write-Host "[1/5] Uploading Docker & Nginx config..." -ForegroundColor Yellow
scp "$DeployDir\Dockerfile" "${VpsUser}@${VpsIp}:${RemotePath}/"
scp "$DeployDir\docker-compose.yml" "${VpsUser}@${VpsIp}:${RemotePath}/"
scp "$DeployDir\nginx.conf" "${VpsUser}@${VpsIp}:${RemotePath}/"
scp "$DeployDir\enable_https.sh" "${VpsUser}@${VpsIp}:${RemotePath}/"

# ── Step 2: Upload Python app ──
Write-Host "[2/5] Uploading Python server..." -ForegroundColor Yellow
scp "$ProjectDir\eu_ai_act.py" "${VpsUser}@${VpsIp}:${RemotePath}/"
scp "$ProjectDir\eu_ai_act_server.py" "${VpsUser}@${VpsIp}:${RemotePath}/"

# ── Step 3: Upload web frontend ──
Write-Host "[3/5] Uploading PWA frontend..." -ForegroundColor Yellow
ssh ${VpsUser}@${VpsIp} "mkdir -p ${RemotePath}/web"
scp "$ProjectDir\web\index.html" "${VpsUser}@${VpsIp}:${RemotePath}/web/"
scp "$ProjectDir\web\app.js" "${VpsUser}@${VpsIp}:${RemotePath}/web/"
scp "$ProjectDir\web\style.css" "${VpsUser}@${VpsIp}:${RemotePath}/web/"
scp "$ProjectDir\web\manifest.json" "${VpsUser}@${VpsIp}:${RemotePath}/web/"
scp "$ProjectDir\web\sw.js" "${VpsUser}@${VpsIp}:${RemotePath}/web/"
scp "$ProjectDir\web\icon-192.png" "${VpsUser}@${VpsIp}:${RemotePath}/web/"
scp "$ProjectDir\web\icon-512.png" "${VpsUser}@${VpsIp}:${RemotePath}/web/"
scp "$ProjectDir\web\icon-maskable-512.png" "${VpsUser}@${VpsIp}:${RemotePath}/web/"
scp "$ProjectDir\web\apple-touch-icon.png" "${VpsUser}@${VpsIp}:${RemotePath}/web/"

# ── Step 4: Build & Start on VPS ──
Write-Host "[4/5] Building and starting on VPS..." -ForegroundColor Yellow
ssh ${VpsUser}@${VpsIp} "cd ${RemotePath} && docker-compose build && docker-compose up -d"

# ── Step 5: Verify ──
Write-Host "[5/5] Verifying deployment..." -ForegroundColor Yellow
Start-Sleep -Seconds 5
try {
    $response = Invoke-WebRequest -Uri "http://${VpsIp}:8080/api/stats" -Method GET -TimeoutSec 10
    $data = $response.Content | ConvertFrom-Json
    Write-Host ""
    Write-Host "  ==========================================" -ForegroundColor Green
    Write-Host "   DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
    Write-Host "  ==========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "  App URL:  http://${VpsIp}:8080" -ForegroundColor Yellow
    Write-Host "  API:      http://${VpsIp}:8080/api/stats" -ForegroundColor Gray
    Write-Host "  Days left: $($data.days_remaining)" -ForegroundColor White
    Write-Host ""
    Write-Host "  HTTPS?  Run on VPS:" -ForegroundColor Cyan
    Write-Host "    ssh ${VpsUser}@${VpsIp}" -ForegroundColor Gray
    Write-Host "    bash ${RemotePath}/enable_https.sh yourdomain.com" -ForegroundColor Gray
    Write-Host ""
} catch {
    Write-Host ""
    Write-Host "  [!] Could not verify. Check manually:" -ForegroundColor Red
    Write-Host "      ssh ${VpsUser}@${VpsIp}" -ForegroundColor Yellow
    Write-Host "      cd ${RemotePath} && docker-compose logs" -ForegroundColor Yellow
    Write-Host ""
}
