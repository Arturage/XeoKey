# Deployment Guide

Complete guide for deploying XeoKey to production.

## Pre-Deployment Checklist

- [ ] All environment variables configured
- [ ] Strong `SESSION_SECRET` generated (32+ characters)
- [ ] Strong `ENCRYPTION_KEY` generated
- [ ] MongoDB configured and accessible
- [ ] HTTPS certificate obtained
- [ ] Reverse proxy configured (if using)
- [ ] Firewall rules configured
- [ ] Backup strategy in place
- [ ] Monitoring set up
- [ ] Log rotation configured

## Environment Setup

### 1. Set All Environment Variables

Create a `.env` file or set system environment variables:

```env
NODE_ENV=production
PORT=3000
SESSION_SECRET=<strong-random-32-char-key>
ENCRYPTION_KEY=<strong-random-key>
MONGODB_URI=<your-mongodb-connection-string>
```

**Important**: Generate strong random keys for production. See [Configuration Guide](./CONFIGURATION.md) for key generation.

### 2. Use HTTPS

HTTPS is required for secure cookies and encrypted communication.

#### Option A: Reverse Proxy (Recommended)

Use nginx, Caddy, or another reverse proxy:

**nginx example:**
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Caddy example:**
```
your-domain.com {
    reverse_proxy localhost:3000
}
```

#### Option B: Direct HTTPS

Configure Bun to use HTTPS directly (requires SSL certificates).

### 3. Database Security

#### MongoDB Authentication

Enable authentication in MongoDB:

```javascript
use admin
db.createUser({
  user: "xeokey",
  pwd: "strong-password",
  roles: [ { role: "readWrite", db: "XeoKey" } ]
})
```

Update `MONGODB_URI`:
```
MONGODB_URI=mongodb://xeokey:strong-password@localhost:27017/XeoKey
```

#### Network Restrictions

- Restrict MongoDB to localhost or private network
- Use firewall rules to limit access
- Use VPN for remote database access

#### Encryption at Rest

Enable MongoDB encryption at rest for sensitive data.

## Deployment Methods

### Method 1: Direct Deployment

1. **Install dependencies:**
   ```bash
   bun install
   ```

2. **Set environment variables**

3. **Start the server:**
   ```bash
   bun run start
   ```

4. **Use process manager** (recommended):
   ```bash
   # Using PM2
   pm2 start bun --name xeokey -- run start

   # Using systemd (Linux)
   # Create /etc/systemd/system/xeokey.service
   ```

### Method 2: Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM oven/bun:latest

WORKDIR /app

COPY package.json bun.lock ./
RUN bun install

COPY . .

EXPOSE 3000

CMD ["bun", "run", "start"]
```

Build and run:
```bash
docker build -t xeokey .
docker run -d -p 3000:3000 --env-file .env xeokey
```

### Method 3: Cloud Platform

#### Vercel / Netlify
Not recommended for this application (requires persistent server).

#### Railway / Render
1. Connect your repository
2. Set environment variables
3. Configure build command: `bun install`
4. Configure start command: `bun run start`

#### DigitalOcean / AWS / GCP
1. Create a VM instance
2. Install Bun
3. Clone repository
4. Set environment variables
5. Use process manager (PM2, systemd)
6. Configure reverse proxy

## Process Management

### Using PM2

```bash
# Install PM2
npm install -g pm2

# Start application
pm2 start bun --name xeokey -- run start

# Save PM2 configuration
pm2 save

# Set up PM2 to start on boot
pm2 startup
```

### Using systemd (Linux)

Create `/etc/systemd/system/xeokey.service`:

```ini
[Unit]
Description=XeoKey Password Manager
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/XeoKey
Environment="NODE_ENV=production"
EnvironmentFile=/path/to/.env
ExecStart=/usr/local/bin/bun run start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable xeokey
sudo systemctl start xeokey
```

## Monitoring

### Log Monitoring

1. **Check logs regularly:**
   ```bash
   tail -f logs/server.log
   ```

2. **Set up log rotation:**
   ```bash
   # Using logrotate
   /path/to/XeoKey/logs/*.log {
       daily
       rotate 7
       compress
       missingok
       notifempty
   }
   ```

3. **Monitor for errors:**
   ```bash
   grep -i error logs/server.log
   ```

### Health Checks

Monitor the `/api/status` endpoint:
```bash
curl http://localhost:3000/api/status
```

### Uptime Monitoring

Use services like:
- UptimeRobot
- Pingdom
- StatusCake

## Backup Strategy

### MongoDB Backups

1. **Regular backups:**
   ```bash
   mongodump --uri="mongodb://localhost:27017" --out=/backup/path
   ```

2. **Automated backups:**
   ```bash
   # Add to crontab
   0 2 * * * mongodump --uri="mongodb://localhost:27017" --out=/backup/path/$(date +\%Y-\%m-\%d)
   ```

3. **Backup encryption keys:**
   - Store `SESSION_SECRET` and `ENCRYPTION_KEY` securely
   - Use secrets management (HashiCorp Vault, AWS Secrets Manager)
   - Never store keys in backups

4. **Test restore procedures:**
   ```bash
   mongorestore --uri="mongodb://localhost:27017" /backup/path
   ```

## Performance Optimization

1. **Enable gzip compression** (in reverse proxy)
2. **Use CDN** for static assets (if applicable)
3. **Optimize MongoDB indexes**
4. **Monitor database performance**
5. **Use connection pooling**

## Security Hardening

1. **Firewall rules:**
   - Only allow necessary ports (80, 443)
   - Restrict MongoDB port (27017) to localhost

2. **Keep dependencies updated:**
   ```bash
   bun update
   ```

3. **Regular security audits:**
   - Review logs for suspicious activity
   - Monitor failed login attempts
   - Check for unusual patterns

4. **SSL/TLS configuration:**
   - Use strong cipher suites
   - Enable HSTS
   - Use TLS 1.2 or higher

## Troubleshooting

See the [Troubleshooting Guide](./TROUBLESHOOTING.md) for common deployment issues.

## Post-Deployment

1. **Verify functionality:**
   - Test login/registration
   - Test password creation
   - Test password retrieval
   - Check analytics dashboard

2. **Monitor logs:**
   - Check for errors
   - Verify database connections
   - Monitor performance

3. **Set up alerts:**
   - Server downtime
   - Database connection failures
   - High error rates

## Maintenance

### Regular Tasks

- [ ] Review logs weekly
- [ ] Check for updates monthly
- [ ] Test backups monthly
- [ ] Review security settings quarterly
- [ ] Rotate keys annually (or as needed)

### Updates

1. **Pull latest changes:**
   ```bash
   git pull
   ```

2. **Update dependencies:**
   ```bash
   bun install
   ```

3. **Restart server:**
   ```bash
   pm2 restart xeokey
   # or
   sudo systemctl restart xeokey
   ```

## Additional Resources

- [Configuration Guide](./CONFIGURATION.md)
- [Security Guide](./SECURITY.md)
- [Troubleshooting Guide](./TROUBLESHOOTING.md)

