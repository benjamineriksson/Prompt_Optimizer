# Chrome Web Store Publishing Guide - Prompt Optimizer

This guide will walk you through publishing your Prompt Optimizer extension to the Chrome Web Store.

## 🚀 Chrome Web Store (Recommended)

### Prerequisites
- Google account
- $5 one-time registration fee
- Completed and tested extension
- Store listing materials

### Step 1: Prepare Your Extension

#### 1.1 Create Icons (Required for Store)
You'll need to create these icon files in `frontend/extension/icons/`:
- `icon16.png` (16x16 pixels)
- `icon32.png` (32x32 pixels)  
- `icon48.png` (48x48 pixels)
- `icon128.png` (128x128 pixels)

**Quick icon creation options:**
- **AI Generation**: Use DALL-E, Midjourney, or Canva with prompt: "Simple purple gradient sparkle star icon for browser extension, minimalist design, transparent background"
- **Design Tools**: Figma, Adobe Illustrator, or even PowerPoint
- **Icon Libraries**: Find suitable icons on Flaticon, Icons8, or similar

#### 1.2 Update Manifest with Icons
```bash
cd /Users/benjamineriksson/Documents/GitHub/LYRA/frontend/extension
```

Update `manifest.json` to include icons:
```json
{
  "manifest_version": 3,
  "name": "Lyra Prompt Optimizer",
  "version": "1.0.0",
  "description": "Optimize your prompts using Lyra's 4-D methodology powered by DeepSeek AI",
  "icons": {
    "16": "icons/icon16.png",
    "32": "icons/icon32.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  },
  "action": {
    "default_popup": "popup.html",
    "default_title": "Lyra Prompt Optimizer",
    "default_icon": {
      "16": "icons/icon16.png",
      "32": "icons/icon32.png",
      "48": "icons/icon48.png",
      "128": "icons/icon128.png"
    }
  },
  "permissions": ["activeTab", "storage"],
  "host_permissions": ["http://localhost:8000/*", "https://api.deepseek.com/*"]
}
```

#### 1.3 Update for Production
Change the API URL in `popup.js` for production:
```javascript
// For production, change to your deployed backend URL
this.apiUrl = 'https://your-backend-domain.com';
// Or keep localhost for development version
```

#### 1.4 Create Package
```bash
cd frontend/extension
zip -r lyra-extension.zip . -x "*.DS_Store" "*.git*" "README.md"
```

### Step 2: Chrome Web Store Registration

1. **Visit Chrome Web Store Developer Dashboard**
   - Go to [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole)
   - Sign in with your Google account

2. **Pay Registration Fee**
   - One-time $5 fee required
   - Use Google Pay or credit card

3. **Register as Developer**
   - Fill out developer information
   - Verify your identity if required

### Step 3: Upload Extension

1. **Create New Item**
   - Click "Add new item"
   - Upload your `lyra-extension.zip` file
   - Wait for upload and initial validation

2. **Fill Store Listing**

#### Basic Information
- **Name**: Lyra Prompt Optimizer
- **Summary**: Transform vague prompts into clear, effective instructions using AI-powered 4-D methodology
- **Description**:
```
Lyra Prompt Optimizer helps you create better AI prompts using a proven 4-D methodology: Deconstruct, Diagnose, Develop, and Deliver.

✨ FEATURES:
• 4-D Methodology: Systematic approach to prompt optimization
• Two modes: BASIC (quick fixes) and DETAIL (comprehensive analysis)
• Multi-platform: Optimized for ChatGPT, Claude, Gemini, and other AI tools
• Real-time optimization powered by DeepSeek AI
• Copy-to-clipboard for easy use
• Clean, intuitive interface

🎯 HOW IT WORKS:
1. Enter your rough prompt
2. Choose optimization style (BASIC or DETAIL)
3. Select your target AI platform
4. Get professionally optimized prompts instantly

🔧 PERFECT FOR:
• Content creators seeking better AI outputs
• Developers writing technical prompts
• Marketers crafting campaign content
• Students and researchers
• Anyone using AI tools regularly

Transform your AI interactions today with Lyra's proven methodology!
```

#### Store Assets (Required)
- **Icon**: 128x128 PNG (your icon128.png)
- **Screenshots**: 1280x800 or 640x400 pixels (create 3-5 screenshots)
- **Promotional tile**: 440x280 PNG (optional but recommended)

