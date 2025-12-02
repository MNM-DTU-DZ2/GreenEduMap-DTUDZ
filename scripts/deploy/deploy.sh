#!/bin/bash
# ============================================
# GreenEduMap Production Deployment v1.0
# Automated VPS deployment with domain/SSL support
# ============================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}🌱 GreenEduMap Production Deployment v1.0${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Check root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}❌ Please run as root: sudo ./deploy.sh${NC}"
    exit 1
fi

# Configuration
PROJECT_DIR="/opt/greenedumap"
DOCKER_DIR="${PROJECT_DIR}/infrastructure/docker"
BACKUP_DIR="/opt/backups/greenedumap"

# ============================================
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}Select deployment mode:${NC}"
echo "1) 🌐 Domain-based (with SSL)"
echo "   Example: greenedumap.com with auto SSL"
echo "   Recommended for: Production"
echo ""
echo "2) 🖥️  IP-only (direct access via IP:PORT)"
echo "   Example: 34.85.44.142:8000"
echo "   Recommended for: Testing, development"
echo ""
read -p "Enter choice [1-2]: " DEPLOY_MODE

if [ "$DEPLOY_MODE" = "1" ]; then
    USE_DOMAIN=true
    echo ""
    echo -e "${YELLOW}📝 Domain-based deployment selected${NC}"
    read -p "Enter your domain (e.g., greenedumap.com): " DOMAIN
    read -p "Enter your email for SSL certificates: " EMAIL

    if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
        echo -e "${RED}❌ Domain and email are required!${NC}"
        exit 1
    fi

    echo -e "${GREEN}✅ Domain: $DOMAIN${NC}"
    echo -e "${GREEN}✅ Email: $EMAIL${NC}"

    # Main domain and www
    MAIN_DOMAIN="$DOMAIN"
    WWW_DOMAIN="www.$DOMAIN"
    API_DOMAIN="api.$DOMAIN"
else
    USE_DOMAIN=false
    SERVER_IP=$(curl -s ifconfig.me || echo "localhost")
    echo ""
    echo -e "${YELLOW}🖥️  IP-only deployment selected${NC}"
    echo -e "${GREEN}✅ Server IP: $SERVER_IP${NC}"
fi

echo ""

# ============================================
echo -e "${YELLOW}[Step 1/10] System Update${NC}"
apt-get update -qq
apt-get upgrade -y -qq
echo -e "${GREEN}✅ System updated${NC}"

# ============================================
echo -e "${YELLOW}[Step 2/10] Installing Docker${NC}"
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker
    systemctl start docker
    usermod -aG docker root
    echo -e "${GREEN}✅ Docker installed${NC}"
else
    echo -e "${GREEN}✅ Docker already installed${NC}"
fi

if ! command -v docker-compose &> /dev/null; then
    curl -sL "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo -e "${GREEN}✅ Docker Compose installed${NC}"
else
    echo -e "${GREEN}✅ Docker Compose already installed${NC}"
fi

# ============================================
# Install Nginx and Certbot (only for domain mode)
if [ "$USE_DOMAIN" = true ]; then
    echo -e "${YELLOW}[Step 3/10] Installing Nginx${NC}"
    if ! command -v nginx &> /dev/null; then
        apt-get install -y nginx
        systemctl enable nginx
        systemctl start nginx
        echo -e "${GREEN}✅ Nginx installed${NC}"
    else
        echo -e "${GREEN}✅ Nginx already installed${NC}"
    fi

    echo -e "${YELLOW}[Step 4/10] Installing Certbot${NC}"
    if ! command -v certbot &> /dev/null; then
        apt-get install -y certbot python3-certbot-nginx
        echo -e "${GREEN}✅ Certbot installed${NC}"
    else
        echo -e "${GREEN}✅ Certbot already installed${NC}"
    fi
fi

# ============================================
echo -e "${YELLOW}[Step 5/10] Installing Git${NC}"
if ! command -v git &> /dev/null; then
    apt-get install -y git
    echo -e "${GREEN}✅ Git installed${NC}"
else
    echo -e "${GREEN}✅ Git already installed${NC}"
fi

