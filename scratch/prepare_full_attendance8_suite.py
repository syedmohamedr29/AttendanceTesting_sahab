import requests
import json
import time
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment
import sys

sys.stdout.reconfigure(encoding='utf-8')

company_id = "3a249871-7a8d-dec5-2d72-47795dd2662d" # Attendance 8

with open("scratch/current_token.json") as f:
    token_data = json.load(f)

token = token_data["access_token"]
tenant = "Attendance"

base_url = "https://attendance2.dev.zoolwork.com"
auth_headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": tenant,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

print(f"Preparing full test suite execution for Company: Attendance 8 ({company_id})...")

