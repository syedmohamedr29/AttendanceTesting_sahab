import os
import sys
import json
import time
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding='utf-8')

# Authentication & Configuration
with open('scratch/current_token.json', 'r', encoding='utf-8') as f:
    token_data = json.load(f)
token = token_data.get('access_token')

company_id = "3a249871-7a8d-dec5-2d72-47795dd2662d"
loc_id = "3a24d629-0d56-a428-baa1-98493a77e614"

base_url = "https://attendance2.dev.zoolwork.com"
post_endpoint = f"{base_url}/api/companies/{company_id}/worktemplates/fixed?locationId={loc_id}"
patch_base_endpoint = f"{base_url}/api/companies/{company_id}/worktemplates/fixed"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Standard Baseline Payload - ShortCode MUST be exactly 7 letters or digits
def get_p01_baseline(short_code="FXPOS01"):
    return {
        "templateName": {
            "en": f"Standard Fixed Shift {short_code}",
            "ar": f"وردية العمل الثابتة {short_code}"
        },
        "shortCode": short_code,
        "templateType": 1,
        "totalWorkDurationInMinutes": 2700,
        "totalWorkingDays": 5,
        "totalDaysOff": 2,
        "timeZoneId": "Asia/Riyadh",
        "fixedTimeSlots": [
            {
                "workDurationInMinutes": 540,
                "dayEnum": 1,
                "isWorkingDay": True,
                "recurrenceOfMonth": [1, 2, 3, 4, 5],
                "startTime": "08:00:00",
                "endTime": "17:00:00"
            },
            {
                "workDurationInMinutes": 540,
                "dayEnum": 2,
                "isWorkingDay": True,
                "recurrenceOfMonth": [1, 2, 3, 4, 5],
                "startTime": "08:00:00",
                "endTime": "17:00:00"
            },
            {
                "workDurationInMinutes": 540,
                "dayEnum": 3,
                "isWorkingDay": True,
                "recurrenceOfMonth": [1, 2, 3, 4, 5],
                "startTime": "08:00:00",
                "endTime": "17:00:00"
            },
            {
                "workDurationInMinutes": 540,
                "dayEnum": 4,
                "isWorkingDay": True,
                "recurrenceOfMonth": [1, 2, 3, 4, 5],
                "startTime": "08:00:00",
                "endTime": "17:00:00"
            },
            {
                "workDurationInMinutes": 540,
                "dayEnum": 5,
                "isWorkingDay": True,
                "recurrenceOfMonth": [1, 2, 3, 4, 5],
                "startTime": "08:00:00",
                "endTime": "17:00:00"
            },
            {
                "workDurationInMinutes": 0,
                "dayEnum": 6,
                "isWorkingDay": False,
                "recurrenceOfMonth": [],
                "startTime": "00:00:00",
                "endTime": "00:00:00"
            },
            {
                "workDurationInMinutes": 0,
                "dayEnum": 7,
                "isWorkingDay": False,
                "recurrenceOfMonth": [],
                "startTime": "00:00:00",
                "endTime": "00:00:00"
            }
        ]
    }

results = []

def record_test(test_id, category, method, url, payload, resp, start_time, notes=""):
    elapsed_ms = int((time.time() - start_time) * 1000)
    status_code = resp.status_code if resp is not None else 0
    resp_text = resp.text if resp is not None else ""
    
    error_code = None
    error_message = None
    validation_errors = None
    created_id = None
    
    try:
        data = resp.json() if resp is not None else {}
        if isinstance(data, dict):
            created_id = data.get('id')
            if 'error' in data:
                err = data['error']
                error_code = err.get('code')
                error_message = err.get('message')
                validation_errors = err.get('validationErrors')
    except Exception:
        pass
    
    # Determination of Pass/Fail
    if category.startswith("POST Positive") or category.startswith("PATCH Positive"):
        passed = (status_code in [200, 201])
    else: # Negative & BVA (boundary invalid)
        passed = (status_code >= 400)

    res = {
        "test_id": test_id,
        "category": category,
        "method": method,
        "url": url,
        "payload": payload,
        "status_code": status_code,
        "elapsed_ms": elapsed_ms,
        "error_code": error_code,
        "error_message": error_message,
        "validation_errors": validation_errors,
        "created_id": created_id,
        "passed": passed,
        "notes": notes,
        "response_summary": (resp_text[:300] + '...') if len(resp_text) > 300 else resp_text
    }
    results.append(res)
    mark = "PASS" if passed else "FAIL"
    detail_str = f" | {error_code}" if error_code else ""
    if error_message:
        detail_str += f": {error_message}"
    print(f"[{test_id}] {category} -> HTTP {status_code} ({mark}) [{elapsed_ms}ms]{detail_str}", flush=True)
    return res

