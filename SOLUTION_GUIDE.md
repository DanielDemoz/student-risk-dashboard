# 🔍 Problem Diagnosis & Solutions

## Main Problem: "Failed to fetch" Error

This error means the frontend (GitHub Pages) cannot connect to the backend API server.

## Common Causes & Solutions

### Problem 1: Server Not Running ❌

**Symptoms:**
- "Failed to fetch" error
- Port 8001 not responding

**Solution:**
```bash
# Start the server
python start.py

# Or directly
py -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

**Verify:**
- Open http://localhost:8001 in browser
- Should see dashboard or API response

---

### Problem 2: CORS Issues (Cross-Origin) ❌

**Symptoms:**
- Works on localhost but fails from GitHub Pages
- Browser console shows CORS error

**Current Status:**
✅ CORS is already configured in `app/main.py` with `allow_origins=["*"]`

**If still having issues:**
```python
# In app/main.py, ensure CORS is before routes:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Problem 3: Port Blocked or Different Port ❌

**Symptoms:**
- Server won't start
- "Address already in use" error

**Solution:**
```bash
# Use a different port
py -m uvicorn app.main:app --reload --port 8002

# Then update API URL in dashboard to: http://localhost:8002
```

---

### Problem 4: API URL Configuration ❌

**Symptoms:**
- GitHub Pages can't find backend
- Wrong URL in dashboard

**Solution:**
1. **For Local Development:**
   - API URL: `http://localhost:8001`
   - Make sure server is running locally

2. **For Production (Deployed Backend):**
   - Deploy backend to Render/Railway
   - Update API URL in dashboard to: `https://your-app.onrender.com`

---

### Problem 5: Type Conversion Errors ❌

**Symptoms:**
- "'>' not supported between instances of 'str' and 'int'"
- Server crashes on upload

**Status:**
✅ Already fixed in latest commit

**If still occurs:**
- Restart server after pulling latest code
- Ensure `utils/data_preprocessing.py` has latest fixes

---

## Step-by-Step Troubleshooting

### Step 1: Run Diagnostic
```bash
python diagnose.py
```

This will check:
- Python version
- Required packages
- File structure
- Imports
- Port availability
- CORS configuration

### Step 2: Start Server Properly
```bash
# Option 1: Using start.py
python start.py

# Option 2: Direct uvicorn
py -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8001

# Option 3: With specific host (allows external connections)
py -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Step 3: Test Server
```bash
# Test in browser
http://localhost:8001

# Test API endpoint
http://localhost:8001/results

# Should return JSON or error message
```

### Step 4: Check Browser Console
1. Open browser Developer Tools (F12)
2. Go to Console tab
3. Look for errors
4. Go to Network tab
5. Try uploading file
6. Check if request reaches server

---

## Quick Fix Checklist

- [ ] Server is running (`python start.py`)
- [ ] Port 8001 is accessible
- [ ] All packages installed (`pip install -r requirements.txt`)
- [ ] API URL in dashboard is correct
- [ ] CORS is enabled (already done)
- [ ] No firewall blocking port 8001
- [ ] Browser allows localhost connections

---

## Recommended Setup

### For Local Development:
1. **Terminal 1:** Start server
   ```bash
   python start.py
   ```

2. **Browser:** Open http://localhost:8001

3. **GitHub Pages:** Use `http://localhost:8001` as API URL

### For Production:
1. **Deploy Backend:**
   - Render: Connect GitHub repo, auto-deploy
   - Railway: Connect repo, set Python runtime
   
2. **Update Dashboard:**
   - Change API URL to deployed backend URL
   - Example: `https://student-risk-api.onrender.com`

---

## Still Having Issues?

1. **Check server logs:**
   - Look at terminal where server is running
   - Check for error messages

2. **Test API directly:**
   ```bash
   # Using curl or browser
   curl http://localhost:8001/results
   ```

3. **Check network:**
   - Verify firewall isn't blocking
   - Check if antivirus is interfering

4. **Restart everything:**
   - Stop server (CTRL+C)
   - Close browser
   - Restart server
   - Clear browser cache
   - Try again

