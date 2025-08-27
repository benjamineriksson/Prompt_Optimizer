# Deployment Guide - Lyra Prompt Optimizer

This guide covers deployment options for both the backend API and frontend interfaces.

## Backend Deployment

### Local Development

1. **Setup Environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your DeepSeek API key
   ```

3. **Run Development Server**
   ```bash
   python app.py
   ```
   Server will run on `http://localhost:8000`

### Production Deployment

#### Option 1: Using Gunicorn (Recommended)

1. **Install Gunicorn** (already in requirements.txt)

2. **Run with Gunicorn**
   ```bash
   gunicorn --bind 0.0.0.0:8000 --workers 4 app:app
   ```

3. **Systemd Service** (Linux)
   Create `/etc/systemd/system/lyra-api.service`:
   ```ini
   [Unit]
   Description=Lyra Prompt Optimizer API
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/path/to/LYRA/backend
   Environment=PATH=/path/to/LYRA/backend/venv/bin
   ExecStart=/path/to/LYRA/backend/venv/bin/gunicorn --bind 0.0.0.0:8000 --workers 4 app:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Enable and start:
   ```bash
   sudo systemctl enable lyra-api
   sudo systemctl start lyra-api
   ```

#### Option 2: Docker Deployment

1. **Create Dockerfile** (backend/Dockerfile):
   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 5000

   CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
   ```

2. **Build and Run**
   ```bash
   docker build -t lyra-api .
   docker run -d -p 8000:8000 --env-file .env lyra-api
   ```

#### Option 3: Cloud Deployment

**Heroku:**
1. Create `Procfile` in backend directory:
   ```
   web: gunicorn app:app
   ```

2. Deploy:
   ```bash
   heroku create your-lyra-api
   heroku config:set DEEPSEEK_API_KEY=your_key_here
   git push heroku main
   ```

**Railway/Render:**
- Connect GitHub repository
- Set environment variables in dashboard
- Deploy automatically

### Reverse Proxy (Nginx)

For production, use Nginx as a reverse proxy:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Frontend Deployment

### Browser Extension

#### Development Testing
1. **Chrome/Edge:**
   - Open `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked"
   - Select `frontend/extension/` folder

2. **Firefox:**
   - Open `about:debugging`
   - Click "This Firefox"
   - Click "Load Temporary Add-on"
   - Select `manifest.json` from `frontend/extension/`

#### Production Release

1. **Prepare for Store**
   - Create icons (16x16, 32x32, 48x48, 128x128 px)
   - Update `manifest.json` with final details
   - Test thoroughly
   - Prepare store listing materials

2. **Chrome Web Store**
   - Register developer account ($5 fee)
   - Upload extension package (.zip)
   - Fill store listing
   - Submit for review

3. **Firefox Add-ons**
   - Create Mozilla developer account
   - Upload .zip file to AMO
   - Complete listing information
   - Submit for review

#### Extension Packaging
```bash
cd frontend/extension
zip -r lyra-extension.zip . -x "*.DS_Store" "*.git*"
```

### Web Application

#### Static Hosting
For the standalone web app:

1. **GitHub Pages**
   - Push to GitHub repository
   - Enable Pages in repository settings
   - Select branch and folder

2. **Netlify**
   - Connect GitHub repository
   - Deploy from `frontend/webapp/` folder
   - Set up custom domain if needed

3. **Vercel**
   - Import GitHub repository
   - Configure build settings
   - Deploy automatically

#### Custom Server
```nginx
server {
    listen 80;
    server_name your-webapp-domain.com;
    root /path/to/LYRA/frontend/webapp;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy to backend
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Configuration for Production

### CORS Settings
Update backend `config.py` for production:
```python
CORS_ORIGINS = "https://your-domain.com,chrome-extension://your-extension-id"
```

### API Key Security
- Never commit API keys to version control
- Use environment variables or secret management services
- Rotate keys regularly
- Monitor API usage

### Rate Limiting
Consider implementing additional rate limiting:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)
```

### SSL/HTTPS
For production, always use HTTPS:
- Obtain SSL certificates (Let's Encrypt for free)
- Configure Nginx with SSL
- Update all API calls to use HTTPS

### Monitoring and Logging

1. **Application Monitoring**
   ```python
   import logging
   
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
       handlers=[
           logging.FileHandler('lyra.log'),
           logging.StreamHandler()
       ]
   )
   ```

2. **Health Checks**
   - Monitor `/health` endpoint
   - Set up alerts for API failures
   - Track response times

### Backup and Recovery
- Regular database backups (if applicable)
- Configuration file backups
- API key secure storage
- Disaster recovery plan

## Performance Optimization

### Backend
- Use connection pooling for API calls
- Implement response caching where appropriate
- Monitor memory usage
- Scale horizontally with multiple workers

### Frontend
- Minify CSS and JavaScript
- Optimize images
- Use CDN for static assets
- Implement service workers for offline functionality

## Security Considerations

1. **API Security**
   - Input validation and sanitization
   - Rate limiting per IP
   - CORS configuration
   - API key rotation

2. **Frontend Security**
   - Content Security Policy (CSP)
   - Secure cookie handling
   - XSS prevention
   - Data encryption for sensitive information

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Check CORS_ORIGINS configuration
   - Verify frontend URL matches allowed origins

2. **API Key Issues**
   - Verify environment variable is set
   - Check API key validity with DeepSeek

3. **Rate Limiting**
   - Monitor API usage
   - Implement exponential backoff
   - Consider upgrading API plan

4. **Extension Issues**
   - Check manifest permissions
   - Verify host permissions for API calls
   - Test in different browsers

### Monitoring Commands
```bash
# Check application logs
tail -f /var/log/lyra/app.log

# Monitor system resources
htop

# Check API health
curl -X GET http://localhost:8000/health

# Test optimization endpoint
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{"raw_prompt":"test","prompt_style":"BASIC","target_ai":"ChatGPT"}'
```

## Scaling Considerations

### Horizontal Scaling
- Use load balancer (Nginx, HAProxy)
- Deploy multiple backend instances
- Implement session affinity if needed

### Database Scaling
- If adding persistent storage
- Read replicas for better performance
- Caching layer (Redis)

### CDN Integration
- Serve static assets from CDN
- Cache API responses where appropriate
- Geographic distribution

This deployment guide ensures your Lyra Prompt Optimizer can be successfully deployed in various environments while maintaining security, performance, and reliability.
