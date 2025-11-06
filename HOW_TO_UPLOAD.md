# 📤 How to Upload Excel File - Step by Step Guide

## Quick Steps

1. **Prepare your Excel file** with two worksheets
2. **Start the server** (if not running)
3. **Open the dashboard** in your browser
4. **Click "Choose File"** or the file upload area
5. **Select your Excel file**
6. **Click "Upload & Process Excel File"**
7. **Wait for processing** (usually a few seconds)
8. **View results** in the table below

---

## Detailed Instructions

### Step 1: Prepare Your Excel File

Your Excel file must have **two worksheets**:

#### Worksheet 1: "Grades"
Required columns:
- `Student#` - Unique student identifier
- `Student Name` - Full name
- `Program Name` - Program/course name
- `Current Overall Program Grade` - Numeric grade (0-100) or letter grade

**Example:**
| Student# | Student Name | Program Name | Current Overall Program Grade |
|----------|--------------|--------------|-------------------------------|
| S101 | Alice Brown | Business Admin | 82 |
| S102 | Ben Carter | Accounting | 68 |

#### Worksheet 2: "Attendance"
Required columns:
- `Student#` - Must match Grades worksheet
- `Student Name` - Full name
- `Scheduled Hours to Date` - Total scheduled hours
- `Attended Hours to Date` - Hours attended
- `Attended % to Date` - (Optional, will be calculated if missing)

**Example:**
| Student# | Student Name | Scheduled Hours to Date | Attended Hours to Date | Attended % to Date |
|----------|--------------|-------------------------|----------------------|-------------------|
| S101 | Alice Brown | 100 | 92 | 92 |
| S102 | Ben Carter | 100 | 65 | 65 |

### Step 2: Start the Server

**Open PowerShell/Terminal and run:**

```powershell
cd "C:\Users\asbda\Computek College Students at Risk"
python start.py
```

**Wait for:**
```
INFO:     Uvicorn running on http://127.0.0.1:8001
INFO:     Application startup complete.
```

### Step 3: Open Dashboard

**In your browser, go to:**
- **Local:** http://localhost:8001
- **GitHub Pages:** https://danieldemoz.github.io/student-risk-dashboard/

### Step 4: Upload File

1. **Find the upload section** (top of the page)
2. **Click on the file upload area** (dashed box)
   - Or click "Click to Select Excel File"
3. **Browse your computer** for the Excel file
4. **Select the file** and click "Open"
5. **Verify** the file name appears (e.g., "✓ Selected: Computek Demo Data.xlsx")
6. **Click** "Upload & Process Excel File" button

### Step 5: Wait for Processing

You'll see:
- ⏳ Loading spinner
- "Processing files and calculating risk scores..." message

**Processing usually takes:**
- Small files (< 100 students): 2-5 seconds
- Large files (100+ students): 5-15 seconds

### Step 6: View Results

After processing, you'll see:

1. **Success message** (green box)
   - "✅ Processed X students successfully"

2. **Summary Statistics** (colored cards)
   - Total students
   - High Risk count
   - At Risk count
   - Safe count

3. **Results Table** (top 10 at-risk students)
   - Student Name
   - Program
   - Grade
   - Attendance %
   - Risk Label (color-coded)
   - Recommended Action
   - Email (clickable mailto link)

---

## Troubleshooting Upload Issues

### Problem: "Failed to fetch"
**Solution:**
- Make sure server is running (`python start.py`)
- Check API URL is correct (should be `http://localhost:8001`)

### Problem: "File must be an Excel file"
**Solution:**
- Make sure file extension is `.xlsx` or `.xls`
- Not a CSV file - must be Excel format

### Problem: "Student# column not found"
**Solution:**
- Check your Excel file has a column named `Student#`
- Column names are case-sensitive
- Make sure there are no extra spaces

### Problem: "Could not find required worksheets"
**Solution:**
- Verify your Excel file has worksheets named:
  - "Grades" (or contains "grade" in the name)
  - "Attendance" (or contains "attendance" in the name)
- Sheet names are case-insensitive

### Problem: Processing takes too long
**Solution:**
- This is normal for large files (500+ students)
- Wait for the processing to complete
- Check server terminal for progress

---

## Example Excel File Structure

### Grades Worksheet:
```
Student# | Student Name      | Program Name              | Current Overall Program Grade
---------|-------------------|---------------------------|------------------------------
S101     | Alice Brown       | Business Admin            | 82
S102     | Ben Carter        | Accounting                | 68
S103     | Carla James       | Marketing                 | 72
```

### Attendance Worksheet:
```
Student# | Student Name      | Scheduled Hours to Date | Attended Hours to Date | Attended % to Date
---------|-------------------|-------------------------|------------------------|-------------------
S101     | Alice Brown       | 100                     | 92                     | 92
S102     | Ben Carter        | 100                     | 65                     | 65
S103     | Carla James       | 100                     | 88                     | 88
```

---

## Tips

✅ **Best Practices:**
- Use consistent Student# format across both worksheets
- Ensure Student# matches exactly between worksheets
- Remove any empty rows
- Save as .xlsx format (recommended)

❌ **Common Mistakes:**
- Forgetting to include Student# column
- Using different Student# formats (e.g., "S101" vs "101")
- Missing required columns
- Using CSV instead of Excel format

---

## Need Help?

1. **Check server is running:** Look for "Uvicorn running" message
2. **Check browser console:** Press F12 → Console tab for errors
3. **Check server logs:** Look at terminal where server is running
4. **Run diagnostic:** `python diagnose.py`

