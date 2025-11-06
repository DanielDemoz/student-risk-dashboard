"""
Data merging and cleaning utilities.
Handles CSV/Excel file processing, validation, and merging.
"""

import pandas as pd
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_csv_file(df: pd.DataFrame, file_type: str) -> Tuple[bool, str]:
    """
    Validate CSV file has required columns.
    
    Args:
        df: DataFrame to validate
        file_type: Type of file ('grades', 'attendance', 'absences')
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_columns = {
        'grades': ['Student ID', 'Student Name', 'Grade', 'Program'],
        'attendance': ['Student ID', 'Student Name', 'Classes Attended', 'Total Classes', 'Program'],
        'absences': ['Student ID', 'Student Name', 'Absence Dates', 'Program']
    }
    
    required = required_columns.get(file_type, [])
    
    if not required:
        return False, f"Unknown file type: {file_type}"
    
    missing_cols = [col for col in required if col not in df.columns]
    
    if missing_cols:
        return False, f"Missing required columns in {file_type}: {', '.join(missing_cols)}"
    
    return True, ""


def clean_student_id(df: pd.DataFrame, id_column: str = 'Student ID') -> pd.DataFrame:
    """Clean and standardize Student ID column."""
    df = df.copy()
    df[id_column] = df[id_column].astype(str).str.strip()
    return df


def load_csv_file(file_path: Path) -> pd.DataFrame:
    """Load CSV or Excel file into DataFrame."""
    try:
        if file_path.suffix.lower() in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)
        return df
    except Exception as e:
        logger.error(f"Error loading file {file_path}: {str(e)}")
        raise


def merge_student_data(
    grades_df: Optional[pd.DataFrame] = None,
    attendance_df: Optional[pd.DataFrame] = None,
    absences_df: Optional[pd.DataFrame] = None
) -> pd.DataFrame:
    """
    Merge grades, attendance, and absences data by Student ID.
    
    Args:
        grades_df: DataFrame with grades data
        attendance_df: DataFrame with attendance data
        absences_df: DataFrame with absences data
    
    Returns:
        Merged DataFrame with all student data
    """
    merged = pd.DataFrame()
    
    # Start with grades if available
    if grades_df is not None:
        grades_df = clean_student_id(grades_df)
        merged = grades_df.copy()
        logger.info(f"Starting merge with {len(grades_df)} students from grades")
    
    # Merge attendance data
    if attendance_df is not None:
        attendance_df = clean_student_id(attendance_df)
        if merged.empty:
            merged = attendance_df.copy()
        else:
            # Merge on Student ID, keeping all students from grades
            merged = merged.merge(
                attendance_df[['Student ID', 'Classes Attended', 'Total Classes']],
                on='Student ID',
                how='left'
            )
            # Update Student Name and Program if missing
            for col in ['Student Name', 'Program']:
                if col in attendance_df.columns:
                    merged[col] = merged[col].fillna(
                        merged['Student ID'].map(
                            attendance_df.set_index('Student ID')[col]
                        )
                    )
        logger.info(f"Merged attendance data")
    
    # Merge absences data
    if absences_df is not None:
        absences_df = clean_student_id(absences_df)
        if merged.empty:
            merged = absences_df.copy()
        else:
            # Add absence information
            absences_df = absences_df.copy()
            if 'Absence Dates' in absences_df.columns:
                # Count absences
                absences_df['Absence_Count'] = absences_df['Absence Dates'].apply(
                    lambda x: len(str(x).split(',')) if pd.notna(x) and str(x).strip() else 0
                )
                merged = merged.merge(
                    absences_df[['Student ID', 'Absence Dates', 'Absence_Count']],
                    on='Student ID',
                    how='left'
                )
            # Update Student Name and Program if missing
            for col in ['Student Name', 'Program']:
                if col in absences_df.columns:
                    merged[col] = merged[col].fillna(
                        merged['Student ID'].map(
                            absences_df.set_index('Student ID')[col]
                        )
                    )
        logger.info(f"Merged absences data")
    
    # Ensure required columns exist with defaults
    if 'Classes Attended' not in merged.columns:
        merged['Classes Attended'] = 0
    if 'Total Classes' not in merged.columns:
        merged['Total Classes'] = 1
    if 'Grade' not in merged.columns:
        merged['Grade'] = 0
    if 'Absence_Count' not in merged.columns:
        merged['Absence_Count'] = 0
    if 'Absence Dates' not in merged.columns:
        merged['Absence Dates'] = ''
    
    return merged


def process_uploaded_files(
    files: Dict[str, Path]
) -> Tuple[pd.DataFrame, int, List[str]]:
    """
    Process and merge uploaded CSV/Excel files.
    
    Args:
        files: Dictionary mapping file types to file paths
    
    Returns:
        Tuple of (merged_dataframe, number_of_files_processed, error_messages)
    """
    errors = []
    grades_df = None
    attendance_df = None
    absences_df = None
    files_processed = 0
    
    # Process grades file
    if 'grades' in files:
        try:
            df = load_csv_file(files['grades'])
            is_valid, error_msg = validate_csv_file(df, 'grades')
            if is_valid:
                grades_df = df
                files_processed += 1
                logger.info(f"Processed grades file: {len(df)} records")
            else:
                errors.append(f"Grades file validation failed: {error_msg}")
        except Exception as e:
            errors.append(f"Error processing grades file: {str(e)}")
    
    # Process attendance file
    if 'attendance' in files:
        try:
            df = load_csv_file(files['attendance'])
            is_valid, error_msg = validate_csv_file(df, 'attendance')
            if is_valid:
                attendance_df = df
                files_processed += 1
                logger.info(f"Processed attendance file: {len(df)} records")
            else:
                errors.append(f"Attendance file validation failed: {error_msg}")
        except Exception as e:
            errors.append(f"Error processing attendance file: {str(e)}")
    
    # Process absences file
    if 'absences' in files:
        try:
            df = load_csv_file(files['absences'])
            is_valid, error_msg = validate_csv_file(df, 'absences')
            if is_valid:
                absences_df = df
                files_processed += 1
                logger.info(f"Processed absences file: {len(df)} records")
            else:
                errors.append(f"Absences file validation failed: {error_msg}")
        except Exception as e:
            errors.append(f"Error processing absences file: {str(e)}")
    
    if files_processed == 0:
        raise ValueError("No valid files were processed. " + "; ".join(errors))
    
    # Merge all data
    merged_df = merge_student_data(grades_df, attendance_df, absences_df)
    
    return merged_df, files_processed, errors

