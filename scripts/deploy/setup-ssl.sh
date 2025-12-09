#!/bin/bash
#
# GreenEduMap-DTUDZ - Open Data Platform for Green Urban Development
# Copyright (C) 2025 DTU-DZ2 Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#

# ==============================================
# GreenEduMap SSL Setup Script
# ==============================================
# This script installs Nginx and SSL certificates

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}=========================================${NC}"
echo -e "${CYAN} GreenEduMap - SSL Setup${NC}"
echo -e "${CYAN}=========================================${NC}"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}ERROR: Please run as root (sudo)${NC}"
    exit 1
fi

# ===========================================
# 1. Get Domain Information
# ===========================================
echo -e "${YELLOW}[1/6] Domain Configuration${NC}"
echo ""
read -p "Enter your API domain (e.g., api.greenedumap.io.vn): " API_DOMAIN
read -p "Enter your Web App domain (e.g., greenedumap.io.vn): " WEB_DOMAIN
read -p "Enter your email for Let's Encrypt: " LETSENCRYPT_EMAIL

if [ -z "$API_DOMAIN" ]; then
    echo -e "${RED}ERROR: API domain is required${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✓ API Domain: $API_DOMAIN${NC}"
echo -e "${GREEN}✓ Web Domain: $WEB_DOMAIN${NC}"
echo -e "${GREEN}✓ Email: $LETSENCRYPT_EMAIL${NC}"
echo ""

# ===========================================
# 2. Install Nginx
# ===========================================
echo -e "${YELLOW}[2/6] Installing Nginx...${NC}"

if command -v nginx &> /dev/null; then
    echo -e "${GREEN}✓ Nginx already installed${NC}"
else
    apt update
    apt install -y nginx
    systemctl enable nginx
    systemctl start nginx
    echo -e "${GREEN}✓ Nginx installed${NC}"
fi

echo ""

# ===========================================
# 3. Install Certbot
# ===========================================
echo -e "${YELLOW}[3/6] Installing Certbot...${NC}"

if command -v certbot &> /dev/null; then
    echo -e "${GREEN}✓ Certbot already installed${NC}"
else
    apt install -y certbot python3-certbot-nginx
    echo -e "${GREEN}✓ Certbot installed${NC}"
fi

echo ""

# ===========================================
# 4. Configure Nginx (HTTP first)
# ===========================================
echo -e "${YELLOW}[4/6] Configuring Nginx...${NC}"

# API Gateway config
cat > /etc/nginx/sites-available/greenedumap-api << EOF
server {
    listen 80;
    listen [::]:80;
    server_name $API_DOMAIN;

    location / {
        proxy_pass http://localhost:4500;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

# Web App config (if provided)
if [ -n "$WEB_DOMAIN" ]; then
    cat > /etc/nginx/sites-available/greenedumap-web << EOF
server {
    listen 80;
    listen [::]:80;
    server_name $WEB_DOMAIN;

    location / {
        proxy_pass http://localhost:4501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF
fi

# Enable sites
ln -sf /etc/nginx/sites-available/greenedumap-api /etc/nginx/sites-enabled/
if [ -n "$WEB_DOMAIN" ]; then
    ln -sf /etc/nginx/sites-available/greenedumap-web /etc/nginx/sites-enabled/
fi

# Remove default site
rm -f /etc/nginx/sites-enabled/default

# Test nginx config
nginx -t

# Reload nginx
systemctl reload nginx

echo -e "${GREEN}✓ Nginx configured${NC}"
echo ""

# ===========================================
# 5. Get SSL Certificates
# ===========================================
echo -e "${YELLOW}[5/6] Obtaining SSL certificates...${NC}"

if [ -z "$LETSENCRYPT_EMAIL" ]; then
    echo -e "${YELLOW}⚠️  No email provided, skipping SSL setup${NC}"
else
    # Get certificate for API domain
    certbot --nginx -d $API_DOMAIN --non-interactive --agree-tos -m $LETSENCRYPT_EMAIL --redirect
    
    # Get certificate for Web domain (if provided)
    if [ -n "$WEB_DOMAIN" ]; then
        certbot --nginx -d $WEB_DOMAIN --non-interactive --agree-tos -m $LETSENCRYPT_EMAIL --redirect
    fi
    
    echo -e "${GREEN}✓ SSL certificates obtained${NC}"
fi

echo ""

# ===========================================
# 6. Setup Auto-renewal
# ===========================================
echo -e "${YELLOW}[6/6] Setting up auto-renewal...${NC}"

# Test renewal
certbot renew --dry-run

echo -e "${GREEN}✓ Auto-renewal configured${NC}"
echo ""

# ===========================================
# Summary
# ===========================================
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN} SSL Setup Complete!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo -e "${CYAN}Your services are now available at:${NC}"
echo "  API Gateway:  https://$API_DOMAIN"
if [ -n "$WEB_DOMAIN" ]; then
    echo "  Web App:      https://$WEB_DOMAIN"
fi
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Update CORS_ORIGINS in .env.production"
echo "  2. Update NEXT_PUBLIC_API_URL in .env.production"
echo "  3. Restart Docker services"
echo ""
echo -e "${CYAN}Commands:${NC}"
echo "  Check SSL: certbot certificates"
echo "  Renew SSL: certbot renew"
echo "  Nginx logs: tail -f /var/log/nginx/error.log"
echo ""
