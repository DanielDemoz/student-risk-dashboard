"""
Example script demonstrating how to use the Risk Dashboard API.
This script shows how to interact with the API programmatically.
"""

import requests
import json
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000"

def print_response(title, response):
    """Pretty print API response."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(json.dumps(response, indent=2, default=str))


def example_upload_files():
    """Example: Upload CSV files to the API."""
    print("\n📤 Example: Uploading files...")
    
    data_dir = Path("data")
    
    files = {}
    if (data_dir / "grades.csv").exists():
        files['grades'] = open(data_dir / "grades.csv", 'rb')
    if (data_dir / "attendance.csv").exists():
        files['attendance'] = open(data_dir / "attendance.csv", 'rb')
    if (data_dir / "absences.csv").exists():
        files['absences'] = open(data_dir / "absences.csv", 'rb')
    
    if not files:
        print("❌ No data files found in data/ directory.")
        print("   Run 'python create_sample_data.py' first to generate sample data.")
        return
    
    try:
        response = requests.post(f"{BASE_URL}/upload", files=files)
        print_response("Upload Response", response.json())
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure the API server is running:")
        print("   python start_server.py")
    finally:
        for f in files.values():
            f.close()


def example_get_all_students():
    """Example: Get all student risk data."""
    print("\n📊 Example: Fetching all students...")
    
    try:
        response = requests.get(f"{BASE_URL}/students")
        students = response.json()
        print_response(f"All Students ({len(students)} total)", students[:5])  # Show first 5
        print(f"\n... and {len(students) - 5} more students")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure the API server is running.")


def example_get_student_by_id():
    """Example: Get individual student by ID."""
    print("\n👤 Example: Fetching student by ID...")
    
    student_id = "5682941"  # Replace with actual student ID
    
    try:
        response = requests.get(f"{BASE_URL}/students/{student_id}")
        print_response(f"Student {student_id}", response.json())
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure the API server is running.")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"❌ Student {student_id} not found.")


def example_get_summary():
    """Example: Get risk summary statistics."""
    print("\n📈 Example: Fetching risk summary...")
    
    try:
        response = requests.get(f"{BASE_URL}/summary")
        print_response("Risk Summary", response.json())
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure the API server is running.")


def example_filter_by_program():
    """Example: Filter students by program."""
    print("\n🎓 Example: Filtering by program...")
    
    program = "Accounting, Payroll and Tax"
    
    try:
        response = requests.get(f"{BASE_URL}/students", params={"program": program})
        students = response.json()
        print_response(f"Students in {program} ({len(students)} total)", students[:3])
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure the API server is running.")


def example_filter_by_risk_level():
    """Example: Filter students by risk level."""
    print("\n⚠️ Example: Filtering by risk level...")
    
    risk_level = "High"
    
    try:
        response = requests.get(f"{BASE_URL}/students", params={"risk_level": risk_level})
        students = response.json()
        print_response(f"High Risk Students ({len(students)} total)", students[:3])
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure the API server is running.")


def example_get_programs():
    """Example: Get per-program summary."""
    print("\n📚 Example: Fetching program summaries...")
    
    try:
        response = requests.get(f"{BASE_URL}/programs")
        print_response("Program Summaries", response.json())
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure the API server is running.")


def example_train_model():
    """Example: Train ML model (optional)."""
    print("\n🤖 Example: Training ML model...")
    
    try:
        response = requests.post(f"{BASE_URL}/train-model")
        print_response("Model Training Response", response.json())
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure the API server is running.")


if __name__ == "__main__":
    print("="*60)
    print("AI Attendance & Performance Risk Dashboard API")
    print("Example Usage Script")
    print("="*60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/")
        print("✅ API server is running!")
        print_response("API Information", response.json())
    except requests.exceptions.ConnectionError:
        print("❌ API server is not running.")
        print("\nPlease start the server first:")
        print("   python start_server.py")
        print("\nOr run:")
        print("   uvicorn app.main:app --reload")
        exit(1)
    
    # Run examples
    example_upload_files()
    example_get_summary()
    example_get_all_students()
    example_get_student_by_id()
    example_filter_by_program()
    example_filter_by_risk_level()
    example_get_programs()
    # example_train_model()  # Uncomment if you want to train the model
    
    print("\n" + "="*60)
    print("✅ Examples completed!")
    print("="*60)