print("=====================================================================", flush=True)
print("EXECUTING REFINED FIXED WORK TEMPLATE VALIDATION RUNNER V2 (LOC 1)", flush=True)
print("=====================================================================", flush=True)

# -------------------------------------------------------------------
# 1. POST POSITIVE SCENARIOS (7-Char Unique Short Codes)
# -------------------------------------------------------------------
print("\n--- 1. POST POSITIVE SCENARIOS ---", flush=True)

# P01: Standard 5-day template
ts = time.time()
p01_payload = get_p01_baseline("FXPOS01")
r = requests.post(post_endpoint, json=p01_payload, headers=headers, verify=False, timeout=30)
res_p01 = record_test("POST-P01", "POST Positive", "POST", post_endpoint, p01_payload, r, ts, "Standard 5-day template (Sun-Thu, 08:00-17:00, 2700 min)")
p01_created_id = res_p01.get("created_id")

# P02: Six working days
ts = time.time()
p02_payload = get_p01_baseline("FXPOS02")
p02_payload["totalWorkDurationInMinutes"] = 3240
p02_payload["totalWorkingDays"] = 6
p02_payload["totalDaysOff"] = 1
p02_payload["fixedTimeSlots"][5] = {
    "workDurationInMinutes": 540,
    "dayEnum": 6,
    "isWorkingDay": True,
    "recurrenceOfMonth": [1, 2, 3, 4, 5],
    "startTime": "08:00:00",
    "endTime": "17:00:00"
}
r = requests.post(post_endpoint, json=p02_payload, headers=headers, verify=False, timeout=30)
record_test("POST-P02", "POST Positive", "POST", post_endpoint, p02_payload, r, ts, "Six working days (Sun-Fri, 3240 min)")

# P03: Four working days
ts = time.time()
p03_payload = get_p01_baseline("FXPOS03")
p03_payload["totalWorkDurationInMinutes"] = 2160
p03_payload["totalWorkingDays"] = 4
p03_payload["totalDaysOff"] = 3
p03_payload["fixedTimeSlots"][0] = {
    "workDurationInMinutes": 0,
    "dayEnum": 1,
    "isWorkingDay": False,
    "recurrenceOfMonth": [],
    "startTime": "00:00:00",
    "endTime": "00:00:00"
}
r = requests.post(post_endpoint, json=p03_payload, headers=headers, verify=False, timeout=30)
record_test("POST-P03", "POST Positive", "POST", post_endpoint, p03_payload, r, ts, "Four working days (Mon-Thu, 2160 min, Sun off with 0 duration)")

# P04: Different working durations
ts = time.time()
p04_payload = get_p01_baseline("FXPOS04")
p04_payload["totalWorkDurationInMinutes"] = 2550
p04_payload["fixedTimeSlots"][0] = {
    "workDurationInMinutes": 480,
    "dayEnum": 1,
    "isWorkingDay": True,
    "recurrenceOfMonth": [1, 2, 3, 4, 5],
    "startTime": "08:00:00",
    "endTime": "16:00:00"
}
p04_payload["fixedTimeSlots"][1] = {
    "workDurationInMinutes": 510,
    "dayEnum": 2,
    "isWorkingDay": True,
    "recurrenceOfMonth": [1, 2, 3, 4, 5],
    "startTime": "08:00:00",
    "endTime": "16:30:00"
}
p04_payload["fixedTimeSlots"][4] = {
    "workDurationInMinutes": 480,
    "dayEnum": 5,
    "isWorkingDay": True,
    "recurrenceOfMonth": [1, 2, 3, 4, 5],
    "startTime": "08:00:00",
    "endTime": "16:00:00"
}
r = requests.post(post_endpoint, json=p04_payload, headers=headers, verify=False, timeout=30)
record_test("POST-P04", "POST Positive", "POST", post_endpoint, p04_payload, r, ts, "Different durations per day (480, 510, 540, 540, 480 = 2550 min)")

