import sys
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding='utf-8')

print("Starting generation of Policies - Manual DTO Validations sheet...")

# Headers matching 'CDWT - Manual DTO Validations' exactly
DTO_HEADERS = [
    "TC ID",
    "Category",
    "Policy Type",
    "Field Under Test",
    "Test Scenario / Edge Case",
    "HTTP Method",
    "Endpoint Route",
    "Sample Request Payload (JSON)",
    "Expected HTTP & Code",
    "Pri",
    "Automation Status",
    "Manual Status",
    "Actual HTTP Code",
    "Actual Server Response / Notes",
    "Known Defect / QA Reference"
]

print(f"DTO Headers count: {len(DTO_HEADERS)}")

