#!/bin/bash
# ============================================================
#  Enable HTTPS for EU AI Act App
#  Usage: bash enable_https.sh yourdomain.com
# ============================================================

set -e

DOMAIN=$1

if [ -z "$DOMAIN" ]; then
    echo "Usage: bash enable_https.sh yourdomain.com"
    exit 1
fi

echo ""
echo "🔒 Setting up HTTPS for: $DOMAIN"
echo ""

# Replace placeholder in nginx config
APP_DIR="/root/eu-ai-act"
cd "$APP_DIR"

sed -i "s/YOUR_DOMAIN/$DOMAIN/g" nginx.conf

echo "[1/3] Nginx config updated for $DOMAIN"

# Start containers WITHOUT SSL first (to get certs)
echo "[2/3] Starting services to obtain certificate..."

# Create a temporary nginx config for initial cert request
cat > nginx_temp.conf << TMPEOF
server {
    listen 80;
    server_name $DOMAIN;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        proxy_pass http://eu-ai-act:8080;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
TMPEOF

# Use temp config to start
cp nginx.conf nginx_ssl.conf
cp nginx_temp.conf nginx.conf

docker-compose up -d eu-ai-act nginx

sleep 5

# Get SSL certificate
echo "[3/3] Requesting SSL certificate from Let's Encrypt..."
docker-compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email admin@$DOMAIN \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN

# Swap to full SSL config
cp nginx_ssl.conf nginx.conf
rm -f nginx_temp.conf nginx_ssl.conf

# Restart with SSL
docker-compose restart nginx

echo ""
echo "✅ HTTPS is live!"
echo "🌐 https://$DOMAIN"
echo ""