# P05: Selected monthly recurrences
ts = time.time()
p05_payload = get_p01_baseline("FXPOS05")
p05_payload["fixedTimeSlots"][0]["recurrenceOfMonth"] = [1, 3, 5]
r = requests.post(post_endpoint, json=p05_payload, headers=headers, verify=False, timeout=30)
record_test("POST-P05", "POST Positive", "POST", post_endpoint, p05_payload, r, ts, "Selected monthly recurrences [1, 3, 5] on Sunday")

# P06: India timezone
ts = time.time()
p06_payload = get_p01_baseline("FXPOS06")
p06_payload["timeZoneId"] = "Asia/Kolkata"
r = requests.post(post_endpoint, json=p06_payload, headers=headers, verify=False, timeout=30)
record_test("POST-P06", "POST Positive", "POST", post_endpoint, p06_payload, r, ts, "India timezone (Asia/Kolkata)")

# P07: One-minute duration boundary
ts = time.time()
p07_payload = get_p01_baseline("FXPOS07")
p07_payload["totalWorkDurationInMinutes"] = 5
for i in range(5):
    p07_payload["fixedTimeSlots"][i]["workDurationInMinutes"] = 1
    p07_payload["fixedTimeSlots"][i]["startTime"] = "08:00:00"
    p07_payload["fixedTimeSlots"][i]["endTime"] = "08:01:00"
r = requests.post(post_endpoint, json=p07_payload, headers=headers, verify=False, timeout=30)
record_test("POST-P07", "POST Positive", "POST", post_endpoint, p07_payload, r, ts, "One-minute duration boundary (1 min/day, total 5 min)")

# P08: Twelve-hour duration candidate
ts = time.time()
p08_payload = get_p01_baseline("FXPOS08")
p08_payload["totalWorkDurationInMinutes"] = 3600
for i in range(5):
    p08_payload["fixedTimeSlots"][i]["workDurationInMinutes"] = 720
    p08_payload["fixedTimeSlots"][i]["startTime"] = "08:00:00"
    p08_payload["fixedTimeSlots"][i]["endTime"] = "20:00:00"
r = requests.post(post_endpoint, json=p08_payload, headers=headers, verify=False, timeout=30)
record_test("POST-P08", "POST Positive", "POST", post_endpoint, p08_payload, r, ts, "Twelve-hour duration candidate (720 min/day, total 3600 min)")

# P09: Localized naming
ts = time.time()
p09_payload = get_p01_baseline("FXPOS09")
p09_payload["templateName"] = {
    "en": "Executive Fixed Morning Shift",
    "ar": "وردية الصباح الثابتة التنفيذية"
}
r = requests.post(post_endpoint, json=p09_payload, headers=headers, verify=False, timeout=30)
record_test("POST-P09", "POST Positive", "POST", post_endpoint, p09_payload, r, ts, "Bilingual localized name creation")


# -------------------------------------------------------------------
# 2. POST NEGATIVE SCENARIOS (7-Char Base to isolate specific rule)
# -------------------------------------------------------------------
print("\n--- 2. POST NEGATIVE SCENARIOS ---", flush=True)

# N01: Empty template name
ts = time.time()
n01 = get_p01_baseline("FXNEG01")
n01["templateName"] = {"en": "", "ar": ""}
r = requests.post(post_endpoint, json=n01, headers=headers, verify=False, timeout=30)
record_test("POST-N01", "POST Negative", "POST", post_endpoint, n01, r, ts, "Empty template name")

# N02: Null template name
ts = time.time()
n02 = get_p01_baseline("FXNEG02")
n02["templateName"] = None
r = requests.post(post_endpoint, json=n02, headers=headers, verify=False, timeout=30)
record_test("POST-N02", "POST Negative", "POST", post_endpoint, n02, r, ts, "Null template name")

# N03: Empty short code
ts = time.time()
n03 = get_p01_baseline("FXNEG03")
n03["shortCode"] = ""
r = requests.post(post_endpoint, json=n03, headers=headers, verify=False, timeout=30)
record_test("POST-N03", "POST Negative", "POST", post_endpoint, n03, r, ts, "Empty short code")

