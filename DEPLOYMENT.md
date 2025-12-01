# VNPT Data Analysis Platform - Deployment Guide

## 🚀 Local Development

### Prerequisites
- Python 3.8+
- pip

### Setup

```bash
# 1. Install dependencies
pip install -r requirements_streamlit.txt

# 2. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## ☁️ Deploy to Hugging Face Spaces

### Step 1: Create Hugging Face Account
1. Go to https://huggingface.co/
2. Sign up for free account
3. Verify email

### Step 2: Create New Space
1. Click "New Space" button
2. Fill in details:
   - **Name**: `vnpt-data-analysis`
   - **License**: Apache 2.0
   - **SDK**: Streamlit
   - **Hardware**: CPU basic (free)

### Step 3: Upload Files

Upload these files to your Space:
```
app.py
pages/
├── 1_📊_Data_Exploration.py
├── 2_🧹_Data_Cleaning.py
├── 3_📈_Statistical_Analysis.py
└── 4_📉_Visualization.py
data_cleaner.py
statistical_analyzer.py
config.yaml
requirements_streamlit.txt
.streamlit/
└── config.toml
```

### Step 4: Auto-Deploy
- Hugging Face will automatically detect Streamlit
- Build process starts automatically
- App will be live at: `https://huggingface.co/spaces/YOUR_USERNAME/vnpt-data-analysis`

---

## 🔧 Alternative: Streamlit Community Cloud

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_GITHUB_REPO
git push -u origin main
```

### Step 2: Deploy
1. Go to https://streamlit.io/cloud
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file: `app.py`
6. Click "Deploy"

---

## 📦 Required Files

### requirements_streamlit.txt
```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.14.0
openpyxl>=3.1.0
matplotlib>=3.7.0
seaborn>=0.12.0
pyyaml>=6.0
```

### .streamlit/config.toml
```toml
[theme]
primaryColor = "#0066B2"  # VNPT Blue
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

---

## 🎯 Features

- ✅ Interactive data upload
- ✅ Step-by-step workflow
- ✅ Real-time data cleaning
- ✅ Statistical analysis
- ✅ Interactive visualizations
- ✅ VNPT branding
- ✅ Mobile responsive

---

## 🔒 Security Notes

- Max upload size: 200MB
- XSRF protection enabled
- No sensitive data stored
- Session-based state management

---

## 📞 Support

For issues or questions:
- Check Streamlit docs: https://docs.streamlit.io
- Hugging Face docs: https://huggingface.co/docs/hub/spaces

---

## 📄 License

Internal use only - VNPT Corporation
