"""
Simple test - just check if server responds
"""
import sys

try:
    import requests
except ImportError:
    print("Installing requests...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests

API_BASE = "http://localhost:8001"

print("Testing server at:", API_BASE)
print()

try:
    print("1. Testing connection...")
    response = requests.get(f"{API_BASE}/", timeout=3)
    print(f"   [OK] Server responded! Status: {response.status_code}")
    print()
    
    print("2. Testing /results endpoint...")
    try:
        response = requests.get(f"{API_BASE}/results", timeout=3)
        print(f"   [OK] Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Found {len(data)} students")
    except Exception as e:
        print(f"   [INFO] {e}")
    
    print()
    print("3. Testing static files...")
    response = requests.get(f"{API_BASE}/static/style.css", timeout=3)
    print(f"   [OK] Static files accessible: {response.status_code == 200}")
    
    print()
    print("=" * 60)
    print("[SUCCESS] Server is running and responding!")
    print("=" * 60)
    print("\nYou can now:")
    print("1. Open http://localhost:8001 in your browser")
    print("2. Upload an Excel file")
    print("3. View risk analysis results")
    
except requests.exceptions.ConnectionError:
    print("[ERROR] Cannot connect to server")
    print()
    print("Server is NOT running. Start it with:")
    print("  python start.py")
    print()
    print("Make sure you see:")
    print("  INFO: Uvicorn running on http://127.0.0.1:8001")
    sys.exit(1)
    
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

