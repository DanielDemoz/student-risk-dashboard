# Deployment Guide

## GitHub Pages (Static HTML)

The `index.html` file in the root directory is a GitHub Pages-compatible landing page that explains how to run the application locally.

### Setup GitHub Pages

1. Go to your repository Settings
2. Navigate to Pages
3. Select "Deploy from a branch"
4. Choose `main` branch and `/ (root)` folder
5. Save

The landing page will be available at: `https://yourusername.github.io/student-risk-dashboard/`

## Local Development

### Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/student-risk-dashboard.git
cd student-risk-dashboard

# Install dependencies
pip install -r requirements.txt

# Start server
python start.py
```

Then open http://localhost:8001

## Cloud Deployment Options

### 1. Render

1. Sign up at render.com
2. Connect your GitHub repository
3. Create new Web Service
4. Set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Deploy!

### 2. Railway

1. Sign up at railway.app
2. New Project → Deploy from GitHub
3. Select your repository
4. Railway auto-detects Python and FastAPI
5. Deploy!

### 3. Heroku

1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
3. Deploy:
   ```bash
   heroku create
   git push heroku main
   ```

### 4. PythonAnywhere

1. Upload code via web interface
2. Set Web App WSGI configuration
3. Point to `app.main:app`
4. Reload!

## Environment Variables

For production, consider setting:
- `DATABASE_URL` - If using external database
- `CORS_ORIGINS` - Allowed frontend origins
- `SECRET_KEY` - For session management (if added)

## Notes

- The application requires Python 3.10+
- All dependencies are in `requirements.txt`
- Static files are served from `/static` directory
- Data files are stored in `/data` (gitignored)

