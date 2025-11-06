"""Start the server."""
import os
import sys
from pathlib import Path

# Change to script directory to ensure correct working directory
script_dir = Path(__file__).parent
os.chdir(script_dir)
sys.path.insert(0, str(script_dir))

import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("Starting Student Risk Dashboard...")
    print(f"Working directory: {os.getcwd()}")
    print("Open: http://localhost:8001")
    print("=" * 60)
    print("\nPress CTRL+C to stop the server\n")
    
    try:
        uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print(f"\n\nError starting server: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you're in the project directory")
        print("2. Check if port 8001 is available")
        print("3. Run: python diagnose.py")
        sys.exit(1)

