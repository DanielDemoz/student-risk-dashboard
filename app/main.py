"""
FastAPI Student Risk Dashboard - Clean Version
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import List
import pandas as pd

from fastapi import FastAPI, File, UploadFile, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.models import StudentRiskPrediction, ExcelUploadResponse

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import after path setup
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.data_preprocessing import process_excel_file

# Create FastAPI app
app = FastAPI(title="Student Risk Dashboard API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure directories exist
Path("data").mkdir(exist_ok=True)
Path("static").mkdir(exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve main dashboard."""
    html_path = Path(__file__).parent.parent / "static" / "index.html"
    if html_path.exists():
        return FileResponse(html_path)
    return HTMLResponse("<h1>Dashboard not found. Please check static/index.html</h1>")


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/upload-excel", response_model=ExcelUploadResponse)
async def upload_excel(file: UploadFile = File(...), train_model: bool = Query(False)):
    """Upload and process Excel file."""
    if not file.filename or not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Must upload Excel file (.xlsx or .xls)")
    
    try:
        # Save file
        data_dir = Path("data")
        file_path = data_dir / file.filename
        content = await file.read()
        file_path.write_bytes(content)
        
        # Process file
        df, stats = process_excel_file(file_path)
        
        # Save results
        output_path = data_dir / "processed_students.csv"
        df.to_csv(output_path, index=False)
        
        return ExcelUploadResponse(
            message=f"Processed {len(df)} students successfully",
            students_processed=len(df),
            at_risk_count=stats['at_risk_count'],
            safe_count=stats['safe_count'],
            avg_grade=round(stats['avg_grade'], 2),
            avg_attendance=round(stats['avg_attendance'], 2),
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/results", response_model=List[StudentRiskPrediction])
async def get_results(at_risk_only: bool = Query(False)):
    """Get processed results."""
    output_path = Path("data") / "processed_students.csv"
    
    if not output_path.exists():
        raise HTTPException(status_code=404, detail="No data found. Upload Excel file first.")
    
    df = pd.read_csv(output_path)
    
    if at_risk_only:
        df = df[df['risk_label'].isin(['At Risk', 'High Risk'])]
    
    # Sort: High Risk first, then At Risk, then Safe
    df['sort_order'] = df['risk_label'].map({'High Risk': 0, 'At Risk': 1, 'Safe': 2})
    df = df.sort_values('sort_order').drop('sort_order', axis=1)
    
    results = []
    for _, row in df.iterrows():
        results.append(StudentRiskPrediction(
            student_id=str(row['student_id']),
            student_name=str(row['student_name']),
            program=str(row.get('program', 'Unknown')),
            grade=float(row['grade']),
            attendance_rate=float(row['attendance_rate']),
            risk_label=str(row['risk_label']),
            recommended_action=str(row['recommended_action']),
            email=str(row.get('email', ''))
        ))
    
    return results


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)

