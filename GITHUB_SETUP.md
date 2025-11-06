# GitHub Setup Instructions

## Step 1: Initialize Git Repository

If you haven't already, run:

**Windows:**
```cmd
setup_github.bat
```

**Mac/Linux:**
```bash
chmod +x setup_github.sh
./setup_github.sh
```

**Or manually:**
```bash
git init
git add .
git commit -m "Initial commit: Student Risk Dashboard"
```

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `student-risk-dashboard`
3. Description: `Student Risk Assessment Dashboard for Computek College`
4. Choose Public or Private
5. **Don't** initialize with README (we already have one)
6. Click "Create repository"

## Step 3: Connect and Push

Copy the commands GitHub shows you, or run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/student-risk-dashboard.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

## Step 4: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under "Source", select:
   - Branch: `main`
   - Folder: `/ (root)`
4. Click **Save**

Your landing page will be available at:
`https://YOUR_USERNAME.github.io/student-risk-dashboard/`

## Step 5: Update README (Optional)

In `README.md`, replace:
- `yourusername` with your actual GitHub username
- Update any repository URLs

## Files Included for GitHub

✅ **index.html** - Landing page for GitHub Pages
✅ **README.md** - Project documentation
✅ **.gitignore** - Excludes sensitive files
✅ **requirements.txt** - Python dependencies
✅ **DEPLOYMENT.md** - Deployment guide
✅ **.github/workflows/deploy.yml** - GitHub Pages deployment

## What's Gitignored

- Database files (`*.db`)
- Data files (`data/*.csv`, `data/*.xlsx`)
- Python cache (`__pycache__/`)
- Virtual environments (`venv/`, `env/`)
- Model files (`models/*.pkl`)

## Quick Commands Reference

```bash
# Check status
git status

# Add changes
git add .

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push

# Pull latest changes
git pull
```

## Troubleshooting

**"Repository not found"**
- Check your repository URL
- Verify you have push access

**"Permission denied"**
- Set up SSH keys or use HTTPS with personal access token
- GitHub → Settings → Developer settings → Personal access tokens

**"Branch protection"**
- If main branch is protected, create a new branch and make a Pull Request

