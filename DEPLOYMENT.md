# 🚀 Deployment Guide - Live Demo URLs for Your Resume

This guide will help you deploy the Procurement Intelligence Platform to get **live demo URLs** you can put on your resume.

## 📋 Overview

You'll deploy two services:
1. **FastAPI Backend** on Render (free tier)
2. **Streamlit Dashboard** on Streamlit Cloud (free tier)

**Time required**: ~15 minutes  
**Cost**: FREE  
**Result**: Live URLs you can share on your resume

---

## Step 1: Push to GitHub

Before deploying, push your code to a GitHub repository:

```bash
# Initialize git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Procurement Intelligence Platform"

# Create GitHub repo and push
git remote add origin https://github.com/YOUR_USERNAME/procurement-intelligence-platform.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy FastAPI Backend on Render

### Option A: Using render.yaml (Recommended)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New" → "Blueprint"
3. Connect your GitHub repository
4. Select the `render.yaml` file
5. Click "Apply"
6. Wait for deployment (2-3 minutes)

**Your API will be live at**: `https://procurement-api-XXXX.onrender.com`

### Option B: Manual Deployment

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `procurement-api`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free
5. Click "Create Web Service"
6. Wait for deployment

---

## Step 3: Deploy Streamlit Dashboard on Streamlit Cloud

1. Go to [Streamlit Cloud](https://share.streamlit.io/)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Configure:
   - **Repository**: `YOUR_USERNAME/procurement-intelligence-platform`
   - **Branch**: `main`
   - **Main file path**: `dashboard/app.py`
6. Click "Deploy"

**Your dashboard will be live at**: `https://YOUR_USERNAME-procurement-intelligence-platform-XXXX.streamlit.app`

---

## Step 4: Connect Dashboard to API

### For Local Development

The dashboard automatically connects to local API:
```python
API_URL = "http://localhost:8000"  # Default for local
```

### For Streamlit Cloud (Production)

Update `dashboard/app.py` to use your deployed API:

```python
import os

# Use environment variable or default to local
API_URL = os.getenv("API_URL", "http://localhost:8000")

# For Streamlit Cloud, set this in secrets:
# API_URL = "https://procurement-api-XXXX.onrender.com"
```

### Setting API_URL on Streamlit Cloud

1. Go to your app on [Streamlit Cloud](https://share.streamlit.io/)
2. Click "Manage app" → "Settings"
3. Go to "Secrets" section
4. Add:
```toml
API_URL = "https://your-render-api-url.onrender.com"
```
5. Click "Save" and reboot app

---

## Step 5: Update Your Resume

Add these live URLs to your resume:

### Resume Bullet Point

> **Procurement Intelligence Platform** | [Live Demo](https://your-dashboard-url.streamlit.app) | [API Docs](https://your-api-url.onrender.com/docs)
> - Built full-stack analytics platform with FastAPI backend and Streamlit frontend
> - Implemented ML-powered forecasting and risk assessment algorithms
> - Deployed on Render and Streamlit Cloud with CI/CD pipeline
> - [GitHub Repository](https://github.com/YOUR_USERNAME/procurement-intelligence-platform)

### GitHub README Badge

Add this badge to your README.md:

```markdown
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-green)](https://your-dashboard-url.streamlit.app)
[![API Docs](https://img.shields.io/badge/API%20Docs-Swagger-blue)](https://your-api-url.onrender.com/docs)
```

---

## Step 6: Verify Everything Works

### Test API Endpoints

```bash
# Health check
curl https://your-api-url.onrender.com/health

# Get KPIs
curl https://your-api-url.onrender.com/kpis

# Get API documentation (Swagger UI)
# Open in browser: https://your-api-url.onrender.com/docs
```

### Test Dashboard

1. Open your Streamlit Cloud URL in browser
2. Verify data loads from API
3. Test filters and visualizations

---

## 🎯 Quick Start Commands

### Start Locally (Development)

```bash
# Terminal 1: Start API
uvicorn api.main:app --reload

# Terminal 2: Start Dashboard
streamlit run dashboard/app.py
```

### Deploy Updates

```bash
# Make changes
git add .
git commit -m "Update: description of changes"
git push origin main

# Render and Streamlit Cloud auto-deploy on push!
```

---

## 📊 What You'll Have After Deployment

✅ **Live API URL** (e.g., `https://procurement-api-xyz.onrender.com`)  
✅ **Live Dashboard URL** (e.g., `https://procurement-dashboard.streamlit.app`)  
✅ **Interactive API Docs** (Swagger UI at `/docs`)  
✅ **Professional Demo** you can share in interviews  
✅ **Impressive Portfolio Piece** with real deployment

---

## 🔧 Troubleshooting

### API Returns 500 Errors

**Solution**: Database not initialized

The API auto-initializes on startup. If you see errors:
1. Check logs in Render dashboard
2. Ensure `init_db()` is called in `api/main.py`

### Dashboard Can't Connect to API

**Solution**: Update API_URL

1. Get your Render API URL from dashboard
2. Add to Streamlit Cloud secrets
3. Reboot the Streamlit app

### Slow Loading Times

**Expected**: Free tiers have cold starts

- Render free tier spins down after 15 min of inactivity
- First request may take 30-60 seconds (cold start)
- Subsequent requests are fast

---

## 🎉 Success!

You now have:
- ✅ Production deployment on Render
- ✅ Live dashboard on Streamlit Cloud  
- ✅ Professional demo URLs for your resume
- ✅ Real-world DevOps experience

**Your portfolio is now interview-ready!** 🚀

---

## 📞 Support

If you encounter issues:
1. Check Render/Streamlit Cloud logs
2. Verify environment variables are set
3. Test API endpoints with curl/Postman
4. Check CORS settings if dashboard can't connect

**Good luck with your job search!** 💼
