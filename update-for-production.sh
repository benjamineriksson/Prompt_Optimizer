#!/bin/bash

# Update Lyra Extension for Production
echo "🔄 Updating Lyra Extension for Production Deployment..."

# Get the production URL from user
echo "Enter your deployed backend URL (e.g., https://your-app.railway.app):"
read -p "Production URL: " PRODUCTION_URL

if [ -z "$PRODUCTION_URL" ]; then
    echo "❌ No URL provided. Exiting."
    exit 1
fi

# Remove trailing slash if present
PRODUCTION_URL=$(echo "$PRODUCTION_URL" | sed 's/\/$//')

echo "🔧 Updating API URLs to: $PRODUCTION_URL"

# Update extension
echo "  Updating extension popup.js..."
sed -i.bak "s|this\.apiUrl = 'http://localhost:8000';|this.apiUrl = '$PRODUCTION_URL';|g" frontend/extension/popup.js

# Update web app
echo "  Updating web app script.js..."
sed -i.bak "s|this\.apiUrl = 'http://localhost:8000';|this.apiUrl = '$PRODUCTION_URL';|g" frontend/webapp/script.js

# Update manifest host permissions
echo "  Updating manifest.json permissions..."
sed -i.bak "s|\"http://localhost:8000/\*\"|\"$PRODUCTION_URL/*\"|g" frontend/extension/manifest.json

# Create production package
echo "📦 Creating production extension package..."
cd frontend/extension
zip -r lyra-extension-production.zip . \
    -x "*.DS_Store" \
    -x "*.git*" \
    -x "README.md" \
    -x "icons/README.md" \
    -x "*.bak" \
    -x "lyra-extension*.zip"

if [ $? -eq 0 ]; then
    echo "✅ Production package created: frontend/extension/lyra-extension-production.zip"
    echo "   Size: $(du -h lyra-extension-production.zip | cut -f1)"
else
    echo "❌ Failed to create production package"
    exit 1
fi

cd ../..

echo ""
echo "🎉 Extension updated for production!"
echo ""
echo "📋 Next steps:"
echo "1. Test your backend at: $PRODUCTION_URL/health"
echo "2. Upload lyra-extension-production.zip to Chrome Web Store"
echo "3. Complete store listing"
echo ""
echo "🔄 To revert to development mode, run:"
echo "   git checkout frontend/extension/popup.js frontend/webapp/script.js frontend/extension/manifest.json"
