<!--GreenEduMap-DTUDZ - Open Data Platform for Green Urban Development
Copyright (C) 2025 DTU-DZ2 Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.-->
# GreenEduMap SSL Setup Guide

## Prerequisites

1. **Domain Names** (đã trỏ DNS về VPS):
   - API: `api.greenedumap.io.vn` → `54.169.211.12`
   - Web: `greenedumap.io.vn` → `54.169.211.12`

2. **Ports mở trên firewall/security group**:
   - Port 80 (HTTP)
   - Port 443 (HTTPS)

## Quick Setup (Automated)

### 1. Upload script lên VPS

```bash
# Từ máy local, copy script lên VPS
scp scripts/deploy/setup-ssl.sh ubuntu@54.169.211.12:/opt/greenedumap/scripts/deploy/

# Hoặc trên VPS, pull code mới
cd /opt/greenedumap
git pull origin develop
```

### 2. Chạy script trên VPS

```bash
# SSH vào VPS
ssh ubuntu@54.169.211.12

# Chạy script với quyền root
cd /opt/greenedumap/scripts/deploy
sudo chmod +x setup-ssl.sh
sudo ./setup-ssl.sh
```

### 3. Nhập thông tin khi được hỏi

```
Enter your API domain: api.greenedumap.io.vn
Enter your Web App domain: greenedumap.io.vn
Enter your email for Let's Encrypt: your-email@example.com
```

### 4. Cập nhật environment variables

```bash
cd /opt/greenedumap/infrastructure/docker

# Sửa .env.production
nano .env.production
```

Thay đổi:
```env
# API URLs
NEXT_PUBLIC_API_URL=https://api.greenedumap.io.vn

# CORS Origins
CORS_ORIGINS=["https://greenedumap.io.vn","https://api.greenedumap.io.vn"]
```

### 5. Restart Docker services

```bash
docker-compose --env-file .env.production down
docker-compose --env-file .env.production up -d
```

## Manual Setup (Step by Step)

### 1. Install Nginx

```bash
sudo apt update
sudo apt install -y nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

### 2. Install Certbot

```bash
sudo apt install -y certbot python3-certbot-nginx
```

### 3. Configure Nginx

Create API config:
```bash
sudo nano /etc/nginx/sites-available/greenedumap-api
```

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name api.greenedumap.io.vn;

    location / {
        proxy_pass http://localhost:4500;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Create Web config:
```bash
sudo nano /etc/nginx/sites-available/greenedumap-web
```

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name greenedumap.io.vn;

    location / {
        proxy_pass http://localhost:4501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable sites:
```bash
sudo ln -s /etc/nginx/sites-available/greenedumap-api /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/greenedumap-web /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

### 4. Get SSL Certificates

```bash
# For API domain
sudo certbot --nginx -d api.greenedumap.io.vn

# For Web domain
sudo certbot --nginx -d greenedumap.io.vn
```

### 5. Test Auto-renewal

```bash
sudo certbot renew --dry-run
```

## Verification

### Check SSL Certificate

```bash
sudo certbot certificates
```

### Test HTTPS

```bash
# API
curl https://api.greenedumap.io.vn/health

# Web (from browser)
https://greenedumap.io.vn
```

### Check Nginx Logs

```bash
# Error logs
sudo tail -f /var/log/nginx/error.log

# Access logs
sudo tail -f /var/log/nginx/access.log
```

## Troubleshooting

### Port 80/443 not accessible

Check firewall:
```bash
sudo ufw status
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

AWS Security Group: Add inbound rules for ports 80 and 443.

### SSL Certificate Failed

Check DNS:
```bash
nslookup api.greenedumap.io.vn
```

Must return your VPS IP: `54.169.211.12`

### Nginx errors

Check config syntax:
```bash
sudo nginx -t
```

View detailed errors:
```bash
sudo journalctl -u nginx -n 50
```

## Certificate Renewal

Certificates auto-renew every 60 days via cron job.

Manual renewal:
```bash
sudo certbot renew
sudo systemctl reload nginx
```

## Security Headers (Optional)

Add to nginx config for better security:

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
```

## AWS/VPS Specific

### Security Group Rules

| Type | Protocol | Port | Source |
|------|----------|------|--------|
| HTTP | TCP | 80 | 0.0.0.0/0 |
| HTTPS | TCP | 443 | 0.0.0.0/0 |

### Elastic IP (Optional)

For production, use AWS Elastic IP to ensure IP doesn't change.
