# 🚀 Server Startup Options

You have multiple ways to start the server on different ports!

## Option 1: Default Port 8001

```powershell
python start.py
```

**Access at:** http://localhost:8001

---

## Option 2: Port 8000

```powershell
python start_server.py
```

**Access at:** http://localhost:8000

**Update dashboard API URL to:** `http://localhost:8000`

---

## Option 3: Port 3000

```powershell
python start_server_3000.py
```

**Access at:** http://localhost:3000

**Update dashboard API URL to:** `http://localhost:3000`

---

## Option 4: Custom Port

```powershell
python start_all_ports.py 5000
```

**Access at:** http://localhost:5000 (or whatever port you specify)

**Update dashboard API URL to:** `http://localhost:5000`

---

## Why Use Different Ports?

1. **Port 8001 is busy** - Use 8000 or 3000
2. **Multiple projects** - Run different servers on different ports
3. **Testing** - Test with different configurations
4. **Firewall issues** - Some ports may be blocked

---

## Quick Start Guide

### Step 1: Choose a port

Pick one:
- **8001** (default)
- **8000** (alternative)
- **3000** (alternative)
- **Custom** (any number you want)

### Step 2: Start the server

**For port 8001:**
```powershell
python start.py
```

**For port 8000:**
```powershell
python start_server.py
```

**For port 3000:**
```powershell
python start_server_3000.py
```

**For custom port (e.g., 5000):**
```powershell
python start_all_ports.py 5000
```

### Step 3: Update Dashboard API URL

1. Open the dashboard: http://localhost:8001 (or your chosen port)
2. Find the **API Server URL** input box
3. Change it to match your server port:
   - Port 8001: `http://localhost:8001`
   - Port 8000: `http://localhost:8000`
   - Port 3000: `http://localhost:3000`
   - Custom: `http://localhost:[PORT]`

### Step 4: Upload Excel File

Now you can upload your Excel file and it should work!

---

## Troubleshooting

### Port Already in Use?

If you get "Address already in use" error:

1. **Try a different port:**
   ```powershell
   python start_server.py  # Port 8000
   ```

2. **Or kill the process using the port:**
   ```powershell
   # Find process using port 8001
   netstat -ano | findstr :8001
   
   # Kill it (replace PID with actual number)
   taskkill /PID [PID] /F
   ```

### Still Getting "Failed to fetch"?

1. **Check server is running:**
   - Look for "Uvicorn running" message
   - Should see: `INFO: Application startup complete.`

2. **Verify API URL:**
   - Must match the port your server is using
   - Format: `http://localhost:XXXX` (no https, no trailing slash)

3. **Check browser console:**
   - Press F12 → Console tab
   - Look for error messages

4. **Try different port:**
   - Some ports may be blocked by firewall
   - Try 8000, 3000, or 5000

---

## All Available Startup Scripts

| Script | Port | Command |
|--------|------|----------|
| `start.py` | 8001 | `python start.py` |
| `start_server.py` | 8000 | `python start_server.py` |
| `start_server_3000.py` | 3000 | `python start_server_3000.py` |
| `start_all_ports.py` | Custom | `python start_all_ports.py [PORT]` |

---

## Recommended: Try Port 8000 First

If port 8001 doesn't work, try port 8000:

```powershell
# Terminal 1: Start server on port 8000
python start_server.py
```

Then in the dashboard:
- Change API URL to: `http://localhost:8000`
- Upload your Excel file

This often works better if port 8001 is blocked or busy!

