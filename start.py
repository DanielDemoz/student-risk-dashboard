"""Start the server."""
import uvicorn

if __name__ == "__main__":
    print("Starting Student Risk Dashboard...")
    print("Open: http://localhost:8001")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)