# N04: Duplicate short code (7 chars: use FXL0101 which exists in Loc 1)
ts = time.time()
n04 = get_p01_baseline("FXL0101")
r = requests.post(post_endpoint, json=n04, headers=headers, verify=False, timeout=30)
record_test("POST-N04", "POST Negative", "POST", post_endpoint, n04, r, ts, "Duplicate short code (existing FXL0101)")

# N05: Invalid template type
ts = time.time()
n05 = get_p01_baseline("FXNEG05")
n05["templateType"] = 999
r = requests.post(post_endpoint, json=n05, headers=headers, verify=False, timeout=30)
record_test("POST-N05", "POST Negative", "POST", post_endpoint, n05, r, ts, "Invalid template type (999)")

# N06: Invalid day enum
ts = time.time()
n06 = get_p01_baseline("FXNEG06")
n06["fixedTimeSlots"][0]["dayEnum"] = 8
r = requests.post(post_endpoint, json=n06, headers=headers, verify=False, timeout=30)
record_test("POST-N06", "POST Negative", "POST", post_endpoint, n06, r, ts, "Invalid dayEnum (8)")

# N07: Invalid recurrence
ts = time.time()
n07 = get_p01_baseline("FXNEG07")
n07["fixedTimeSlots"][0]["recurrenceOfMonth"] = [6]
r = requests.post(post_endpoint, json=n07, headers=headers, verify=False, timeout=30)
record_test("POST-N07", "POST Negative", "POST", post_endpoint, n07, r, ts, "Invalid recurrenceOfMonth ([6])")

# N08: Negative duration
ts = time.time()
n08 = get_p01_baseline("FXNEG08")
n08["fixedTimeSlots"][0]["workDurationInMinutes"] = -540
r = requests.post(post_endpoint, json=n08, headers=headers, verify=False, timeout=30)
record_test("POST-N08", "POST Negative", "POST", post_endpoint, n08, r, ts, "Negative work duration (-540)")

# N09: Decimal duration
ts = time.time()
n09 = get_p01_baseline("FXNEG09")
n09["fixedTimeSlots"][0]["workDurationInMinutes"] = 540.5
r = requests.post(post_endpoint, json=n09, headers=headers, verify=False, timeout=30)
record_test("POST-N09", "POST Negative", "POST", post_endpoint, n09, r, ts, "Decimal work duration (540.5)")

# N10: Invalid start time
ts = time.time()
n10 = get_p01_baseline("FXNEG10")
n10["fixedTimeSlots"][0]["startTime"] = "25:00:00"
r = requests.post(post_endpoint, json=n10, headers=headers, verify=False, timeout=30)
record_test("POST-N10", "POST Negative", "POST", post_endpoint, n10, r, ts, "Invalid start time (25:00:00)")

# N11: End time earlier than start time
ts = time.time()
n11 = get_p01_baseline("FXNEG11")
n11["fixedTimeSlots"][0]["startTime"] = "17:00:00"
n11["fixedTimeSlots"][0]["endTime"] = "08:00:00"
r = requests.post(post_endpoint, json=n11, headers=headers, verify=False, timeout=30)
record_test("POST-N11", "POST Negative", "POST", post_endpoint, n11, r, ts, "End time earlier than start time (17:00 -> 08:00)")

# N12: Invalid timezone
ts = time.time()
n12 = get_p01_baseline("FXNEG12")
n12["timeZoneId"] = "Invalid/Timezone"
r = requests.post(post_endpoint, json=n12, headers=headers, verify=False, timeout=30)
record_test("POST-N12", "POST Negative", "POST", post_endpoint, n12, r, ts, "Invalid timezone (Invalid/Timezone)")

# N13: Incorrect total duration
ts = time.time()
n13 = get_p01_baseline("FXNEG13")
n13["totalWorkDurationInMinutes"] = 3000
r = requests.post(post_endpoint, json=n13, headers=headers, verify=False, timeout=30)
record_test("POST-N13", "POST Negative", "POST", post_endpoint, n13, r, ts, "Incorrect total duration (declared 3000, sum 2700)")

# N14: Incorrect working-day count
ts = time.time()
n14 = get_p01_baseline("FXNEG14")
n14["totalWorkingDays"] = 6
r = requests.post(post_endpoint, json=n14, headers=headers, verify=False, timeout=30)
record_test("POST-N14", "POST Negative", "POST", post_endpoint, n14, r, ts, "Incorrect working-day count (declared 6, actual 5)")

