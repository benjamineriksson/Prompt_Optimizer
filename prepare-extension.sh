#!/bin/bash

# Lyra Extension Publishing Preparation Script
echo "🚀 Preparing Lyra Prompt Optimizer for Chrome Web Store..."

cd "$(dirname "$0")"

# Check if we're in the right directory
if [ ! -d "frontend/extension" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

cd frontend/extension

echo "📋 Pre-publishing checklist:"
echo ""

# Check for required files
echo "✅ Checking required files..."
required_files=("manifest.json" "popup.html" "popup.js" "styles.css")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file exists"
    else
        echo "  ❌ $file missing"
        exit 1
    fi
done

# Check for icons
echo ""
echo "🎨 Checking icons..."
icon_sizes=(16 32 48 128)
icons_missing=false

for size in "${icon_sizes[@]}"; do
    icon_file="icons/icon${size}.png"
    if [ -f "$icon_file" ]; then
        echo "  ✓ icon${size}.png exists"
    else
        echo "  ⚠️  icon${size}.png missing (required for store)"
        icons_missing=true
    fi
done

if [ "$icons_missing" = true ]; then
    echo ""
    echo "📝 ICONS NEEDED:"
    echo "   Create these icon files before publishing:"
    echo "   - icons/icon16.png (16x16 pixels)"
    echo "   - icons/icon32.png (32x32 pixels)"
    echo "   - icons/icon48.png (48x48 pixels)"
    echo "   - icons/icon128.png (128x128 pixels)"
    echo ""
    echo "   💡 Quick solution:"
    echo "   - Use DALL-E, Canva, or Figma"
    echo "   - Search for 'sparkle star icon purple gradient'"
    echo "   - Make background transparent"
    echo ""
    read -p "Continue without icons? Extension will work but can't be published to store (y/n): " continue_without_icons
    if [ "$continue_without_icons" != "y" ]; then
        echo "Please create icons first, then run this script again."
        exit 1
    fi
fi

# Check API URL
echo ""
echo "🌐 Checking API configuration..."
if grep -q "localhost:8000" popup.js; then
    echo "  ⚠️  Using localhost API URL (development mode)"
    echo "     For production, update popup.js with your deployed backend URL"
    echo "     Example: this.apiUrl = 'https://your-backend.herokuapp.com';"
else
    echo "  ✓ Production API URL configured"
fi

# Check manifest version
echo ""
echo "📦 Extension info:"
name=$(grep '"name"' manifest.json | cut -d'"' -f4)
version=$(grep '"version"' manifest.json | cut -d'"' -f4)
echo "  Name: $name"
echo "  Version: $version"

# Create package
echo ""
echo "📦 Creating extension package..."

# Remove old package if exists
[ -f "lyra-extension.zip" ] && rm lyra-extension.zip

# Create package excluding development files
zip -r lyra-extension.zip . \
    -x "*.DS_Store" \
    -x "*.git*" \
    -x "README.md" \
    -x "icons/README.md" \
    -x "lyra-extension.zip"

if [ $? -eq 0 ]; then
    echo "  ✅ Package created: lyra-extension.zip"
    echo "     Size: $(du -h lyra-extension.zip | cut -f1)"
else
    echo "  ❌ Failed to create package"
    exit 1
fi

echo ""
echo "🎉 Publishing preparation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Create icons if missing (see docs/publishing-guide.md)"
echo "2. Deploy backend to production (if not done already)"
echo "3. Update API URL in popup.js for production"
echo "4. Re-run this script to create final package"
echo "5. Go to Chrome Web Store Developer Dashboard"
echo "6. Upload lyra-extension.zip"
echo "7. Complete store listing (see publishing-guide.md for details)"
echo ""
echo "📚 Full guide: docs/publishing-guide.md"
echo "🌐 Chrome Web Store: https://chrome.google.com/webstore/devconsole"
echo ""
echo "Good luck! 🚀"
