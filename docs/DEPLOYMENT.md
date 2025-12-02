# GreenEduMap Production Deployment Guide

## Quick Start

### Prerequisites
- VPS with Ubuntu 20.04/22.04
- Root access
- Domain name pointing to VPS IP (optional)

### Initial Deployment

1. **SSH to your VPS:**
```bash
ssh root@your-vps-ip
```

2. **Download and run the deployment script:**
```bash
# Download deploy script
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/greenedumap/main/scripts/deploy/deploy.sh

# Make executable
chmod +x deploy.sh

# Run deployment
sudo ./deploy.sh
```

3. **Follow the prompts:**
   - Select deployment mode (Domain or IP-only)
   - Enter domain name (if mode 1)
   - Enter email for SSL (if mode 1)

4. **Wait for deployment to complete (~10-15 minutes)**

### Access Your Application

**Domain Mode:**
- Main Site: `https://yourdomain.com`
- API: `https://api.yourdomain.com`
- API Docs: `https://api.yourdomain.com/docs`

**IP Mode:**
- Main Site: `http://YOUR_IP:3000`
- API: `http://YOUR_IP:8000`
- API Docs: `http://YOUR_IP:8000/docs`

---

## Updates

To update to the latest version:

```bash
cd /opt/greenedumap
sudo ./scripts/deploy/update.sh
```

The update script will:
- ✅ Create automatic database backup
- ✅ Pull latest code
- ✅ Run migrations
- ✅ Rolling restart services (zero downtime)
- ✅ Auto-rollback on failure

---

## Useful Commands

### View Logs
```bash
cd /opt/greenedumap/infrastructure/docker
docker-compose logs -f                    # All services
docker-compose logs -f api-gateway        # Specific service
```

### Check Status
```bash
docker-compose ps
```

### Restart Service
```bash
docker-compose restart api-gateway
```

### Database Backup
```bash
docker-compose exec postgres pg_dump -U greenedumap greenedumap_prod > backup.sql
```

### Database Restore
```bash
docker-compose exec -T postgres psql -U greenedumap -d greenedumap_prod < backup.sql
```

---

## Troubleshooting

### Services not starting?
```bash
# Check logs
docker-compose logs

# Restart all services
docker-compose down
docker-compose up -d
```

### SSL certificate issues?
```bash
# Renew certificates manually
certbot renew

# Test renewal
certbot renew --dry-run
```

### Database connection issues?
```bash
# Check database is running
docker-compose ps postgres

# Check database logs
docker-compose logs postgres
```

---

## Security Checklist

After deployment, secure your VPS:

```bash
# 1. Setup firewall
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

# 2. Install fail2ban
apt-get install fail2ban
systemctl enable fail2ban

# 3. Disable root SSH login
sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
systemctl restart sshd

# 4. Setup automatic updates
apt-get install unattended-upgrades
dpkg-reconfigure -plow unattended-upgrades
```

---

## Credentials

Your deployment credentials are saved in:
```
/root/greenedumap-credentials.txt
```

**Keep this file secure!**

---

## Support

- Documentation: [GitHub Wiki]
- Issues: [GitHub Issues]
- Email: admin@greenedumap.com