# N15: Incorrect days-off count
ts = time.time()
n15 = get_p01_baseline("FXNEG15")
n15["totalDaysOff"] = 3
r = requests.post(post_endpoint, json=n15, headers=headers, verify=False, timeout=30)
record_test("POST-N15", "POST Negative", "POST", post_endpoint, n15, r, ts, "Incorrect days-off count (declared 3, actual 2)")

# N16: Working day with zero duration
ts = time.time()
n16 = get_p01_baseline("FXNEG16")
n16["fixedTimeSlots"][0]["workDurationInMinutes"] = 0
n16["fixedTimeSlots"][0]["isWorkingDay"] = True
n16["fixedTimeSlots"][0]["startTime"] = "08:00:00"
n16["fixedTimeSlots"][0]["endTime"] = "17:00:00"
r = requests.post(post_endpoint, json=n16, headers=headers, verify=False, timeout=30)
record_test("POST-N16", "POST Negative", "POST", post_endpoint, n16, r, ts, "Working day with zero duration (0 min, 08:00-17:00)")

# N17: Off-day with non-zero duration
ts = time.time()
n17 = get_p01_baseline("FXNEG17")
n17["fixedTimeSlots"][6]["workDurationInMinutes"] = 540
n17["fixedTimeSlots"][6]["isWorkingDay"] = False
n17["fixedTimeSlots"][6]["startTime"] = "08:00:00"
n17["fixedTimeSlots"][6]["endTime"] = "17:00:00"
r = requests.post(post_endpoint, json=n17, headers=headers, verify=False, timeout=30)
record_test("POST-N17", "POST Negative", "POST", post_endpoint, n17, r, ts, "Off-day with non-zero duration (isWorkingDay=False, 540 min)")

# N18: Duplicate overlapping day
ts = time.time()
n18 = get_p01_baseline("FXNEG18")
n18["fixedTimeSlots"].append({
    "workDurationInMinutes": 540,
    "dayEnum": 2,
    "isWorkingDay": True,
    "recurrenceOfMonth": [3, 4],
    "startTime": "08:00:00",
    "endTime": "17:00:00"
})
r = requests.post(post_endpoint, json=n18, headers=headers, verify=False, timeout=30)
record_test("POST-N18", "POST Negative", "POST", post_endpoint, n18, r, ts, "Duplicate overlapping day (two Monday slots)")

# N19: Wrong data type for isWorkingDay (string "true")
ts = time.time()
n19 = get_p01_baseline("FXNEG19")
n19_str = json.dumps(n19).replace('"isWorkingDay": true', '"isWorkingDay": "true"', 1)
r = requests.post(post_endpoint, data=n19_str, headers=headers, verify=False, timeout=30)
record_test("POST-N19", "POST Negative", "POST", post_endpoint, n19_str, r, ts, "Wrong data type for isWorkingDay (string 'true')")

# N20: Wrong data type for duration (string "540")
ts = time.time()
n20 = get_p01_baseline("FXNEG20")
n20_str = json.dumps(n20).replace('"workDurationInMinutes": 540', '"workDurationInMinutes": "540"', 1)
r = requests.post(post_endpoint, data=n20_str, headers=headers, verify=False, timeout=30)
record_test("POST-N20", "POST Negative", "POST", post_endpoint, n20_str, r, ts, "Wrong data type for workDurationInMinutes (string '540')")

# N21: Short code length below 7 chars (6 chars)
ts = time.time()
n21 = get_p01_baseline("FX0001")
r = requests.post(post_endpoint, json=n21, headers=headers, verify=False, timeout=30)
record_test("POST-N21", "POST Negative", "POST", post_endpoint, n21, r, ts, "ShortCode below 7 chars (6 chars: 'FX0001')")

# N22: Short code length above 7 chars (8 chars)
ts = time.time()
n22 = get_p01_baseline("FX000001")
r = requests.post(post_endpoint, json=n22, headers=headers, verify=False, timeout=30)
record_test("POST-N22", "POST Negative", "POST", post_endpoint, n22, r, ts, "ShortCode above 7 chars (8 chars: 'FX000001')")

