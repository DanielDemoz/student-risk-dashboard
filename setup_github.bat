@echo off
REM GitHub Setup Script for Windows

echo Setting up GitHub repository...
echo.

REM Initialize git if not already
if not exist ".git" (
    echo Initializing git repository...
    git init
)

REM Add all files
echo Adding files to git...
git add .

REM Create initial commit
echo Creating initial commit...
git commit -m "Initial commit: Student Risk Dashboard"

echo.
echo Files are ready for GitHub!
echo.
echo Next steps:
echo 1. Create a new repository on GitHub (https://github.com/new)
echo 2. Copy the repository URL
echo 3. Run these commands:
echo.
echo    git remote add origin YOUR_REPOSITORY_URL
echo    git branch -M main
echo    git push -u origin main
echo.
echo Your repository will be available at:
echo    https://github.com/YOUR_USERNAME/student-risk-dashboard
echo.
echo For GitHub Pages, go to Settings ^> Pages and enable it.
pause

