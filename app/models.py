"""
Data models for Student Risk Dashboard.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class StudentRiskPrediction(BaseModel):
    """Student risk prediction response."""
    student_id: str
    student_name: str
    program: Optional[str] = None
    grade: float
    attendance_rate: float
    risk_label: str
    recommended_action: str
    email: Optional[str] = None


class ExcelUploadResponse(BaseModel):
    """Response for Excel upload."""
    message: str
    students_processed: int
    at_risk_count: int
    safe_count: int
    avg_grade: float
    avg_attendance: float
    timestamp: datetime