# N23: Short code with special characters
ts = time.time()
n23 = get_p01_baseline("FX-0001")
r = requests.post(post_endpoint, json=n23, headers=headers, verify=False, timeout=30)
record_test("POST-N23", "POST Negative", "POST", post_endpoint, n23, r, ts, "ShortCode with hyphen ('FX-0001')")


# -------------------------------------------------------------------
# 3. PATCH POSITIVE SCENARIOS (Preserving ShortCode to test true update)
# -------------------------------------------------------------------
print("\n--- 3. PATCH POSITIVE SCENARIOS ---", flush=True)

# Select target template for patch:
# Prefer newly created P01 template, else fallback to existing c9e00652-eae5-429a-bef0-4d4ddf9e0a0f
target_patch_id = p01_created_id or "c9e00652-eae5-429a-bef0-4d4ddf9e0a0f"
target_shortcode = "FXPOS01" if p01_created_id else "FXL0101"
patch_url = f"{patch_base_endpoint}/{target_patch_id}?locationId={loc_id}"
print(f"Target Template ID for PATCH: {target_patch_id} (shortCode: {target_shortcode})", flush=True)

# PATCH-P01: Update template name
ts = time.time()
patch_p01 = get_p01_baseline(target_shortcode)
patch_p01["templateName"] = {
    "en": f"Standard Fixed Shift {target_shortcode} Updated",
    "ar": f"وردية العمل الثابتة {target_shortcode} محدثة"
}
r = requests.patch(patch_url, json=patch_p01, headers=headers, verify=False, timeout=30)
record_test("PATCH-P01", "PATCH Positive", "PATCH", patch_url, patch_p01, r, ts, "Update template name (en & ar)")

# PATCH-P02: Update working hours
ts = time.time()
patch_p02 = get_p01_baseline(target_shortcode)
for i in range(5):
    patch_p02["fixedTimeSlots"][i]["startTime"] = "09:00:00"
    patch_p02["fixedTimeSlots"][i]["endTime"] = "18:00:00"
r = requests.patch(patch_url, json=patch_p02, headers=headers, verify=False, timeout=30)
record_test("PATCH-P02", "PATCH Positive", "PATCH", patch_url, patch_p02, r, ts, "Update working hours (09:00-18:00)")

# PATCH-P03: Update to six working days
ts = time.time()
patch_p03 = get_p01_baseline(target_shortcode)
patch_p03["totalWorkDurationInMinutes"] = 3240
patch_p03["totalWorkingDays"] = 6
patch_p03["totalDaysOff"] = 1
patch_p03["fixedTimeSlots"][5] = {
    "workDurationInMinutes": 540,
    "dayEnum": 6,
    "isWorkingDay": True,
    "recurrenceOfMonth": [1, 2, 3, 4, 5],
    "startTime": "08:00:00",
    "endTime": "17:00:00"
}
r = requests.patch(patch_url, json=patch_p03, headers=headers, verify=False, timeout=30)
record_test("PATCH-P03", "PATCH Positive", "PATCH", patch_url, patch_p03, r, ts, "Update schedule to 6 working days (3240 min)")

# PATCH-P04: Update to four working days
ts = time.time()
patch_p04 = get_p01_baseline(target_shortcode)
patch_p04["totalWorkDurationInMinutes"] = 2160
patch_p04["totalWorkingDays"] = 4
patch_p04["totalDaysOff"] = 3
patch_p04["fixedTimeSlots"][0] = {
    "workDurationInMinutes": 0,
    "dayEnum": 1,
    "isWorkingDay": False,
    "recurrenceOfMonth": [],
    "startTime": "00:00:00",
    "endTime": "00:00:00"
}
r = requests.patch(patch_url, json=patch_p04, headers=headers, verify=False, timeout=30)
record_test("PATCH-P04", "PATCH Positive", "PATCH", patch_url, patch_p04, r, ts, "Update schedule to 4 working days (2160 min)")

# PATCH-P05: Update one working day's duration
ts = time.time()
patch_p05 = get_p01_baseline(target_shortcode)
patch_p05["totalWorkDurationInMinutes"] = 2640
patch_p05["fixedTimeSlots"][4]["workDurationInMinutes"] = 480
patch_p05["fixedTimeSlots"][4]["endTime"] = "16:00:00"
r = requests.patch(patch_url, json=patch_p05, headers=headers, verify=False, timeout=30)
record_test("PATCH-P05", "PATCH Positive", "PATCH", patch_url, patch_p05, r, ts, "Update Thursday duration to 480 min (total 2640 min)")

