# Deployment Guide - Streamlit Cloud

## 🚀 Quick Deploy to Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at share.streamlit.io)

### Step 1: Prepare Repository

1. **Initialize Git** (if not done):
```bash
git init
git add .
git commit -m "Initial commit - VNPT HRDC Data Analysis Platform"
```

2. **Create GitHub Repository**:
- Go to github.com
- Create new repository: `vnpt-hrdc-data-analysis`
- Don't initialize with README (we have one)

3. **Push to GitHub**:
```bash
git remote add origin https://github.com/YOUR_USERNAME/vnpt-hrdc-data-analysis.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**:
   - Visit: https://share.streamlit.io
   - Sign in with GitHub

2. **Create New App**:
   - Click "New app"
   - Select your repository: `vnpt-hrdc-data-analysis`
   - Main file path: `app.py`
   - Click "Deploy"

3. **Wait for Deployment**:
   - Takes 2-5 minutes
   - Streamlit will install dependencies from `requirements_streamlit.txt`
   - App will auto-start

### Step 3: Configure (Optional)

**Secrets** (if needed):
- Go to App settings → Secrets
- Add any API keys or sensitive data

**Custom Domain** (paid plan):
- Settings → General → Custom subdomain

### Step 4: Share

Your app will be live at:
```
https://YOUR_USERNAME-vnpt-hrdc-data-analysis-app-xxxxx.streamlit.app
```

## 📋 Checklist Before Deploy

- ✅ All files committed to Git
- ✅ `requirements_streamlit.txt` is complete
- ✅ `.streamlit/config.toml` is included
- ✅ No sensitive data in code
- ✅ Sample data (if needed) is in repo
- ✅ README.md is updated

## 🔧 Troubleshooting

### App won't start
- Check logs in Streamlit Cloud dashboard
- Verify all dependencies in requirements.txt
- Check Python version compatibility

### Missing files
- Ensure all `.py` files are committed
- Check `.streamlit/config.toml` exists
- Verify `pages/` folder structure

### Performance issues
- Streamlit Cloud free tier: 1GB RAM
- Optimize data loading
- Use caching (`@st.cache_data`)

## 🔄 Update Deployed App

```bash
# Make changes locally
git add .
git commit -m "Update: description"
git push

# Streamlit Cloud auto-redeploys
```

## 🌐 Alternative: Hugging Face Spaces

1. Create Space at huggingface.co/spaces
2. Select Streamlit SDK
3. Upload files or connect Git
4. Auto-deploy

## 📞 Support

Issues? Contact VNPT HRDC Portal Team

---

**Ready to deploy!** 🚀
