import sys
import json
import requests
import uuid

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token_info = json.load(f)

token = token_info["access_token"]
cid = "3a249870-184c-0373-f344-015d602678d7" # Attendance 6

headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": "Attendance",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

base_url = "https://attendance2.dev.zoolwork.com"

results = []

def run_test(tc_id, title, method, url, payload=None, expected_status=[200]):
    print(f"\n" + "="*80)
    print(f"[{tc_id}] {title}")
    print(f"ROUTE: {method.upper()} {url}")
    if payload:
        print("REQUEST BODY:\n", json.dumps(payload, indent=2, ensure_ascii=False))
    
    resp = None
    try:
        if method.lower() == "get":
            resp = requests.get(url, headers=headers, timeout=15)
        elif method.lower() == "post":
            resp = requests.post(url, headers=headers, json=payload, timeout=15)
        elif method.lower() == "patch":
            resp = requests.patch(url, headers=headers, json=payload, timeout=15)
        elif method.lower() == "delete":
            resp = requests.delete(url, headers=headers, timeout=15)
    except Exception as e:
        print("EXECUTION EXCEPTION:", e)
        results.append({
            "tc_id": tc_id, "title": title, "method": method, "url": url,
            "status": "ERROR", "code": None, "response": str(e), "payload": payload
        })
        return None

    status_code = resp.status_code
    print(f"HTTP STATUS: {status_code}")
    res_data = None
    try:
        res_data = resp.json()
        print("RESPONSE BODY:\n", json.dumps(res_data, indent=2, ensure_ascii=False))
    except Exception:
        print("RESPONSE TEXT:\n", resp.text)
        res_data = resp.text

    passed = status_code in expected_status
    print("VERDICT:", "PASS" if passed else "FAIL (Unexpected Status)")
    results.append({
        "tc_id": tc_id,
        "title": title,
        "method": method,
        "url": url,
        "payload": payload,
        "code": status_code,
        "response": res_data,
        "passed": passed,
        "expected": expected_status
    })
    return res_data

# =========================================================================
# PHASE 1: POSITIVE POLICY CREATION (Break, Grace Period, Overtime)
# =========================================================================

# 1. Break Policy
p_break = {
    "name": {
        "en": "Attendance 6 Standard Break Policy",
        "ar": "سياسة الاستراحة القياسية للحضور 6"
    },
    "breaks": [
        {"name": "Morning Coffee", "type": "Paid", "durationMinutes": 15},
        {"name": "Lunch Break", "type": "Unpaid", "durationMinutes": 45},
        {"name": "Afternoon Tea", "type": "Paid", "durationMinutes": 15}
    ]
}
break_res = run_test("TC-POL-BRK-01", "Create Valid Break Policy (Omitted tenantName & id)", "post",
                     f"{base_url}/api/companies/{cid}/attpolicies/break", p_break, [200, 201])

# 2. Grace Period Policy
p_grace = {
    "name": {
        "en": "Attendance 6 Flexible Grace Period",
        "ar": "فترة السماح المرنة للحضور 6"
    },
    "lateCheckInGraceMinutes": 15,
    "earlyCheckOutGraceMinutes": 10,
    "deviationThreshold": 3,
    "deviationPeriod": "Monthly",
    "deductLeaveFrom": "AnnualLeave",
    "deductionDays": 0.5
}
grace_res = run_test("TC-POL-GRC-01", "Create Valid Grace Period Policy (Omitted tenantName & id)", "post",
                     f"{base_url}/api/companies/{cid}/attpolicies/graceperiod", p_grace, [200, 201])

# 3. Overtime Policy
p_ot = {
    "name": {
        "en": "Attendance 6 Standard Overtime Policy",
        "ar": "سياسة العمل الإضافي للحضور 6"
    },
    "overtimeRule": "AllExtraTime",
    "hasBufferBeforeOvertime": True,
    "bufferMinutes": 15,
    "rates": [
        {"dayRate": "WorkingDay", "rateFormula": 1.5},
        {"dayRate": "DayOff", "rateFormula": 2.0},
        {"dayRate": "Holiday", "rateFormula": 2.5}
    ]
}
ot_res = run_test("TC-POL-OVT-01", "Create Valid Overtime Policy (Omitted tenantName & id)", "post",
                  f"{base_url}/api/companies/{cid}/attpolicies/overtime", p_ot, [200, 201])

with open("scratch/phase1_creation_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\n=== PHASE 1 EXECUTION COMPLETE ===")

