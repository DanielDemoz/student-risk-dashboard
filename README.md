# 📊 Student Risk Dashboard

**Computek College - AI Attendance & Performance Risk Assessment System**

A FastAPI-based web application for analyzing student performance and attendance data to identify at-risk students.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/DanielDemoz/student-risk-dashboard.git
   cd student-risk-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server**
   ```bash
   python start.py
   ```

4. **Open your browser**
   - Main Dashboard: http://localhost:8001
   - API Documentation: http://localhost:8001/docs

## 📋 Features

- ✅ **Excel File Upload** - Upload Excel files with Grades and Attendance worksheets
- ✅ **Automatic Risk Calculation** - Identifies High Risk, At Risk, and Safe students
- ✅ **Real-time Processing** - Instant data processing and risk assessment
- ✅ **Dashboard Interface** - Clean, responsive web interface
- ✅ **REST API** - Full API for integration with other systems
- ✅ **Email Integration** - Automatic email generation for student contact

## 📁 Excel File Format

Your Excel file must contain two worksheets:

### Grades Worksheet
- `Student#` - Unique student identifier
- `Student Name` - Full name
- `Program Name` - Program/course name
- `Current Overall Program Grade` - Numeric grade (0-100 or letter grade)

### Attendance Worksheet
- `Student#` - Unique student identifier (must match Grades)
- `Student Name` - Full name
- `Scheduled Hours to Date` - Total scheduled hours
- `Attended Hours to Date` - Hours attended
- `Attended % to Date` - Attendance percentage (optional, calculated if missing)

## 🎯 Risk Classification

- **High Risk**: Grade < 70% AND Attendance < 70%
- **At Risk**: Grade < 70% OR Attendance < 70% (but not both)
- **Safe**: Grade ≥ 70% AND Attendance ≥ 70%

## 📡 API Endpoints

### Upload Excel File
```http
POST /upload-excel
Content-Type: multipart/form-data

file: [Excel file]
train_model: false (optional)
```

### Get Results
```http
GET /results?at_risk_only=false
```

Returns JSON array of student risk predictions:
```json
[
  {
    "student_id": "S101",
    "student_name": "John Doe",
    "program": "Business Admin",
    "grade": 82.5,
    "attendance_rate": 92.3,
    "risk_label": "Safe",
    "recommended_action": "Continue regular progress checks.",
    "email": "john.doe@college.ca"
  }
]
```

## 🛠️ Development

### Project Structure
```
.
├── app/
│   ├── main.py          # FastAPI application
│   └── models.py        # Pydantic models
├── static/
│   ├── index.html       # Dashboard UI
│   ├── main.js          # Frontend JavaScript
│   └── style.css        # Styling
├── utils/
│   └── data_preprocessing.py  # Excel processing logic
├── data/                # Uploaded files (gitignored)
├── requirements.txt     # Python dependencies
└── start.py            # Server startup script
```

### Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start development server:
   ```bash
   python start.py
   ```

3. Access the dashboard at http://localhost:8001

## 📦 Deployment

### Option 1: Local/On-Premise
Run the FastAPI server on your local network or server.

### Option 2: Cloud Deployment
Deploy to:
- **Render**: Connect GitHub repo, auto-deploy
- **Railway**: Connect repo, set Python runtime
- **Heroku**: Add Procfile, deploy via Git
- **Azure App Service**: Deploy Python web app
- **AWS EC2**: Run on EC2 instance

### Example: Render Deployment

1. Connect your GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Deploy!

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

**Computek College**
- Institution: Computek College
- Project: Student Risk Assessment Dashboard

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Pandas for data processing
- OpenPyXL for Excel file handling

---

⭐ If you find this project helpful, please give it a star!
