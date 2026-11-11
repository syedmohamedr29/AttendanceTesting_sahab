# -*- coding: utf-8 -*-
"""
Full Automated Test Suite Runner for 'Holiday Calendar - Test Cases' (310 Test Cases)
Targets: Attendance 2 (3a247435-3cea-83ae-6a9f-6dda99f386a3) and Attendance 3 (3a247435-e31d-ef15-8cc9-62c587f4eb3f)
Microservice: https://attendance2.dev.zoolwork.com
"""

import requests
import json
import time
import sys
import uuid
import datetime
import urllib3
urllib3.disable_warnings()

sys.stdout.reconfigure(encoding='utf-8')

# Load Auth Token
with open('scratch/current_token.json', 'r', encoding='utf-8') as f:
    token_data = json.load(f)
token = token_data['access_token']

BASE_URL = "https://attendance2.dev.zoolwork.com"
COMPANY_URL = "https://company8.dev.zoolwork.com"

# Target Companies
ATT2_ID = "3a247435-3cea-83ae-6a9f-6dda99f386a3"
ATT3_ID = "3a247435-e31d-ef15-8cc9-62c587f4eb3f"
TENANT_ID = "3a24741e-2667-1223-f12e-62a69fab3838"

# Scoped Holiday Type IDs
ATT2_HTYPES = {
    "public": "3a247435-3cfa-7c43-8e74-eda55a21e647",
    "religious": "3a247435-3cfa-7cce-156d-548e9bae873f",
    "national": "3a247435-3cfa-45b2-7a78-09ba99eac996",
    "bank": "3a247435-3cfa-66f0-3bd2-7ee4d0775d9f",
    "gazette": "3a247435-3cfa-054b-ef49-92891543ac60"
}

ATT3_HTYPES = {
    "public": "3a247435-e32a-b077-aaf2-731b6165321d",
    "religious": "3a247435-e32a-6c46-5911-d75495b1d40d",
    "national": "3a247435-e32b-24be-bce7-f3f2e2773379",
    "bank": "3a247435-e32b-89aa-e8b6-3190f73d6790",
    "gazette": "3a247435-e32b-0304-f667-b68e43ccab91"
}

headers_std = {
    "Authorization": f"Bearer {token}",
    "__tenant": "Attendance",
    "Content-Type": "application/json"
}

# Load the 310 test cases
with open('scratch/holiday_test_cases_dump.json', 'r', encoding='utf-8') as f:
    test_cases = json.load(f)

print(f"Loaded {len(test_cases)} test cases to execute.")

results = []
pass_count = 0
fail_count = 0

# Helper to run a test
def record_result(tc_info, actual_status, response_text, latency_ms, passed, defect_notes=""):
    global pass_count, fail_count
    if passed:
        pass_count += 1
        status_str = "Pass"
    else:
        fail_count += 1
        status_str = "Fail"
    
    clean_text = response_text.replace('\n', ' ')[:150]
    remarks = f"HTTP {actual_status} | {latency_ms}ms"
    if defect_notes:
        remarks += f" | {defect_notes}"
    elif not passed:
        remarks += f" | {clean_text}"
    else:
        remarks += f" | Verified on Attendance 2 / Attendance 3"
        
    res_entry = {
        "tc": tc_info["tc"],
        "row": tc_info["row"],
        "section": tc_info["section"],
        "scenario": tc_info["scenario"],
        "status": status_str,
        "actual_status": actual_status,
        "latency_ms": latency_ms,
        "remarks": remarks,
        "response_excerpt": clean_text
    }
    results.append(res_entry)
    print(f"[{status_str:4s}] {tc_info['tc']}: {tc_info['scenario'][:50]} -> HTTP {actual_status} ({latency_ms}ms)")

# Execute test suite logic
# Let's write the execution loop in detail

