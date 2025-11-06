# 🚀 Quick Start Guide

## Installation & Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate sample data (optional):**
   ```bash
   python create_sample_data.py
   ```

3. **Start the API server:**
   ```bash
   python start_server.py
   ```
   Or:
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access the API:**
   - API Root: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc

## First Steps

### 1. Upload Data Files

**Option A: Using the Web Form**
- Open `templates/upload_form.html` in your browser
- Upload CSV/Excel files for grades, attendance, and/or absences

**Option B: Using Python**
```python
import requests

files = {
    'grades': open('data/grades.csv', 'rb'),
    'attendance': open('data/attendance.csv', 'rb'),
    'absences': open('data/absences.csv', 'rb')
}

response = requests.post('http://localhost:8000/upload', files=files)
print(response.json())
```

**Option C: Using cURL**
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "grades=@data/grades.csv" \
  -F "attendance=@data/attendance.csv" \
  -F "absences=@data/absences.csv"
```

### 2. View Risk Data

**Get all students:**
```bash
curl http://localhost:8000/students
```

**Get summary statistics:**
```bash
curl http://localhost:8000/summary
```

**Get specific student:**
```bash
curl http://localhost:8000/students/5682941
```

### 3. Test the API

Run the example script:
```bash
python example_usage.py
```

## Power BI Integration

The API provides Power BI-compatible endpoints:

1. **Get Risk Data:**
   ```
   GET http://localhost:8000/risk-data
   ```

2. **Get Summary:**
   ```
   GET http://localhost:8000/risk-summary
   ```

3. **Filter by Program:**
   ```
   GET http://localhost:8000/risk-data?program=Accounting, Payroll and Tax
   ```

4. **Filter by Risk Level:**
   ```
   GET http://localhost:8000/risk-data?risk_level=High
   ```

In Power BI:
- Use "Web" data source
- Enter the API URL
- Set authentication to "Anonymous" (or configure as needed)

## File Format Requirements

### Grades File (grades.csv)
Required columns:
- `Student ID`
- `Student Name`
- `Grade`
- `Program` (optional)

### Attendance File (attendance.csv)
Required columns:
- `Student ID`
- `Student Name`
- `Classes Attended`
- `Total Classes`
- `Program` (optional)

### Absences File (absences.csv)
Required columns:
- `Student ID`
- `Student Name`
- `Absence Dates` (comma-separated, optional)
- `Program` (optional)

## Risk Score Calculation

Risk scores are automatically calculated using:
- **50%** weight for grades below 70
- **30%** weight for attendance below 90%
- **20%** weight for consecutive absences > 2

Risk levels:
- **High**: ≥ 0.7
- **Medium**: 0.4 - 0.69
- **Low**: < 0.4

## Troubleshooting

**Port already in use:**
```bash
# Use a different port
uvicorn app.main:app --port 8001
```

**Database errors:**
- Delete `db/risk.db` and restart the server to recreate the database

**Import errors:**
- Make sure all dependencies are installed: `pip install -r requirements.txt`

**File upload errors:**
- Check that CSV files have the required columns
- Ensure file names match expected format (grades.csv, attendance.csv, absences.csv)

## Next Steps

1. Review the full documentation in `README.md`
2. Customize risk calculation formulas in `utils/calculate_risk.py`
3. Deploy to production (Render, Railway, Azure, etc.)
4. Configure CORS for your specific dashboard domain
5. Set up automated data refresh (GitHub Actions, cron, etc.)

