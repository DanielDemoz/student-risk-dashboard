"""
Script to create sample CSV files for testing the Risk Dashboard API.
Run this script to generate sample data files.
"""

import pandas as pd
import random
from pathlib import Path

# Create data directory if it doesn't exist
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# Sample programs
programs = [
    "Accounting, Payroll and Tax",
    "Business Administration",
    "Computer Programming",
    "Network Administration",
    "Medical Office Administration"
]

# Generate sample student data
n_students = 50
student_ids = [f"{random.randint(5600000, 5999999)}" for _ in range(n_students)]
student_names = [
    f"Student {i}" for i in range(1, n_students + 1)
]

# Grades Data
grades_data = []
for i, student_id in enumerate(student_ids):
    # Vary grades - some students at risk (low grades)
    if random.random() < 0.3:  # 30% at risk
        grade = random.uniform(50, 75)
    else:
        grade = random.uniform(70, 100)
    
    grades_data.append({
        "Student ID": student_id,
        "Student Name": student_names[i],
        "Grade": round(grade, 1),
        "Program": random.choice(programs)
    })

grades_df = pd.DataFrame(grades_data)
grades_df.to_csv(data_dir / "grades.csv", index=False)
print(f"✅ Created {data_dir / 'grades.csv'} with {len(grades_df)} students")

# Attendance Data
attendance_data = []
for i, student_id in enumerate(student_ids):
    # Vary attendance - some students at risk (low attendance)
    if random.random() < 0.25:  # 25% at risk
        classes_attended = random.randint(70, 89)  # Below 90%
    else:
        classes_attended = random.randint(90, 100)
    
    total_classes = 100
    
    attendance_data.append({
        "Student ID": student_id,
        "Student Name": student_names[i],
        "Classes Attended": classes_attended,
        "Total Classes": total_classes,
        "Program": random.choice(programs)
    })

attendance_df = pd.DataFrame(attendance_data)
attendance_df.to_csv(data_dir / "attendance.csv", index=False)
print(f"✅ Created {data_dir / 'attendance.csv'} with {len(attendance_df)} students")

# Absences Data
absences_data = []
for i, student_id in enumerate(student_ids):
    # Some students with consecutive absences
    if random.random() < 0.15:  # 15% with consecutive absences
        num_absences = random.randint(3, 7)
        absence_dates = ", ".join([
            f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
            for _ in range(num_absences)
        ])
    else:
        absence_dates = ""
    
    absences_data.append({
        "Student ID": student_id,
        "Student Name": student_names[i],
        "Absence Dates": absence_dates,
        "Program": random.choice(programs)
    })

absences_df = pd.DataFrame(absences_data)
absences_df.to_csv(data_dir / "absences.csv", index=False)
print(f"✅ Created {data_dir / 'absences.csv'} with {len(absences_df)} students")

print("\n🎉 Sample data files created successfully!")
print(f"📁 Files location: {data_dir.absolute()}")
print("\nNext steps:")
print("1. Start the API: uvicorn app.main:app --reload")
print("2. Upload files via POST /upload or use templates/upload_form.html")
print("3. View data via GET /students or GET /summary")