# PATCH-P06: Update timezone
ts = time.time()
patch_p06 = get_p01_baseline(target_shortcode)
patch_p06["timeZoneId"] = "Asia/Dubai"
r = requests.patch(patch_url, json=patch_p06, headers=headers, verify=False, timeout=30)
record_test("PATCH-P06", "PATCH Positive", "PATCH", patch_url, patch_p06, r, ts, "Update timezone to Asia/Dubai")

# PATCH-P07: Update recurrence
ts = time.time()
patch_p07 = get_p01_baseline(target_shortcode)
patch_p07["fixedTimeSlots"][0]["recurrenceOfMonth"] = [1, 2, 3]
r = requests.patch(patch_url, json=patch_p07, headers=headers, verify=False, timeout=30)
record_test("PATCH-P07", "PATCH Positive", "PATCH", patch_url, patch_p07, r, ts, "Update Sunday recurrence to [1, 2, 3]")

# PATCH-P08: Update all fields
ts = time.time()
patch_p08 = get_p01_baseline(target_shortcode)
patch_p08["templateName"] = {
    "en": f"Fully Refreshed Fixed Shift {target_shortcode}",
    "ar": f"وردية ثابتة محدثة بالكامل {target_shortcode}"
}
patch_p08["timeZoneId"] = "Asia/Riyadh"
patch_p08["totalWorkDurationInMinutes"] = 2700
r = requests.patch(patch_url, json=patch_p08, headers=headers, verify=False, timeout=30)
record_test("PATCH-P08", "PATCH Positive", "PATCH", patch_url, patch_p08, r, ts, "Update all fields simultaneously")


# -------------------------------------------------------------------
# 4. PATCH NEGATIVE SCENARIOS (Testing Field Validation & Security)
# -------------------------------------------------------------------
print("\n--- 4. PATCH NEGATIVE SCENARIOS ---", flush=True)

# PATCH-N01: Null template name
ts = time.time()
patch_n01 = get_p01_baseline(target_shortcode)
patch_n01["templateName"] = None
r = requests.patch(patch_url, json=patch_n01, headers=headers, verify=False, timeout=30)
record_test("PATCH-N01", "PATCH Negative", "PATCH", patch_url, patch_n01, r, ts, "Null template name in PATCH")

# PATCH-N02: Attempting to modify short code (should be blocked with Cit.Attendance:1107)
ts = time.time()
patch_n02 = get_p01_baseline("FXCHNG1") # Different short code
r = requests.patch(patch_url, json=patch_n02, headers=headers, verify=False, timeout=30)
record_test("PATCH-N02", "PATCH Negative", "PATCH", patch_url, patch_n02, r, ts, "Attempt to alter shortCode in PATCH (Cit.Attendance:1107)")

# PATCH-N03: Invalid day enum
ts = time.time()
patch_n03 = get_p01_baseline(target_shortcode)
patch_n03["fixedTimeSlots"][0]["dayEnum"] = 8
r = requests.patch(patch_url, json=patch_n03, headers=headers, verify=False, timeout=30)
record_test("PATCH-N03", "PATCH Negative", "PATCH", patch_url, patch_n03, r, ts, "Invalid dayEnum (8)")

# PATCH-N04: Negative duration
ts = time.time()
patch_n04 = get_p01_baseline(target_shortcode)
patch_n04["fixedTimeSlots"][0]["workDurationInMinutes"] = -540
r = requests.patch(patch_url, json=patch_n04, headers=headers, verify=False, timeout=30)
record_test("PATCH-N04", "PATCH Negative", "PATCH", patch_url, patch_n04, r, ts, "Negative work duration (-540)")

# PATCH-N05: Decimal duration
ts = time.time()
patch_n05 = get_p01_baseline(target_shortcode)
patch_n05["fixedTimeSlots"][0]["workDurationInMinutes"] = 540.5
r = requests.patch(patch_url, json=patch_n05, headers=headers, verify=False, timeout=30)
record_test("PATCH-N05", "PATCH Negative", "PATCH", patch_url, patch_n05, r, ts, "Decimal work duration (540.5)")

