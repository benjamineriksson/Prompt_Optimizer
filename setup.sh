#!/bin/bash

# Lyra Prompt Optimizer Setup Script
# This script sets up the development environment and runs basic tests

set -e  # Exit on any error

echo "🚀 Setting up Lyra Prompt Optimizer..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "backend" ]; then
    echo "❌ Please run this script from the root directory of the Lyra project."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Set up backend
echo "📦 Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit backend/.env and add your DeepSeek API key!"
    echo "   DEEPSEEK_API_KEY=your_actual_api_key_here"
    echo ""
    read -p "Press Enter after you've added your API key to continue..."
fi

# Test backend setup
echo "🧪 Testing backend setup..."
python -c "
import sys
try:
    from flask import Flask
    from flask_cors import CORS
    import requests
    from dotenv import load_dotenv
    print('✅ All Python dependencies imported successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"

# Check if API key is set
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('DEEPSEEK_API_KEY')
if not api_key or api_key == 'your_deepseek_api_key_here':
    print('❌ Please set your DeepSeek API key in backend/.env')
    exit(1)
else:
    print('✅ API key found in environment')
"

echo "✅ Backend setup complete!"

# Return to root directory
cd ..

# Test frontend files
echo "🧪 Testing frontend files..."

# Check browser extension files
if [ -f "frontend/extension/manifest.json" ] && [ -f "frontend/extension/popup.html" ] && [ -f "frontend/extension/popup.js" ]; then
    echo "✅ Browser extension files found"
else
    echo "❌ Browser extension files missing"
    exit 1
fi

# Check web app files
if [ -f "frontend/webapp/index.html" ] && [ -f "frontend/webapp/script.js" ] && [ -f "frontend/webapp/styles.css" ]; then
    echo "✅ Web application files found"
else
    echo "❌ Web application files missing"
    exit 1
fi

echo ""
echo "🎉 Setup complete! Here's how to run the application:"
echo ""
echo "1. Start the backend server:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python app.py"
echo ""
echo "2. For browser extension:"
echo "   - Open Chrome and go to chrome://extensions/"
echo "   - Enable 'Developer mode'"
echo "   - Click 'Load unpacked' and select the 'frontend/extension' folder"
echo ""
echo "3. For web application:"
echo "   - Open 'frontend/webapp/index.html' in your browser"
echo "   - Make sure the backend server is running"
echo ""
echo "📖 For detailed instructions, see README.md and docs/deployment.md"
echo ""
echo "⚡ Quick test: Visit http://localhost:8000/health after starting the backend"
