# 🚀 Prompt Optimizer - Quick Start Guide

Get your Prompt Optimizer running in minutes!

## Prerequisites

- Python 3.8 or higher
- DeepSeek API key ([Get one here](https://platform.deepseek.com/))
- Modern web browser (Chrome, Firefox, Edge, Safari)

## 🚀 Quick Setup (Automated)

Run the setup script:
```bash
./setup.sh
```

Follow the prompts to configure your API key and test the installation.

## 🛠️ Manual Setup

### 1. Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env file and add your DeepSeek API key:
# DEEPSEEK_API_KEY=your_actual_api_key_here
```

### 2. Start Backend Server

```bash
# From the backend directory
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:8000
 * Press CTRL+C to quit
```

### 3. Test Backend

Open a new terminal and test:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "api_accessible": true
}
```

## 🎯 Choose Your Frontend

### Option A: Browser Extension

1. **Open Extension Management**
   - Chrome: `chrome://extensions/`
   - Edge: `edge://extensions/`
   - Firefox: `about:debugging`

2. **Enable Developer Mode** (Chrome/Edge)

3. **Load Extension**
   - Click "Load unpacked"
   - Select the `frontend/extension/` folder
   - Extension icon should appear in toolbar

4. **Test Extension**
   - Click the Lyra icon in browser toolbar
   - Enter a test prompt
   - Click "Optimize Prompt"

### Option B: Web Application

1. **Open Web App**
   ```bash
   # From project root, open in browser:
   open frontend/webapp/index.html
   # Or simply double-click the file
   ```

2. **Test Web App**
   - Enter a test prompt
   - Select optimization style
   - Click "Optimize My Prompt"

## 📝 First Test

Try optimizing this sample prompt:

**Input:**
```
Write a marketing email for my new product
```

**Settings:**
- Style: BASIC
- Target AI: ChatGPT

**Expected Result:**
You should receive an optimized prompt with specific instructions, context, and structure improvements.

## ✅ Verification Checklist

- [ ] Backend server running on http://localhost:8000
- [ ] Health check returns "healthy" status
- [ ] Frontend interface loads without errors
- [ ] Can submit and receive optimized prompts
- [ ] Copy functionality works
- [ ] Error handling displays appropriately

## 🔧 Troubleshooting

### Common Issues

**"Backend offline" error:**
- Ensure backend server is running
- Check if port 8000 is available (or set custom port with `PORT=9000 python app.py`)
- Verify API key is correctly set in .env

**CORS errors in browser:**
- Make sure backend is running
- Check that frontend is accessing correct API URL
- Verify CORS_ORIGINS setting in config.py

**Extension not loading:**
- Refresh extension in browser
- Check browser console for errors
- Ensure all required files are present
- **Icon errors**: The extension will work without custom icons (uses browser default)

**Missing icons error:**
- Extension works fine without custom icons
- To add custom icons later, create 16x16, 32x32, 48x48, and 128x128 PNG files in `frontend/extension/icons/`
- For now, the extension uses browser default icons

**API key errors:**
- Verify API key is valid and active
- Check DeepSeek account status
- Ensure .env file is in backend directory

### Getting Help

1. **Check Logs**: Backend console shows detailed error messages
2. **Browser Console**: Press F12 to check for frontend errors
3. **API Testing**: Use curl or Postman to test endpoints directly
4. **Documentation**: See `docs/` folder for detailed guides

## 🎉 Next Steps

Once everything is working:

1. **Customize**: Modify the frontend styling to match your preferences
2. **Deploy**: Follow `docs/deployment.md` for production setup
3. **Extend**: Add new features or integrate with other tools
4. **Share**: Package the extension for others to use

## 📚 Additional Resources

- **Full Documentation**: `README.md`
- **Architecture Guide**: `docs/architecture.md`
- **Deployment Guide**: `docs/deployment.md`
- **DeepSeek API Docs**: [platform.deepseek.com/docs](https://platform.deepseek.com/docs)

## 💡 Usage Tips

### Best Prompts for Optimization
- **Good**: Specific but unclear prompts needing structure
- **Examples**: 
  - "Create a workout plan"
  - "Help me write code"
  - "Generate content for social media"

### Optimization Styles
- **BASIC**: Use for simple prompts, quick improvements
- **DETAIL**: Use for complex tasks requiring thorough analysis

### Target AI Selection
- Choose the AI platform you'll actually use
- Different platforms have different strengths
- Optimization techniques are tailored accordingly

---

🎯 **Goal**: Transform vague prompts into clear, effective instructions that get better AI results!

Happy optimizing with Lyra! ✨