# PATCH-N06: Invalid recurrence
ts = time.time()
patch_n06 = get_p01_baseline(target_shortcode)
patch_n06["fixedTimeSlots"][0]["recurrenceOfMonth"] = [6]
r = requests.patch(patch_url, json=patch_n06, headers=headers, verify=False, timeout=30)
record_test("PATCH-N06", "PATCH Negative", "PATCH", patch_url, patch_n06, r, ts, "Invalid recurrence ([6])")

# PATCH-N07: Incorrect total duration
ts = time.time()
patch_n07 = get_p01_baseline(target_shortcode)
patch_n07["totalWorkDurationInMinutes"] = 3000
r = requests.patch(patch_url, json=patch_n07, headers=headers, verify=False, timeout=30)
record_test("PATCH-N07", "PATCH Negative", "PATCH", patch_url, patch_n07, r, ts, "Incorrect total duration (declared 3000, sum 2700)")

# PATCH-N08: Invalid timezone
ts = time.time()
patch_n08 = get_p01_baseline(target_shortcode)
patch_n08["timeZoneId"] = "Invalid/Timezone"
r = requests.patch(patch_url, json=patch_n08, headers=headers, verify=False, timeout=30)
record_test("PATCH-N08", "PATCH Negative", "PATCH", patch_url, patch_n08, r, ts, "Invalid timezone (Invalid/Timezone)")

# PATCH-N09: Non-existing template ID
ts = time.time()
non_exist_url = f"{patch_base_endpoint}/00000000-0000-0000-0000-000000000001?locationId={loc_id}"
r = requests.patch(non_exist_url, json=get_p01_baseline(target_shortcode), headers=headers, verify=False, timeout=30)
record_test("PATCH-N09", "PATCH Negative", "PATCH", non_exist_url, get_p01_baseline(target_shortcode), r, ts, "Non-existing template ID GUID")

# PATCH-N10: Invalid template ID format
ts = time.time()
invalid_id_url = f"{patch_base_endpoint}/invalid-id?locationId={loc_id}"
r = requests.patch(invalid_id_url, json=get_p01_baseline(target_shortcode), headers=headers, verify=False, timeout=30)
record_test("PATCH-N10", "PATCH Negative", "PATCH", invalid_id_url, get_p01_baseline(target_shortcode), r, ts, "Invalid template ID format ('invalid-id')")

# PATCH-N11: Company mismatch
ts = time.time()
other_company_id = "3a24741e-2667-1223-f12e-62a69fab3838"
mismatch_url = f"{base_url}/api/companies/{other_company_id}/worktemplates/fixed/{target_patch_id}?locationId={loc_id}"
r = requests.patch(mismatch_url, json=get_p01_baseline(target_shortcode), headers=headers, verify=False, timeout=30)
record_test("PATCH-N11", "PATCH Negative", "PATCH", mismatch_url, get_p01_baseline(target_shortcode), r, ts, "Company mismatch in URL")

# PATCH-N12: Flexible template ID passed to Fixed endpoint
ts = time.time()
flexi_id = "ef058f08-144c-4ea4-81ca-56657a29bde8"
cross_type_url = f"{patch_base_endpoint}/{flexi_id}?locationId={loc_id}"
r = requests.patch(cross_type_url, json=get_p01_baseline(target_shortcode), headers=headers, verify=False, timeout=30)
record_test("PATCH-N12", "PATCH Negative", "PATCH", cross_type_url, get_p01_baseline(target_shortcode), r, ts, "Cross-template-type (Flexible ID to Fixed PATCH)")


# -------------------------------------------------------------------
# SAVE COMPLETE RESULTS V2
# -------------------------------------------------------------------
with open('scratch/fixed_wt_location_validation_results_v2.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\n=====================================================================", flush=True)
print(f"REFINED TEST SUITE V2 COMPLETE! Executed {len(results)} scenarios.", flush=True)
total_pass = sum(1 for x in results if x['passed'])
total_fail = len(results) - total_pass
print(f"Overall Passed: {total_pass} | Failed/Issues Flagged: {total_fail}", flush=True)
print("Results saved to scratch/fixed_wt_location_validation_results_v2.json", flush=True)
print("=====================================================================", flush=True)
