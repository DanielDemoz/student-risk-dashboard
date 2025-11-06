"""
Start server on multiple ports - choose which one to use
"""
import os
import sys
from pathlib import Path

# Change to script directory
script_dir = Path(__file__).parent
os.chdir(script_dir)
sys.path.insert(0, str(script_dir))

import uvicorn

def start_server(port):
    """Start server on specified port."""
    print("=" * 60)
    print(f"Starting Student Risk Dashboard on PORT {port}")
    print("=" * 60)
    print(f"Working directory: {os.getcwd()}")
    print(f"Open: http://localhost:{port}")
    print("=" * 60)
    print("\nPress CTRL+C to stop the server\n")
    
    try:
        uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=True)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print(f"\n\nError starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import sys
    
    # Default port
    port = 8001
    
    # Check if port specified as argument
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 8001.")
    
    print("\nAvailable ports to try:")
    print("  - Port 8001: python start.py")
    print("  - Port 8000: python start_server.py")
    print("  - Port 3000: python start_server_3000.py")
    print("  - Custom: python start_all_ports.py [PORT_NUMBER]")
    print()
    
    start_server(port)

