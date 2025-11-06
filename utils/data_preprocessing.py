"""
Process Excel file with Grades and Attendance worksheets.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Dict
import logging

logger = logging.getLogger(__name__)


def convert_grade_to_numeric(grade_value) -> float:
    """Convert grade to numeric (0-100)."""
    if pd.isna(grade_value):
        return np.nan
    
    if isinstance(grade_value, (int, float)):
        return float(grade_value) if grade_value > 1 else float(grade_value * 100)
    
    grade_str = str(grade_value).strip().upper().replace('%', '')
    
    try:
        grade_num = float(grade_str)
        return grade_num if grade_num > 1 else grade_num * 100
    except ValueError:
        letter_map = {'A+': 97, 'A': 93, 'A-': 90, 'B+': 87, 'B': 83, 'B-': 80,
                     'C+': 77, 'C': 73, 'C-': 70, 'D+': 67, 'D': 63, 'D-': 60, 'F': 50}
        return letter_map.get(grade_str, np.nan)


def determine_risk_label(grade: float, attendance: float) -> str:
    """Determine risk label."""
    if pd.isna(grade) and pd.isna(attendance):
        return "Unknown"
    
    grade_low = not pd.isna(grade) and grade < 70
    attendance_low = not pd.isna(attendance) and attendance < 70
    
    if grade_low and attendance_low:
        return "High Risk"
    elif grade_low or attendance_low:
        return "At Risk"
    return "Safe"


def get_recommended_action(grade: float, attendance: float) -> str:
    """Get recommended action."""
    grade_low = not pd.isna(grade) and grade < 70
    attendance_low = not pd.isna(attendance) and attendance < 70
    
    if grade_low and attendance_low:
        return "High Risk: Counseling + academic support + attendance intervention"
    elif grade_low:
        return "Schedule tutoring session and academic mentoring. Develop study plan."
    elif attendance_low:
        return "Attendance intervention meeting. Send attendance warning. Time management support."
    return "Continue regular progress checks. No immediate concern."


def process_excel_file(file_path: Path) -> Tuple[pd.DataFrame, Dict]:
    """Process Excel file with Grades and Attendance worksheets."""
    logger.info(f"Processing: {file_path}")
    
    # Read Excel file
    excel_file = pd.ExcelFile(file_path)
    sheet_names = excel_file.sheet_names
    logger.info(f"Available sheets: {sheet_names}")
    
    # Find sheets (case-insensitive)
    grades_sheet = None
    attendance_sheet = None
    
    for sheet in sheet_names:
        if 'grade' in sheet.lower():
            grades_sheet = sheet
        elif 'attendance' in sheet.lower():
            attendance_sheet = sheet
    
    if not grades_sheet:
        grades_sheet = sheet_names[0]
    if not attendance_sheet:
        attendance_sheet = sheet_names[1] if len(sheet_names) > 1 else sheet_names[0]
    
    # Read worksheets
    grades_df = pd.read_excel(file_path, sheet_name=grades_sheet)
    attendance_df = pd.read_excel(file_path, sheet_name=attendance_sheet)
    
    # Standardize column names
    grades_df.columns = grades_df.columns.str.strip()
    attendance_df.columns = attendance_df.columns.str.strip()
    
    # Find Student# column
    student_col_g = None
    student_col_a = None
    
    for col in grades_df.columns:
        if 'student' in col.lower() and '#' in col.lower():
            student_col_g = col
            break
    
    for col in attendance_df.columns:
        if 'student' in col.lower() and '#' in col.lower():
            student_col_a = col
            break
    
    if not student_col_g or not student_col_a:
        raise ValueError("Student# column not found")
    
    # Rename to standard
    grades_df = grades_df.rename(columns={student_col_g: 'Student#'})
    attendance_df = attendance_df.rename(columns={student_col_a: 'Student#'})
    
    # Find grade column
    grade_col = None
    for col in grades_df.columns:
        if 'grade' in col.lower() and ('current' in col.lower() or 'overall' in col.lower()):
            grade_col = col
            break
    
    if not grade_col:
        raise ValueError("Grade column not found")
    
    # Merge
    merged = pd.merge(grades_df, attendance_df, on='Student#', how='outer', suffixes=('_g', '_a'))
    
    # Get student name
    if 'Student Name_g' in merged.columns:
        merged['Student Name'] = merged['Student Name_g'].fillna(merged.get('Student Name_a', ''))
    elif 'Student Name_a' in merged.columns:
        merged['Student Name'] = merged['Student Name_a']
    else:
        merged['Student Name'] = merged.get('Student Name', 'Unknown')
    
    # Get program
    if 'Program Name' in merged.columns:
        merged['Program'] = merged['Program Name']
    elif 'Program Name_g' in merged.columns:
        merged['Program'] = merged['Program Name_g']
    else:
        merged['Program'] = 'Unknown'
    
    # Convert grade
    merged['grade'] = merged[grade_col].apply(convert_grade_to_numeric)
    
    # Calculate attendance rate
    def calc_attendance(row):
        if 'Attended % to Date' in row and pd.notna(row.get('Attended % to Date')):
            return float(row['Attended % to Date'])
        attended = row.get('Attended Hours to Date', 0)
        scheduled = row.get('Scheduled Hours to Date', 0)
        if pd.notna(scheduled) and scheduled > 0:
            return (float(attended) / float(scheduled)) * 100
        return np.nan
    
    merged['attendance_rate'] = merged.apply(calc_attendance, axis=1)
    
    # Fill missing grades with program average
    for program in merged['Program'].unique():
        mask = merged['Program'] == program
        avg = merged.loc[mask, 'grade'].mean()
        if pd.notna(avg):
            merged.loc[mask & merged['grade'].isna(), 'grade'] = avg
    
    # Fill remaining with overall average
    overall_avg = merged['grade'].mean()
    if pd.notna(overall_avg):
        merged['grade'] = merged['grade'].fillna(overall_avg)
    
    # Determine risk
    merged['risk_label'] = merged.apply(
        lambda row: determine_risk_label(row['grade'], row['attendance_rate']), axis=1
    )
    
    # Get recommendations
    merged['recommended_action'] = merged.apply(
        lambda row: get_recommended_action(row['grade'], row['attendance_rate']), axis=1
    )
    
    # Generate emails
    merged['email'] = merged['Student Name'].apply(
        lambda x: f"{str(x).lower().replace(' ', '.')}@college.ca"
    )
    
    # Drop duplicates
    merged = merged.drop_duplicates(subset=['Student#'], keep='first')
    
    # Select final columns
    result = merged[[
        'Student#', 'Student Name', 'Program', 'grade', 
        'attendance_rate', 'risk_label', 'recommended_action', 'email'
    ]].copy()
    
    result.columns = ['student_id', 'student_name', 'program', 'grade', 
                     'attendance_rate', 'risk_label', 'recommended_action', 'email']
    
    # Statistics
    stats = {
        'total_students': len(result),
        'at_risk_count': len(result[result['risk_label'].isin(['At Risk', 'High Risk'])]),
        'safe_count': len(result[result['risk_label'] == 'Safe']),
        'avg_grade': result['grade'].mean(),
        'avg_attendance': result['attendance_rate'].mean()
    }
    
    return result, stats