# ============================================
echo -e "${YELLOW}[Step 6/10] Cloning Repository${NC}"
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Enter repository URL (e.g., https://github.com/user/greenedumap.git):"
    read REPO_URL
    git clone "$REPO_URL" "$PROJECT_DIR"
    echo -e "${GREEN}✅ Repository cloned${NC}"
else
    echo -e "${GREEN}✅ Repository already exists${NC}"
    cd "$PROJECT_DIR"
    git pull origin main
    echo -e "${GREEN}✅ Repository updated${NC}"
fi

cd "$PROJECT_DIR"

# ============================================
echo -e "${YELLOW}[Step 7/10] Configuring Environment${NC}"

# Generate secure passwords
DB_PASSWORD=$(openssl rand -base64 32)
JWT_SECRET=$(openssl rand -base64 64)
REDIS_PASSWORD=$(openssl rand -base64 32)

# Create .env file
if [ "$USE_DOMAIN" = true ]; then
    cat > "${DOCKER_DIR}/.env" <<EOF
# Domain Configuration
DOMAIN="${DOMAIN}"
ADMIN_EMAIL="${EMAIL}"

# Database Configuration
POSTGRES_DB="greenedumap_prod"
POSTGRES_USER="greenedumap"
POSTGRES_PASSWORD="${DB_PASSWORD}"
POSTGRES_PORT="5433"

# Redis
REDIS_PASSWORD="${REDIS_PASSWORD}"
REDIS_PORT="6380"

# MongoDB
MONGO_ROOT_USERNAME="greenedumap"
MONGO_ROOT_PASSWORD="${DB_PASSWORD}"
MONGO_PORT="27018"

# JWT Configuration
JWT_SECRET="${JWT_SECRET}"
JWT_ACCESS_TOKEN_EXPIRE="1800"
JWT_REFRESH_TOKEN_EXPIRE="2592000"

# API Gateway
API_GATEWAY_HOST="0.0.0.0"
API_GATEWAY_PORT="10000"

# Web App
WEB_APP_PORT="4000"
NEXT_PUBLIC_API_URL="https://${API_DOMAIN}"

# Service URLs (internal Docker network)
AUTH_SERVICE_URL="http://auth-service:8001"
EDUCATION_SERVICE_URL="http://education-service:8008"
ENVIRONMENT_SERVICE_URL="http://environment-service:8007"
RESOURCE_SERVICE_URL="http://resource-service:8000"

# Environment
NODE_ENV="production"
DEBUG="false"
EOF
else
    cat > "${DOCKER_DIR}/.env" <<EOF
# IP-based Configuration
SERVER_IP="${SERVER_IP}"

# Database Configuration
POSTGRES_DB="greenedumap_prod"
POSTGRES_USER="greenedumap"
POSTGRES_PASSWORD="${DB_PASSWORD}"
POSTGRES_PORT="5433"

# Redis
REDIS_PASSWORD="${REDIS_PASSWORD}"
REDIS_PORT="6380"

# MongoDB
MONGO_ROOT_USERNAME="greenedumap"
MONGO_ROOT_PASSWORD="${DB_PASSWORD}"
MONGO_PORT="27018"

# JWT Configuration
JWT_SECRET="${JWT_SECRET}"
JWT_ACCESS_TOKEN_EXPIRE="1800"
JWT_REFRESH_TOKEN_EXPIRE="2592000"

# API Gateway
API_GATEWAY_HOST="0.0.0.0"
API_GATEWAY_PORT="10000"

# Web App
WEB_APP_PORT="4000"
NEXT_PUBLIC_API_URL="http://${SERVER_IP}:10000"

# Service URLs (internal Docker network)
AUTH_SERVICE_URL="http://auth-service:8001"
EDUCATION_SERVICE_URL="http://education-service:8008"
ENVIRONMENT_SERVICE_URL="http://environment-service:8007"
RESOURCE_SERVICE_URL="http://resource-service:8000"

# Environment
NODE_ENV="production"
DEBUG="false"
EOF
fi

echo -e "${GREEN}✅ Environment configured${NC}"

# Save passwords to secure file
cat > "/root/greenedumap-credentials.txt" <<EOF
GreenEduMap Deployment Credentials
Generated: $(date)
==================================

Database Password: ${DB_PASSWORD}
JWT Secret: ${JWT_SECRET}
Redis Password: ${REDIS_PASSWORD}

Keep this file secure!
EOF

chmod 600 /root/greenedumap-credentials.txt
echo -e "${GREEN}✅ Credentials saved to /root/greenedumap-credentials.txt${NC}"

# ============================================
echo -e "${YELLOW}[Step 8/10] Building and Starting Services${NC}"

cd "$DOCKER_DIR"

# Pull images
docker-compose pull

# Build custom images
docker-compose build

# Start services
docker-compose up -d

echo -e "${GREEN}✅ Services started${NC}"

# Wait for services to be healthy
echo "Waiting for services to be healthy..."
sleep 10

# ============================================
echo -e "${YELLOW}[Step 9/10] Running Database Migrations${NC}"

# Run migrations for each service
docker-compose exec -T auth-service alembic upgrade head || echo "Auth migrations skipped"
docker-compose exec -T education-service alembic upgrade head || echo "Education migrations skipped"

echo -e "${GREEN}✅ Migrations completed${NC}"

# ============================================
if [ "$USE_DOMAIN" = true ]; then
    echo -e "${YELLOW}[Step 10/10] Configuring Nginx and SSL${NC}"

    # Create Nginx config
    cat > /etc/nginx/sites-available/greenedumap <<EOF
# Green EduMap - Nginx Configuration
# Main domain and www redirect
server {
    listen 80;
    listen [::]:80;
    server_name ${MAIN_DOMAIN} ${WWW_DOMAIN};

    location / {
        proxy_pass http://localhost:4000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}

# API subdomain
server {
    listen 80;
    listen [::]:80;
    server_name ${API_DOMAIN};

    location / {
        proxy_pass http://localhost:10000;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # CORS headers
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type' always;
        
        if (\$request_method = 'OPTIONS') {
            return 204;
        }
    }
}
EOF

    # Enable site
    ln -sf /etc/nginx/sites-available/greenedumap /etc/nginx/sites-enabled/
    rm -f /etc/nginx/sites-enabled/default

    # Test Nginx config
    nginx -t

    # Reload Nginx
    systemctl reload nginx

    echo -e "${GREEN}✅ Nginx configured${NC}"

    # Setup SSL
    echo -e "${YELLOW}Setting up SSL certificates...${NC}"
    certbot --nginx -d ${MAIN_DOMAIN} -d ${WWW_DOMAIN} -d ${API_DOMAIN} --email ${EMAIL} --agree-tos --no-eff-email --redirect

    echo -e "${GREEN}✅ SSL certificates installed${NC}"
else
    echo -e "${YELLOW}[Step 10/10] Skipping Nginx/SSL (IP-only mode)${NC}"
fi

# ============================================
echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}✅ DEPLOYMENT COMPLETE!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""

if [ "$USE_DOMAIN" = true ]; then
    echo -e "${CYAN}🌐 Your application is available at:${NC}"
    echo -e "   Main site: https://${MAIN_DOMAIN}"
    echo -e "   API: https://${API_DOMAIN}"
    echo -e "   API Docs: https://${API_DOMAIN}/docs"
else
    echo -e "${CYAN}🖥️  Your application is available at:${NC}"
    echo -e "   Main site: http://${SERVER_IP}:4000"
    echo -e "   API: http://${SERVER_IP}:10000"
    echo -e "   API Docs: http://${SERVER_IP}:10000/docs"
fi

echo ""
echo -e "${YELLOW}📝 Important Information:${NC}"
echo "   - Credentials saved: /root/greenedumap-credentials.txt"
echo "   - Logs: docker-compose logs -f"
echo "   - Status: docker-compose ps"
echo "   - Update script: ./scripts/deploy/update.sh"
echo ""
echo -e "${CYAN}🔒 Security Recommendations:${NC}"
echo "   1. Setup firewall (ufw)"
echo "   2. Change default SSH port"
echo "   3. Disable root SSH login"
echo "   4. Setup fail2ban"
echo "   5. Regular backups"
echo ""
echo -e "${GREEN}Thank you for using GreenEduMap! 🌱${NC}"
echo ""
