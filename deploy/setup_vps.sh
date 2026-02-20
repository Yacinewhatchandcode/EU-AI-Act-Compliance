#!/bin/bash
# ============================================================
#  EU AI Act + OpenClaw — VPS Auto Setup
#  Run this ON your Hostinger VPS after SSH-ing in:
#    ssh root@YOUR_VPS_IP
#    bash setup_vps.sh
# ============================================================

set -e  # Exit on error

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo -e "${CYAN}======================================================${NC}"
echo -e "${CYAN}  EU AI Act + OpenClaw — VPS Setup${NC}"
echo -e "${CYAN}  Powered by PRIME.AI${NC}"
echo -e "${CYAN}======================================================${NC}"
echo ""

# ── Step 1: System update ──
echo -e "${YELLOW}[1/7] Updating system...${NC}"
apt update -y && apt upgrade -y

# ── Step 2: Install essentials ──
echo -e "${YELLOW}[2/7] Installing Git, Docker, Docker Compose...${NC}"
apt install -y git curl wget ufw docker.io docker-compose

# Enable Docker
systemctl enable docker
systemctl start docker

# ── Step 3: Firewall ──
echo -e "${YELLOW}[3/7] Configuring firewall...${NC}"
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw allow 8080/tcp  # Direct app access (optional, for testing)
ufw --force enable

# ── Step 4: Clone OpenClaw ──
echo -e "${YELLOW}[4/7] Cloning OpenClaw...${NC}"
cd /root
if [ -d "openclaw" ]; then
    echo "  OpenClaw directory exists, pulling latest..."
    cd openclaw && git pull
else
    git clone https://github.com/openclaw/openclaw.git
    cd openclaw
fi

# ── Step 5: Create .env ──
echo -e "${YELLOW}[5/7] Creating .env configuration...${NC}"
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "  Created .env from template"
    else
        cat > .env << 'ENVEOF'
# ── OpenClaw Configuration ──
OPENCLAW_PORT=3000
OPENCLAW_HOST=0.0.0.0

# ── LLM API Keys (add yours) ──
# Uncomment and fill in whichever you use:
# ANTHROPIC_API_KEY=sk-ant-xxxxx
# OPENAI_API_KEY=sk-xxxxx

# ── EU AI Act App ──
EU_AI_ACT_PORT=8080
ENVEOF
        echo "  Created .env with defaults"
    fi
    echo ""
    echo -e "${RED}  ⚠️  IMPORTANT: Edit .env and add your API keys!${NC}"
    echo -e "${YELLOW}     nano /root/openclaw/.env${NC}"
    echo ""
else
    echo "  .env already exists, skipping"
fi

# ── Step 6: Setup EU AI Act app directory ──
echo -e "${YELLOW}[6/7] Preparing EU AI Act app...${NC}"
mkdir -p /root/eu-ai-act
echo ""
echo -e "${GREEN}  App directory ready at /root/eu-ai-act${NC}"
echo -e "${YELLOW}  Upload your files with:${NC}"
echo -e "${CYAN}    scp -r deploy/* root@THIS_VPS_IP:/root/eu-ai-act/${NC}"
echo -e "${CYAN}    scp eu_ai_act.py eu_ai_act_server.py root@THIS_VPS_IP:/root/eu-ai-act/${NC}"
echo -e "${CYAN}    scp -r web root@THIS_VPS_IP:/root/eu-ai-act/${NC}"

# ── Step 7: Show next steps ──
echo ""
echo -e "${CYAN}======================================================${NC}"
echo -e "${GREEN}  ✅ VPS SETUP COMPLETE!${NC}"
echo -e "${CYAN}======================================================${NC}"
echo ""
echo -e "  ${YELLOW}Next steps:${NC}"
echo ""
echo -e "  1. Upload your app files from your PC:"
echo -e "     ${CYAN}Run deploy_to_vps.ps1 on your Windows PC${NC}"
echo ""
echo -e "  2. (Optional) Add your domain:"
echo -e "     ${CYAN}Point your DNS A record to this server's IP${NC}"
echo -e "     ${CYAN}Then run: bash /root/eu-ai-act/enable_https.sh yourdomain.com${NC}"
echo ""
echo -e "  3. Start your app:"
echo -e "     ${CYAN}cd /root/eu-ai-act && docker-compose up -d${NC}"
echo ""
echo -e "  4. Your app will be live at:"
echo -e "     ${GREEN}http://$(curl -s ifconfig.me):8080${NC}"
echo ""
echo -e "${CYAN}======================================================${NC}"
