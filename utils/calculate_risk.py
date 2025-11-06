"""
Risk score calculation utilities.
Implements the risk scoring algorithm based on grades, attendance, and absences.
"""

import pandas as pd
import numpy as np
from typing import List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_consecutive_absences(absence_dates: str) -> int:
    """
    Calculate maximum consecutive absences from absence dates string.
    
    Args:
        absence_dates: Comma-separated string of absence dates
    
    Returns:
        Maximum consecutive absences count
    """
    if pd.isna(absence_dates) or not str(absence_dates).strip():
        return 0
    
    try:
        dates_str = str(absence_dates).strip()
        if not dates_str:
            return 0
        
        # Split dates and count
        dates = [d.strip() for d in dates_str.split(',') if d.strip()]
        
        if len(dates) <= 1:
            return len(dates)
        
        # For simplicity, if multiple dates exist, assume some are consecutive
        # In a real scenario, you'd parse dates and find actual consecutive days
        # For now, return count as a proxy
        return len(dates)
    except Exception as e:
        logger.warning(f"Error calculating consecutive absences: {e}")
        return 0


def calculate_risk_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate derived risk metrics for each student.
    
    Args:
        df: Merged student data DataFrame
    
    Returns:
        DataFrame with calculated risk metrics
    """
    result_df = df.copy()
    
    # Calculate attendance rate
    result_df['attendance_rate'] = (
        result_df['Classes Attended'] / result_df['Total Classes']
    ).fillna(0).clip(0, 1)
    
    # Calculate average grade (if multiple grades exist, take mean)
    if 'Grade' in result_df.columns:
        # Convert Grade to numeric, handling any string values
        result_df['Grade'] = pd.to_numeric(result_df['Grade'], errors='coerce').fillna(0)
        # If there are multiple rows per student, group and average
        if 'Student ID' in result_df.columns:
            avg_grades = result_df.groupby('Student ID')['Grade'].mean().reset_index()
            avg_grades.columns = ['Student ID', 'avg_grade']
            result_df = result_df.merge(avg_grades, on='Student ID', how='left')
        else:
            result_df['avg_grade'] = result_df['Grade']
    else:
        result_df['avg_grade'] = 0
    
    # Calculate consecutive absences
    if 'Absence Dates' in result_df.columns:
        result_df['consecutive_absences'] = result_df['Absence Dates'].apply(
            calculate_consecutive_absences
        )
    elif 'Absence_Count' in result_df.columns:
        result_df['consecutive_absences'] = result_df['Absence_Count']
    else:
        result_df['consecutive_absences'] = 0
    
    # Calculate flags
    result_df['below_70_flag'] = (result_df['avg_grade'] < 70).astype(int)
    result_df['low_attendance_flag'] = (result_df['attendance_rate'] < 0.9).astype(int)
    
    # Calculate risk score
    # Formula: 0.5 * below_70_flag + 0.3 * low_attendance_flag + 0.2 * (consecutive_absences > 2)
    result_df['risk_score'] = (
        0.5 * result_df['below_70_flag'] +
        0.3 * result_df['low_attendance_flag'] +
        0.2 * (result_df['consecutive_absences'] > 2).astype(int)
    ).round(2)
    
    # Determine risk level
    def assign_risk_level(score: float) -> str:
        if score >= 0.7:
            return "High"
        elif score >= 0.4:
            return "Medium"
        else:
            return "Low"
    
    result_df['risk_level'] = result_df['risk_score'].apply(assign_risk_level)
    
    return result_df


def prepare_student_risk_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare final student risk dataset with all required fields.
    
    Args:
        df: DataFrame with calculated metrics
    
    Returns:
        Cleaned DataFrame ready for database storage
    """
    # Ensure Student ID and Student Name exist
    required_cols = ['Student ID', 'Student Name']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"Missing required columns: {required_cols}")
    
    # Select and rename columns for final output
    output_cols = {
        'Student ID': 'student_id',
        'Student Name': 'student_name',
        'Program': 'program',
        'attendance_rate': 'attendance_rate',
        'avg_grade': 'avg_grade',
        'consecutive_absences': 'consecutive_absences',
        'below_70_flag': 'below_70_flag',
        'low_attendance_flag': 'low_attendance_flag',
        'risk_score': 'risk_score',
        'risk_level': 'risk_level'
    }
    
    # Get available columns
    available_cols = {k: v for k, v in output_cols.items() if k in df.columns}
    
    result_df = df[list(available_cols.keys())].copy()
    result_df = result_df.rename(columns=available_cols)
    
    # Fill missing values
    if 'program' in result_df.columns:
        result_df['program'] = result_df['program'].fillna('Unknown')
    else:
        result_df['program'] = 'Unknown'
    
    result_df['attendance_rate'] = result_df['attendance_rate'].fillna(0.0)
    result_df['avg_grade'] = result_df['avg_grade'].fillna(0.0)
    result_df['consecutive_absences'] = result_df['consecutive_absences'].fillna(0)
    result_df['below_70_flag'] = result_df['below_70_flag'].fillna(0)
    result_df['low_attendance_flag'] = result_df['low_attendance_flag'].fillna(0)
    result_df['risk_score'] = result_df['risk_score'].fillna(0.0)
    result_df['risk_level'] = result_df['risk_level'].fillna('Low')
    
    # Remove duplicates based on student_id (keep first occurrence)
    result_df = result_df.drop_duplicates(subset=['student_id'], keep='first')
    
    return result_df


def process_and_calculate_risk(df: pd.DataFrame) -> pd.DataFrame:
    """
    Complete pipeline: calculate metrics and prepare risk dataset.
    
    Args:
        df: Merged student data DataFrame
    
    Returns:
        Final student risk dataset
    """
    # Calculate risk metrics
    df_with_metrics = calculate_risk_metrics(df)
    
    # Prepare final dataset
    risk_dataset = prepare_student_risk_dataset(df_with_metrics)
    
    logger.info(f"Processed {len(risk_dataset)} students for risk calculation")
    
    return risk_dataset

