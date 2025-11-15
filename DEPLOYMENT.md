# Deployment Guide - MadSugu

This guide covers deploying MadSugu to production.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Environment Configuration](#environment-configuration)
- [Docker Deployment](#docker-deployment)
- [Manual Deployment](#manual-deployment)
- [Database Migration](#database-migration)
- [Security Checklist](#security-checklist)

## Prerequisites

### Minimum Server Requirements
- Ubuntu 20.04+ or similar Linux distribution
- 2 CPU cores
- 4GB RAM
- 20GB disk space
- PostgreSQL 15+
- Redis 7+

### Software Requirements
- Docker & Docker Compose
- Nginx (for reverse proxy)
- SSL certificate (Let's Encrypt recommended)

## Environment Configuration

### Backend Environment Variables

Create `backend/.env` file:

```env
# Database
DATABASE_URL=postgresql://user:password@db:5432/madsugu

# Security - IMPORTANT: Change these!
SECRET_KEY=generate-a-secure-random-key-here-minimum-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API
API_V1_STR=/api/v1
PROJECT_NAME=MadSugu
BACKEND_CORS_ORIGINS=["https://yourdomain.com"]

# File Storage
UPLOAD_DIR=/app/uploads
MAX_UPLOAD_SIZE=10485760

# Redis
REDIS_URL=redis://redis:6379/0

# Mobile Money (add when implementing)
ORANGE_MONEY_API_KEY=
MTN_MONEY_API_KEY=
MOOV_MONEY_API_KEY=

# Email (add when implementing)
SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
EMAILS_FROM_EMAIL=noreply@yourdomain.com
```

### Generate Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Docker Deployment

### 1. Create Production Docker Compose

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: madsugu_db_prod
    environment:
      POSTGRES_USER: ${DATABASE_USER}
      POSTGRES_PASSWORD: ${DATABASE_PASSWORD}
      POSTGRES_DB: ${DATABASE_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: madsugu_redis_prod
    volumes:
      - redis_data:/data
    restart: unless-stopped

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    container_name: madsugu_backend_prod
    env_file:
      - ./backend/.env
    volumes:
      - backend_uploads:/app/uploads
    depends_on:
      - db
      - redis
    restart: unless-stopped
    command: gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    container_name: madsugu_frontend_prod
    depends_on:
      - backend
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: madsugu_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - backend_uploads:/var/www/uploads
    depends_on:
      - backend
      - frontend
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  backend_uploads:
```

### 2. Create Production Dockerfile for Backend

`backend/Dockerfile.prod`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

RUN mkdir -p uploads

EXPOSE 8000

CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
```

### 3. Create Production Dockerfile for Frontend

`frontend/Dockerfile.prod`:

```dockerfile
FROM node:20-alpine as builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:20-alpine

WORKDIR /app

COPY --from=builder /app/build ./build
COPY --from=builder /app/package*.json ./

RUN npm ci --production

EXPOSE 3000

CMD ["node", "build"]
```

### 4. Nginx Configuration

Create `nginx/nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:3000;
    }

    server {
        listen 80;
        server_name yourdomain.com;

        # Redirect HTTP to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name yourdomain.com;

        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;

        # SSL configuration
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;

        # API
        location /api {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Uploads
        location /uploads {
            alias /var/www/uploads;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }

        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### 5. Deploy

```bash
# Build and start services
docker-compose -f docker-compose.prod.yml up -d --build

# Initialize database
docker-compose -f docker-compose.prod.yml exec backend python init_categories.py

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

## Manual Deployment

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt gunicorn

# Run with gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Frontend

```bash
cd frontend

# Install dependencies
npm ci

# Build
npm run build

# Run production server
node build
```

## Database Migration

### Backup Database

```bash
docker-compose exec db pg_dump -U postgres madsugu > backup.sql
```

### Restore Database

```bash
docker-compose exec -T db psql -U postgres madsugu < backup.sql
```

### Future: Alembic Migrations

```bash
# Generate migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Use strong database passwords
- [ ] Enable HTTPS with valid SSL certificate
- [ ] Configure firewall (allow only 80, 443, 22)
- [ ] Set up regular backups
- [ ] Configure CORS properly
- [ ] Enable rate limiting
- [ ] Set up monitoring and logging
- [ ] Keep dependencies updated
- [ ] Implement CSRF protection
- [ ] Use environment variables for secrets
- [ ] Set up fail2ban for SSH
- [ ] Configure PostgreSQL authentication
- [ ] Implement file upload size limits
- [ ] Validate all user inputs
- [ ] Set secure cookie flags

## Monitoring

### Health Checks

```bash
# Backend health
curl https://yourdomain.com/health

# Database connection
docker-compose exec db psql -U postgres -c "SELECT 1"
```

### Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
```

## Performance Optimization

1. **Enable Redis caching**
2. **Use CDN for static files**
3. **Compress images on upload**
4. **Enable Gzip compression in Nginx**
5. **Implement database indexing**
6. **Use connection pooling**
7. **Enable HTTP/2**

## Scaling

### Horizontal Scaling

1. Use a load balancer (HAProxy, AWS ELB)
2. Run multiple backend instances
3. Use managed PostgreSQL (AWS RDS, DigitalOcean)
4. Use managed Redis (AWS ElastiCache)
5. Store uploads in S3 or similar

### Vertical Scaling

1. Increase server resources
2. Optimize database queries
3. Add database read replicas
4. Implement caching strategy

## Troubleshooting

### Common Issues

**Backend won't start:**
- Check DATABASE_URL
- Verify PostgreSQL is running
- Check logs: `docker-compose logs backend`

**Frontend can't connect to backend:**
- Verify CORS settings
- Check API_V1_STR configuration
- Verify proxy settings in vite.config.js

**Images not uploading:**
- Check UPLOAD_DIR permissions
- Verify MAX_UPLOAD_SIZE
- Check disk space

## Support

For deployment issues:
1. Check logs first
2. Review this guide
3. Open an issue on GitHub
4. Contact support

## Updates

To update the application:

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up -d --build

# Run migrations (if any)
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

---

For questions or issues, please open an issue on GitHub.
