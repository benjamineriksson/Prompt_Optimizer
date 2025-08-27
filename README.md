# Prompt Optimizer

A self-contained prompt optimization addon that uses the 4-D methodology to enhance prompts for AI interactions.

The Prompt Optimizer implements a proven 4-D methodology for prompt enhancement:

## Features

- **4-D Methodology**: Deconstruct, Diagnose, Develop, Deliver
- **Two Optimization Modes**: BASIC (quick fix) and DETAIL (comprehensive)
- **Multi-Platform Support**: Browser extension and standalone web app
- **AI Target Optimization**: Tailored for ChatGPT, Claude, Gemini, or Other
- **Real-time Processing**: Direct integration with DeepSeek API

## Architecture

### Backend (Python Flask)
- RESTful API endpoints
- DeepSeek API integration
- 4-D methodology implementation
- Secure API key management

### Frontend Options
1. **Browser Extension**: Popup interface with manifest v3 support
2. **Web Application**: Standalone responsive web interface

## Quick Start

### Backend Setup
```bash
pip install -r requirements.txt
export DEEPSEEK_API_KEY="your_api_key_here"
python app.py
```

### Browser Extension
1. Open Chrome/Edge extensions page
2. Enable Developer mode
3. Load unpacked extension from `frontend/extension/` folder

### Web App
1. Open `frontend/webapp/index.html` in browser
2. Ensure backend is running on http://localhost:8000

## Project Structure

```
Prompt_Optimizer/
├── app.py                  # Flask server
├── optimizer.py            # Core optimization logic
├── requirements.txt        # Python dependencies
├── config.py              # Configuration settings
├── Procfile               # Railway/Heroku deployment
├── railway.toml           # Railway configuration
├── frontend/
│   ├── extension/         # Browser extension
│   │   ├── manifest.json
│   │   ├── popup.html
│   │   ├── popup.js
│   │   └── styles.css
│   └── webapp/           # Standalone web app
│       ├── index.html
│       ├── script.js
│       └── styles.css
├── docs/
│   └── deployment.md     # Deployment guide
└── README.md
```

## Configuration

Create a `.env` file in the root directory:
```
DEEPSEEK_API_KEY=your_deepseek_api_key_here
FLASK_ENV=development
CORS_ORIGINS=*
```

## API Endpoints

### POST /optimize
Optimizes a prompt using the 4-D methodology.

**Request Body:**
```json
{
  "raw_prompt": "string",
  "prompt_style": "BASIC|DETAIL",
  "target_ai": "ChatGPT|Claude|Gemini|Other"
}
```

**Response:**
```json
{
  "optimized_prompt": "string",
  "improvements": ["string"],
  "techniques_applied": ["string"],
  "pro_tip": "string"
}
```

## Development

### Backend Development
- Flask with CORS support
- Environment-based configuration
- Comprehensive error handling
- Rate limiting and security measures

### Frontend Development
- Vanilla JavaScript for compatibility
- Responsive CSS design
- Clean, intuitive user interface
- Real-time API communication

## Deployment

See `docs/deployment.md` for detailed deployment instructions for both local development and production environments.

## License

MIT License - see LICENSE file for details.
