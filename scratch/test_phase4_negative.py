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

neg_results = []

def run_neg_test(tc_id, title, method, url, payload=None, expected_status=[400]):
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
        print("EXCEPTION:", e)
        return

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
    print("VERDICT:", "PASS (Properly Rejected)" if passed else f"FAIL / DEFECT (Got {status_code}, expected {expected_status})")
    neg_results.append({
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

print("=== EXECUTING DTO VALIDATION & NEGATIVE TESTS ON ATTENDANCE 6 ===")

# 1. Break: Empty name
run_neg_test("POL-DTO-01", "Break Policy - Empty Name Object", "post",
             f"{base_url}/api/companies/{cid}/attpolicies/break",
             {"name": {}, "breaks": [{"name": "Tea", "type": "Paid", "durationMinutes": 15}]})

# 2. Break: Negative duration
run_neg_test("POL-DTO-15", "Break Policy - Negative DurationMinutes (-15)", "post",
             f"{base_url}/api/companies/{cid}/attpolicies/break",
             {"name": {"en": "Negative Break"}, "breaks": [{"name": "Tea", "type": "Paid", "durationMinutes": -15}]})

# 3. Break: Invalid BreakType enum
run_neg_test("POL-DTO-17", "Break Policy - Invalid BreakType Enum ('SuperPaid')", "post",
             f"{base_url}/api/companies/{cid}/attpolicies/break",
             {"name": {"en": "Invalid Enum"}, "breaks": [{"name": "Tea", "type": "SuperPaid", "durationMinutes": 15}]})

# 4. Grace Period: Negative LateCheckInGraceMinutes
run_neg_test("POL-DTO-24", "Grace Period - Negative LateCheckInGraceMinutes (-10)", "post",
             f"{base_url}/api/companies/{cid}/attpolicies/graceperiod",
             {"name": {"en": "Negative Grace"}, "lateCheckInGraceMinutes": -10, "earlyCheckOutGraceMinutes": 10})

# 5. Grace Period: Invalid DeviationPeriod enum
run_neg_test("POL-DTO-31", "Grace Period - Invalid DeviationPeriod Enum ('Yearly')", "post",
             f"{base_url}/api/companies/{cid}/attpolicies/graceperiod",
             {"name": {"en": "Invalid Period"}, "deviationPeriod": "Yearly"})

# 6. Grace Period: Negative deductionDays
run_neg_test("POL-DTO-36", "Grace Period - Negative DeductionDays (-1.5)", "post",
             f"{base_url}/api/companies/{cid}/attpolicies/graceperiod",
             {"name": {"en": "Negative Days"}, "deductionDays": -1.5})

# 7. Overtime: Negative BufferMinutes
run_neg_test("POL-DTO-46", "Overtime Policy - Negative BufferMinutes (-15)", "post",
             f"{base_url}/api/companies/{cid}/attpolicies/overtime",
             {"name": {"en": "Negative Buffer"}, "bufferMinutes": -15})

# 8. Overtime: Negative RateFormula multiplier
run_neg_test("POL-DTO-58", "Overtime Policy - Negative RateFormula Multiplier (-1.5)", "post",
             f"{base_url}/api/companies/{cid}/attpolicies/overtime",
             {"name": {"en": "Negative Multiplier"}, "rates": [{"dayRate": "WorkingDay", "rateFormula": -1.5}]})

# 9. Overtime: Invalid OvertimeDayRate enum
run_neg_test("POL-DTO-55", "Overtime Policy - Invalid OvertimeDayRate Enum ('WeekendDay')", "post",
             f"{base_url}/api/companies/{cid}/attpolicies/overtime",
             {"name": {"en": "Invalid Rate Enum"}, "rates": [{"dayRate": "WeekendDay", "rateFormula": 1.5}]})

# 10. GET non-existing policy ID
fake_id = "00000000-0000-0000-0000-000000009999"
run_neg_test("TC-POL-GET-02", "GET Non-Existing Policy ID", "get",
             f"{base_url}/api/companies/{cid}/attpolicies/{fake_id}",
             expected_status=[404])

# 11. Soft-Delete Existing Break Policy
break_id = "88a26cf7-54bc-42a1-9624-5fba47cc3587"
run_neg_test("TC-POL-DEL-01", "Soft-Delete Break Policy via PATCH /delete", "patch",
             f"{base_url}/api/companies/{cid}/attpolicies/{break_id}/delete",
             expected_status=[200, 204])

# 12. Retrieve Soft-Deleted Break Policy
run_neg_test("TC-POL-DEL-05", "GET Soft-Deleted Break Policy", "get",
             f"{base_url}/api/companies/{cid}/attpolicies/{break_id}",
             expected_status=[200, 404])

with open("scratch/phase4_negative_results.json", "w", encoding="utf-8") as f:
    json.dump(neg_results, f, indent=2, ensure_ascii=False)

print("\n=== PHASE 4 EXECUTION COMPLETE ===")

