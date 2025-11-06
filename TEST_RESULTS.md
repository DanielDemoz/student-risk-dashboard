# Test Results & Manual Testing Guide

## Automated Test Status

**Test Script:** `test_api.py` and `simple_test.py`

### Current Status
- ❌ Server not responding (timeout)
- ✅ App imports successfully
- ✅ All dependencies installed
- ✅ File structure correct

## Manual Testing Steps

### Step 1: Start Server Manually

**Open a NEW PowerShell window and run:**

```powershell
cd "C:\Users\asbda\Computek College Students at Risk"
python start.py
```

**Expected Output:**
```
============================================================
Starting Student Risk Dashboard...
Working directory: C:\Users\asbda\Computek College Students at Risk
Open: http://localhost:8001
============================================================

INFO:     Uvicorn running on http://127.0.0.1:8001
INFO:     Application startup complete.
```

**If you see errors:**
- Share the error message
- Check the terminal output

### Step 2: Test in Browser

1. **Open browser:** http://localhost:8001
2. **Expected:** Should see the dashboard
3. **If blank/error:** Check browser console (F12)

### Step 3: Test File Upload

1. **Prepare Excel file** with:
   - Grades worksheet (Student#, Student Name, Program Name, Current Overall Program Grade)
   - Attendance worksheet (Student#, Student Name, Scheduled Hours, Attended Hours)

2. **Upload file:**
   - Click "Upload & Process Excel File"
   - Select your Excel file
   - Click submit

3. **Expected:**
   - Success message
   - Results table appears
   - Summary statistics shown

### Step 4: Verify Results

Check that:
- ✅ Summary statistics display correctly
- ✅ Top 10 students shown in table
- ✅ Risk labels are color-coded
- ✅ Recommended actions displayed
- ✅ Email links work

## Test Checklist

- [ ] Server starts without errors
- [ ] http://localhost:8001 loads dashboard
- [ ] Can upload Excel file
- [ ] Processing completes successfully
- [ ] Results display correctly
- [ ] Summary statistics show
- [ ] Risk labels are correct
- [ ] Recommended actions appear
- [ ] Email links are clickable

## Common Issues & Solutions

### Issue: Server won't start
**Solution:** 
- Check for port conflicts
- Run as Administrator if permission errors
- Check Python version: `python --version`

### Issue: "Failed to fetch"
**Solution:**
- Make sure server is running
- Check API URL is correct
- Verify CORS is enabled (already done)

### Issue: Upload fails
**Solution:**
- Check Excel file format
- Verify worksheets are named correctly
- Check server logs for errors

## Running Automated Tests

Once server is running:

```powershell
python test_api.py
```

Or simpler test:

```powershell
python simple_test.py
```

## Next Steps

1. **Start server in separate terminal**
2. **Run test script:** `python test_api.py`
3. **Test in browser:** http://localhost:8001
4. **Upload sample Excel file**
5. **Verify results display**