#### Screenshots to Create
1. Extension popup with sample prompt
2. Optimization in progress
3. Results display with improvements
4. Settings/options view
5. Before/after comparison

#### Categories and Tags
- **Category**: Productivity
- **Additional categories**: Developer Tools, Communication
- **Keywords**: prompt, AI, optimization, ChatGPT, productivity, writing

#### Privacy and Permissions
- **Host permissions**: Explain why you need localhost and DeepSeek API access
- **Privacy policy**: Create a simple privacy policy (see template below)

### Step 4: Privacy Policy (Required)

Create a simple privacy policy:

```
LYRA PROMPT OPTIMIZER - PRIVACY POLICY

Data Collection:
- We collect prompts you choose to optimize for processing
- No personal information is stored permanently
- API calls are made to DeepSeek for optimization processing

Data Use:
- Prompts are sent to DeepSeek API for optimization only
- No data is sold or shared with third parties
- Optimization history is stored locally on your device

Data Storage:
- Local storage only (browser extension storage)
- No cloud storage of personal data
- You can clear data anytime through browser settings

Third-Party Services:
- DeepSeek API for prompt optimization
- Subject to DeepSeek's privacy policy

Contact: [your-email@domain.com]
Last Updated: [current-date]
```

### Step 5: Review and Publish

1. **Submit for Review**
   - Review all information
   - Submit for Chrome Web Store review
   - Review typically takes 1-3 business days

2. **Monitor Review Status**
   - Check developer dashboard for updates
   - Respond to any reviewer feedback
   - Make requested changes if needed

3. **Publication**
   - Once approved, extension goes live
   - Users can find and install it from Chrome Web Store

## 🦊 Firefox Add-ons (AMO)

### Step 1: Prepare for Firefox
1. **Update Manifest for Firefox**
   - Firefox uses Manifest V2 or V3
   - May need slight modifications

2. **Test in Firefox**
   - Load extension in Firefox Developer Mode
   - Ensure all functionality works

### Step 2: Submit to AMO
1. **Create Mozilla Account**
   - Go to [addons.mozilla.org](https://addons.mozilla.org/developers/)
   - Create developer account (free)

2. **Upload Extension**
   - Create new submission
   - Upload extension package
   - Fill out listing information

3. **Review Process**
   - Mozilla reviews all extensions
   - May take 1-2 weeks
   - Automated and manual review

## 🔒 Production Considerations

### Backend Deployment
Before publishing, deploy your backend:

1. **Choose Hosting Platform**
   - Heroku (easy, free tier available)
   - Railway (modern, simple)
   - DigitalOcean App Platform
   - AWS/Google Cloud

2. **Update Extension API URL**
   - Change from localhost to production URL
   - Update manifest host_permissions

3. **SSL Certificate**
   - Ensure HTTPS for production backend
   - Required for extension security

### Security Updates
- Remove localhost permissions for production
- Add only necessary host permissions
- Implement proper error handling
- Add rate limiting if needed

## 📊 Post-Publication

### Monitor Performance
- Track installation numbers
- Monitor user reviews
- Check error reports
- Update as needed

### Marketing
- Share on social media
- Write blog posts about the tool
- Engage with AI/productivity communities
- Consider Product Hunt launch

### Updates
- Regular updates for new features
- Bug fixes based on user feedback
- Keep up with browser API changes
- Monitor extension store policies

## 🛠️ Development Version vs Production

### Development Version
- Uses localhost:8000
- Full debugging enabled
- Quick iteration and testing

### Production Version
- Uses production backend URL
- Optimized and minified
- Error reporting
- Analytics (optional)

## 📝 Checklist Before Publishing

- [ ] Icons created (16, 32, 48, 128px)
- [ ] Extension tested thoroughly
- [ ] Screenshots created
- [ ] Store description written
- [ ] Privacy policy created
- [ ] Backend deployed to production
- [ ] API URL updated for production
- [ ] Extension package created
- [ ] Developer account registered
- [ ] Store listing completed

## 💡 Pro Tips

1. **Start with Chrome Web Store** - Largest user base
2. **Create compelling screenshots** - Visual appeal matters
3. **Write clear description** - Focus on benefits, not features  
4. **Respond to reviews** - Shows active development
5. **Regular updates** - Improves store ranking
6. **Monitor analytics** - Understand user behavior

Your Lyra Prompt Optimizer is ready for the world! 🚀
