# Port Configuration

## Default Port: 8000

The Lyra Prompt Optimizer backend runs on port 8000 by default to avoid conflicts with macOS AirPlay Receiver (which uses port 5000).

## Custom Port Configuration

### Option 1: Environment Variable
```bash
export PORT=9000
python app.py
```

### Option 2: Command Line
```bash
PORT=9000 python app.py
```

### Option 3: .env File
Add to your `.env` file:
```
PORT=9000
```

## Frontend Updates

If you change the backend port, you must also update the frontend API URLs:

### Browser Extension
Edit `frontend/extension/popup.js`:
```javascript
this.apiUrl = 'http://localhost:YOUR_PORT';
```

And update `frontend/extension/manifest.json`:
```json
"host_permissions": [
  "http://localhost:YOUR_PORT/*"
]
```

### Web Application
Edit `frontend/webapp/script.js`:
```javascript
this.apiUrl = 'http://localhost:YOUR_PORT';
```

## Common Port Conflicts

- **5000**: macOS AirPlay Receiver
- **3000**: React development server
- **8080**: Many Java applications
- **8000**: Python development servers (our default)

## Alternative Ports
If 8000 is also busy, try:
- 8001
- 8888
- 9000
- 3001
