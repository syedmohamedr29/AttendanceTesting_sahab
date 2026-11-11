import json
import os
import sys
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

sys.stdout.reconfigure(encoding='utf-8')

# The 27 Mandatory Columns specified by User Master Prompt
COLUMNS = [
    "Test Case ID",
    "Requirement ID",
    "Module Name",
    "API Endpoint",
    "HTTP Method",
    "Scenario Category",
    "Test Scenario",
    "Test Case Title",
    "Preconditions",
    "Request Headers",
    "Request Payload",
    "Test Data",
    "Manual Execution Steps",
    "Expected HTTP Status Code",
    "Expected Response Body",
    "MongoDB Database Name",
    "MongoDB Collection Name",
    "MongoDB Validation Scenario",
    "MongoDB Compass Filter Query",
    "Expected MongoDB Result",
    "Actual API Result",
    "Actual MongoDB Result",
    "API Test Status",
    "Database Test Status",
    "Overall Test Status",
    "Priority",
    "Remarks"
]

print(f"Columns initialized: {len(COLUMNS)}")

