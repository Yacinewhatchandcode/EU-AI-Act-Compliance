# 🚀 EU AI Act — VPS Deployment Guide

## What's in this folder

| File | Purpose |
|------|---------|
| `Dockerfile` | Builds the Python app container |
| `docker-compose.yml` | Runs app + Nginx + Certbot |
| `nginx.conf` | Reverse proxy with HTTPS support |
| `setup_vps.sh` | One-time VPS setup (run on VPS) |
| `enable_https.sh` | Enable HTTPS with your domain |
| `deploy_to_vps.ps1` | One-command deploy from Windows |
| `.dockerignore` | Keeps Docker image lean |

## Quick Start (3 steps)

### 1️⃣ Get your VPS
- Go to [hostinger.com/davidondrej](https://hostinger.com/davidondrej)
- Use promo code: **DAVID**
- Choose Ubuntu 22.04 or 24.04

### 2️⃣ Setup VPS (one time)
```bash
ssh root@YOUR_VPS_IP
# Download and run setup
curl -sL https://raw.githubusercontent.com/your-repo/setup_vps.sh | bash
# OR copy and run manually:
# scp deploy/setup_vps.sh root@YOUR_VPS_IP:/root/
# ssh root@YOUR_VPS_IP "bash /root/setup_vps.sh"
```

### 3️⃣ Deploy from Windows
```powershell
cd C:\Users\Mr Robot\YBE\deploy
.\deploy_to_vps.ps1 -VpsIp "YOUR_VPS_IP"
```

That's it! Your app is live at `http://YOUR_VPS_IP:8080` 🎉

## Add HTTPS (optional)

1. Point your domain's DNS A record to your VPS IP
2. On the VPS:
```bash
bash /root/eu-ai-act/enable_https.sh yourdomain.com
```

## Useful Commands

```bash
# View logs
cd /root/eu-ai-act && docker-compose logs -f

# Restart
docker-compose restart

# Stop
docker-compose down

# Rebuild after code changes
docker-compose build && docker-compose up -d

# Check status
docker-compose ps
```

## Re-deploy after code changes
Just run from your Windows PC again:
```powershell
.\deploy_to_vps.ps1 -VpsIp "YOUR_VPS_IP"
```

---
*Powered by PRIME.AI*
