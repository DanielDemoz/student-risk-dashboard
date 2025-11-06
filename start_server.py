"""
Alternative server startup script - runs on port 8000
"""
import os
import sys
from pathlib import Path

# Change to script directory
script_dir = Path(__file__).parent
os.chdir(script_dir)
sys.path.insert(0, str(script_dir))

import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("Starting Student Risk Dashboard on PORT 8000")
    print("=" * 60)
    print(f"Working directory: {os.getcwd()}")
    print("Open: http://localhost:8000")
    print("=" * 60)
    print("\nPress CTRL+C to stop the server\n")
    
    try:
        uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print(f"\n\nError starting server: {e}")
        sys.exit(1)

