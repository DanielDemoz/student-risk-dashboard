"""
Comprehensive diagnostic script for Student Risk Dashboard
"""

import sys
import socket
from pathlib import Path
import subprocess

print("=" * 70)
print("Student Risk Dashboard - Diagnostic Tool")
print("=" * 70)

issues_found = []
solutions = []

# 1. Check Python version
print("\n[1] Checking Python version...")
version = sys.version_info
if version.major >= 3 and version.minor >= 10:
    print(f"   [OK] Python {version.major}.{version.minor}.{version.micro} - OK")
else:
    print(f"   [X] Python {version.major}.{version.minor} - Need Python 3.10+")
    issues_found.append("Python version")
    solutions.append("Upgrade to Python 3.10 or higher")

# 2. Check required packages
print("\n[2] Checking required packages...")
required_packages = {
    'fastapi': 'FastAPI',
    'uvicorn': 'Uvicorn',
    'pandas': 'Pandas',
    'openpyxl': 'OpenPyXL',
    'pydantic': 'Pydantic'
}

missing = []
for package, name in required_packages.items():
    try:
        __import__(package)
        print(f"   [OK] {name} - OK")
    except ImportError:
        print(f"   [X] {name} - MISSING")
        missing.append(package)
        issues_found.append(f"Missing package: {package}")

if missing:
    solutions.append(f"Install missing packages: pip install {' '.join(missing)}")

# 3. Check file structure
print("\n[3] Checking file structure...")
required_files = [
    'app/main.py',
    'app/models.py',
    'static/index.html',
    'utils/data_preprocessing.py'
]

missing_files = []
for file_path in required_files:
    if Path(file_path).exists():
        print(f"   [OK] {file_path} - OK")
    else:
        print(f"   [X] {file_path} - MISSING")
        missing_files.append(file_path)
        issues_found.append(f"Missing file: {file_path}")

# 4. Test imports
print("\n[4] Testing imports...")
try:
    from app.main import app
    print("   [OK] app.main - OK")
except Exception as e:
    print(f"   [X] app.main - ERROR: {e}")
    issues_found.append("Import error")
    solutions.append(f"Fix import error: {str(e)}")

try:
    from utils.data_preprocessing import process_excel_file
    print("   [OK] utils.data_preprocessing - OK")
except Exception as e:
    print(f"   [X] utils.data_preprocessing - ERROR: {e}")
    issues_found.append("Import error")
    solutions.append(f"Fix import error: {str(e)}")

# 5. Check port availability
print("\n[5] Checking port 8001...")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('127.0.0.1', 8001))
sock.close()

if result == 0:
    print("   [!] Port 8001 is in use - Server might be running")
else:
    print("   [OK] Port 8001 is available")
    if not issues_found:
        print("   → Server is NOT running. Start it with: python start.py")

# 6. Check directories
print("\n[6] Checking directories...")
required_dirs = ['data', 'static', 'db']
for dir_name in required_dirs:
    path = Path(dir_name)
    if path.exists():
        print(f"   [OK] {dir_name}/ - OK")
    else:
        print(f"   [!] {dir_name}/ - Will be created on startup")

# 7. Check CORS configuration
print("\n[7] Checking CORS configuration...")
try:
    from app.main import app
    # Check if CORS middleware is added
    has_cors = any('CORSMiddleware' in str(middleware) for middleware in app.user_middleware)
    if has_cors:
        print("   [OK] CORS middleware configured - OK")
    else:
        print("   [!] CORS middleware not found")
        issues_found.append("CORS configuration")
        solutions.append("CORS should be configured in app/main.py")
except:
    pass

# Summary
print("\n" + "=" * 70)
print("DIAGNOSTIC SUMMARY")
print("=" * 70)

if not issues_found:
    print("\n[SUCCESS] All checks passed!")
    print("\nRECOMMENDED ACTIONS:")
    print("1. Start the server:")
    print("   python start.py")
    print("\n2. Open in browser:")
    print("   http://localhost:8001")
    print("\n3. If accessing from GitHub Pages:")
    print("   - Make sure server is running locally")
    print("   - Or deploy backend to Render/Railway")
    print("   - Update API URL in dashboard")
else:
    print(f"\n[ERROR] Found {len(issues_found)} issue(s):")
    for issue in issues_found:
        print(f"   - {issue}")
    
    print("\nSOLUTIONS:")
    for i, solution in enumerate(solutions, 1):
        print(f"{i}. {solution}")

print("\n" + "=" * 70)

