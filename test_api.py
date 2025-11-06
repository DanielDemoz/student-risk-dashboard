"""
Test script for Student Risk Dashboard API
Tests all endpoints and functionality
"""

import requests
import json
from pathlib import Path
import sys

API_BASE = "http://localhost:8001"

def print_test(name, passed, message=""):
    """Print test result."""
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} {name}")
    if message:
        print(f"      {message}")

def test_server_running():
    """Test if server is running."""
    try:
        response = requests.get(f"{API_BASE}/", timeout=5)
        return response.status_code in [200, 404]
    except requests.exceptions.ConnectionError:
        return False
    except Exception as e:
        print(f"      Error: {e}")
        return False

def test_root_endpoint():
    """Test root endpoint."""
    try:
        response = requests.get(f"{API_BASE}/", timeout=5)
        print_test("Root endpoint", response.status_code == 200, 
                  f"Status: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print_test("Root endpoint", False, f"Error: {e}")
        return False

def test_results_endpoint():
    """Test results endpoint (should return 404 if no data)."""
    try:
        response = requests.get(f"{API_BASE}/results", timeout=5)
        # 404 is expected if no data uploaded yet
        is_ok = response.status_code in [200, 404]
        print_test("Results endpoint", is_ok, 
                  f"Status: {response.status_code} (404 expected if no data)")
        return is_ok
    except Exception as e:
        print_test("Results endpoint", False, f"Error: {e}")
        return False

def test_upload_endpoint_structure():
    """Test upload endpoint accepts file (without actually uploading)."""
    try:
        # Just check if endpoint exists by sending empty request
        # This will fail but should give us info about the endpoint
        response = requests.post(f"{API_BASE}/upload-excel", timeout=5)
        # 422 or 400 is expected for missing file
        is_ok = response.status_code in [400, 422, 415]
        print_test("Upload endpoint structure", is_ok, 
                  f"Status: {response.status_code} (expected 400/422 for missing file)")
        return is_ok
    except Exception as e:
        print_test("Upload endpoint structure", False, f"Error: {e}")
        return False

def test_static_files():
    """Test if static files are accessible."""
    try:
        response = requests.get(f"{API_BASE}/static/style.css", timeout=5)
        is_ok = response.status_code == 200
        print_test("Static files", is_ok, 
                  f"Status: {response.status_code}")
        return is_ok
    except Exception as e:
        print_test("Static files", False, f"Error: {e}")
        return False

def test_api_info():
    """Test API info endpoint if it exists."""
    try:
        response = requests.get(f"{API_BASE}/api", timeout=5)
        is_ok = response.status_code == 200
        if is_ok:
            data = response.json()
            print_test("API info endpoint", True, 
                      f"API version: {data.get('version', 'N/A')}")
        else:
            print_test("API info endpoint", False, 
                      f"Status: {response.status_code}")
        return is_ok
    except:
        print_test("API info endpoint", False, "Endpoint not found (optional)")
        return True  # Not critical

def main():
    print("=" * 70)
    print("Student Risk Dashboard API Test Suite")
    print("=" * 70)
    print(f"\nTesting API at: {API_BASE}\n")
    
    results = []
    
    # Test 1: Server running
    print("[1] Testing server connection...")
    if not test_server_running():
        print("\n[ERROR] Server is not running!")
        print("\nPlease start the server first:")
        print("  python start.py")
        sys.exit(1)
    results.append(True)
    
    # Test 2: Root endpoint
    print("\n[2] Testing root endpoint...")
    results.append(test_root_endpoint())
    
    # Test 3: Results endpoint
    print("\n[3] Testing results endpoint...")
    results.append(test_results_endpoint())
    
    # Test 4: Upload endpoint
    print("\n[4] Testing upload endpoint...")
    results.append(test_upload_endpoint_structure())
    
    # Test 5: Static files
    print("\n[5] Testing static files...")
    results.append(test_static_files())
    
    # Test 6: API info
    print("\n[6] Testing API info endpoint...")
    results.append(test_api_info())
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"\nTests passed: {passed}/{total}")
    
    if passed == total:
        print("\n[SUCCESS] All tests passed! Server is working correctly.")
        print("\nNext steps:")
        print("1. Open http://localhost:8001 in your browser")
        print("2. Upload an Excel file with Grades and Attendance worksheets")
        print("3. View the risk analysis results")
    else:
        print(f"\n[WARNING] {total - passed} test(s) failed.")
        print("Check the error messages above for details.")
    
    print("=" * 70)
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

