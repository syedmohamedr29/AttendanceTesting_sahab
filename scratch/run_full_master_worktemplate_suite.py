import os
import sys
import json
import time
import requests
import urllib3
from pymongo import MongoClient
import bson

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/current_token.json', 'r', encoding='utf-8') as f:
    token_data = json.load(f)
token = token_data.get('access_token')

company_id = "3a249871-7a8d-dec5-2d72-47795dd2662d"
loc2_id = "3a24d646-b3cf-b1d4-61bb-1adf094b52fc" # Location 2 (fresh quota)
loc1_id = "3a24d629-0d56-a428-baa1-98493a77e614"

base_url = "https://attendance2.dev.zoolwork.com"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

results = []

def record(test_id, suite, category, method, url, payload, resp, start_time, notes=""):
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
            created_id = data.get('id') or (data.get('template', {}).get('id') if isinstance(data.get('template'), dict) else None)
            if 'error' in data:
                err = data['error']
                error_code = err.get('code')
                error_message = err.get('message')
                validation_errors = err.get('validationErrors')
    except Exception:
        pass
    
    # Expected Pass/Fail determination
    if category.startswith("Positive"):
        passed = (status_code in [200, 201])
    else: # Negative & Invariants
        passed = (status_code >= 400)

    res = {
        "test_id": test_id,
        "suite": suite,
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
    detail = f" | {error_code}" if error_code else ""
    if error_message:
        detail += f": {error_message}"
    print(f"[{test_id}] {suite} - {category} -> HTTP {status_code} ({mark}) [{elapsed_ms}ms]{detail}", flush=True)
    return res

print("=========================================================================", flush=True)
print("STARTING FULL MASTER WORK TEMPLATE TEST SUITE: FLEXIBLE & SPLIT (LOC 2)", flush=True)
print("=========================================================================", flush=True)

# -----------------------------------------------------------------------
# SUITE 1: FLEXIBLE WORK TEMPLATE (POST & PATCH) - LOCATION 2
# -----------------------------------------------------------------------
print("\n--- SUITE 1: FLEXIBLE WORK TEMPLATE TESTING ---", flush=True)

flexi_post_url = f"{base_url}/api/companies/{company_id}/worktemplates/flexi?locationId={loc2_id}"

def get_base_flexi(code="FXD0001", flex_type=1, duration=2400):
    return {
        "templateName": {"en": f"Flexible Location Shift {code}", "ar": f"وردية مرنة {code}"},
        "shortCode": code,
        "templateType": 2,
        "flexibleType": flex_type,
        "totalWorkDurationInMinutes": duration,
        "totalWorkingDays": 5,
        "totalDaysOff": 2,
        "timeZoneId": "Asia/Riyadh",
        "flexiTimeSlots": [
            {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
            {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
            {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
            {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
            {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
            {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [], "workDurationInMinutes": 0},
            {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [], "workDurationInMinutes": 0}
        ]
    }

# 1.1 POST Positive Scenarios
ts = time.time()
p1 = get_base_flexi("FXD0001", flex_type=1, duration=2400)
r = requests.post(flexi_post_url, json=p1, headers=headers, verify=False, timeout=30)
res_flex_p1 = record("FLX-POS-01", "Flexible", "Positive POST", "POST", flexi_post_url, p1, r, ts, "Flexible Daily standard 5-day (480m/day, 2400m total)")
flex_id_p1 = res_flex_p1.get("created_id")

ts = time.time()
p2 = get_base_flexi("FXW0001", flex_type=2, duration=2400) # FlexibleType 2 = Weekly
r = requests.post(flexi_post_url, json=p2, headers=headers, verify=False, timeout=30)
record("FLX-POS-02", "Flexible", "Positive POST", "POST", flexi_post_url, p2, r, ts, "Flexible Weekly required duration (2400m)")

ts = time.time()
p3 = get_base_flexi("FXD0002", flex_type=1, duration=2880)
p3["totalWorkingDays"] = 6
p3["totalDaysOff"] = 1
p3["flexiTimeSlots"][5] = {"dayEnum": 6, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480}
r = requests.post(flexi_post_url, json=p3, headers=headers, verify=False, timeout=30)
record("FLX-POS-03", "Flexible", "Positive POST", "POST", flexi_post_url, p3, r, ts, "Flexible 6-day schedule (2880m total)")

ts = time.time()
p4 = get_base_flexi("FXD0003", flex_type=1, duration=1920)
p4["totalWorkingDays"] = 4
p4["totalDaysOff"] = 3
p4["flexiTimeSlots"][0] = {"dayEnum": 1, "isWorkingDay": False, "recurrenceOfMonth": [], "workDurationInMinutes": 0}
r = requests.post(flexi_post_url, json=p4, headers=headers, verify=False, timeout=30)
record("FLX-POS-04", "Flexible", "Positive POST", "POST", flexi_post_url, p4, r, ts, "Flexible 4-day schedule (1920m total)")

ts = time.time()
p5 = get_base_flexi("FXD0004", flex_type=1, duration=2400)
p5["timeZoneId"] = "Asia/Kolkata"
r = requests.post(flexi_post_url, json=p5, headers=headers, verify=False, timeout=30)
record("FLX-POS-05", "Flexible", "Positive POST", "POST", flexi_post_url, p5, r, ts, "Flexible India Timezone (Asia/Kolkata)")

# 1.2 POST Negative Scenarios
ts = time.time()
n1 = get_base_flexi("FXDNEG1", flex_type=1, duration=2400)
n1["templateName"] = {"en": "", "ar": ""}
r = requests.post(flexi_post_url, json=n1, headers=headers, verify=False, timeout=30)
record("FLX-NEG-01", "Flexible", "Negative POST", "POST", flexi_post_url, n1, r, ts, "Empty template name")

ts = time.time()
n2 = get_base_flexi("FLX01", flex_type=1, duration=2400) # Length 5 < 7
r = requests.post(flexi_post_url, json=n2, headers=headers, verify=False, timeout=30)
record("FLX-NEG-02", "Flexible", "Negative POST", "POST", flexi_post_url, n2, r, ts, "ShortCode length < 7 ('FLX01')")

ts = time.time()
n3 = get_base_flexi("FXD0001", flex_type=1, duration=2400) # Duplicate
r = requests.post(flexi_post_url, json=n3, headers=headers, verify=False, timeout=30)
record("FLX-NEG-03", "Flexible", "Negative POST", "POST", flexi_post_url, n3, r, ts, "Duplicate shortCode (FXD0001)")

ts = time.time()
n4 = get_base_flexi("FXDNEG4", flex_type=999, duration=2400)
r = requests.post(flexi_post_url, json=n4, headers=headers, verify=False, timeout=30)
record("FLX-NEG-04", "Flexible", "Negative POST", "POST", flexi_post_url, n4, r, ts, "Invalid FlexibleType (999)")

ts = time.time()
n5 = get_base_flexi("FXDNEG5", flex_type=1, duration=2400)
n5["flexiTimeSlots"][0]["workDurationInMinutes"] = -480
r = requests.post(flexi_post_url, json=n5, headers=headers, verify=False, timeout=30)
record("FLX-NEG-05", "Flexible", "Negative POST", "POST", flexi_post_url, n5, r, ts, "Negative daily duration (-480m)")

ts = time.time()
n6 = get_base_flexi("FXDNEG6", flex_type=1, duration=2400)
n6["flexiTimeSlots"][0]["workDurationInMinutes"] = 0 # Working day with 0 duration
r = requests.post(flexi_post_url, json=n6, headers=headers, verify=False, timeout=30)
record("FLX-NEG-06", "Flexible", "Negative POST", "POST", flexi_post_url, n6, r, ts, "Working day with 0 minutes on Daily Flexi")

ts = time.time()
n7 = get_base_flexi("FXDNEG7", flex_type=1, duration=2400)
n7["flexiTimeSlots"][6]["workDurationInMinutes"] = 480 # Off-day with active duration
r = requests.post(flexi_post_url, json=n7, headers=headers, verify=False, timeout=30)
record("FLX-NEG-07", "Flexible", "Negative POST", "POST", flexi_post_url, n7, r, ts, "Off-day with active duration (480m)")

ts = time.time()
n8 = get_base_flexi("FXDNEG8", flex_type=1, duration=2400)
n8["flexiTimeSlots"][0]["dayEnum"] = 8
r = requests.post(flexi_post_url, json=n8, headers=headers, verify=False, timeout=30)
record("FLX-NEG-08", "Flexible", "Negative POST", "POST", flexi_post_url, n8, r, ts, "Invalid dayEnum (8)")

ts = time.time()
n9 = get_base_flexi("FXDNEG9", flex_type=1, duration=2400)
n9["flexiTimeSlots"][0]["recurrenceOfMonth"] = [6]
r = requests.post(flexi_post_url, json=n9, headers=headers, verify=False, timeout=30)
record("FLX-NEG-09", "Flexible", "Negative POST", "POST", flexi_post_url, n9, r, ts, "Invalid recurrence index ([6])")

ts = time.time()
n10 = get_base_flexi("FXDNE10", flex_type=1, duration=3000) # Declared 3000, sum 2400
r = requests.post(flexi_post_url, json=n10, headers=headers, verify=False, timeout=30)
record("FLX-NEG-10", "Flexible", "Negative POST", "POST", flexi_post_url, n10, r, ts, "Duration sum mismatch (3000 vs 2400)")

# 1.3 PATCH Scenarios for Flexible Template
target_flex_id = flex_id_p1
flex_patch_url = f"{base_url}/api/companies/{company_id}/worktemplates/flexi/{target_flex_id}?locationId={loc2_id}"

ts = time.time()
pat1 = get_base_flexi("FXD0001", flex_type=1, duration=2400)
pat1["templateName"] = {"en": "Flexible Location Shift Updated", "ar": "وردية مرنة محدثة"}
r = requests.patch(flex_patch_url, json=pat1, headers=headers, verify=False, timeout=30)
record("FLX-PAT-01", "Flexible", "Positive PATCH", "PATCH", flex_patch_url, pat1, r, ts, "Update Flexible template name")

ts = time.time()
pat2 = get_base_flexi("FXD0001", flex_type=1, duration=2700)
for s in pat2["flexiTimeSlots"][:5]:
    s["workDurationInMinutes"] = 540
r = requests.patch(flex_patch_url, json=pat2, headers=headers, verify=False, timeout=30)
record("FLX-PAT-02", "Flexible", "Positive PATCH", "PATCH", flex_patch_url, pat2, r, ts, "Update daily duration to 540m (2700m total)")

ts = time.time()
pat3 = get_base_flexi("FXD0001", flex_type=1, duration=2700)
pat3["timeZoneId"] = "Asia/Dubai"
r = requests.patch(flex_patch_url, json=pat3, headers=headers, verify=False, timeout=30)
record("FLX-PAT-03", "Flexible", "Positive PATCH", "PATCH", flex_patch_url, pat3, r, ts, "Update timezone to Asia/Dubai")

ts = time.time()
pat4 = get_base_flexi("FXDCHG1", flex_type=1, duration=2700) # Altered code
r = requests.patch(flex_patch_url, json=pat4, headers=headers, verify=False, timeout=30)
record("FLX-PAT-04", "Flexible", "Negative PATCH", "PATCH", flex_patch_url, pat4, r, ts, "Attempt to alter shortCode in PATCH (Cit.Attendance:1107)")

ts = time.time()
pat5 = get_base_flexi("FXD0001", flex_type=1, duration=2700)
pat5["flexiTimeSlots"][0]["recurrenceOfMonth"] = [6] # Recurrence 6 in PATCH
r = requests.patch(flex_patch_url, json=pat5, headers=headers, verify=False, timeout=30)
record("FLX-PAT-05", "Flexible", "Negative PATCH", "PATCH", flex_patch_url, pat5, r, ts, "Recurrence [6] in Flexible PATCH")

ts = time.time()
pat6 = get_base_flexi("FXD0001", flex_type=1, duration=3500) # Duration mismatch in PATCH
r = requests.patch(flex_patch_url, json=pat6, headers=headers, verify=False, timeout=30)
record("FLX-PAT-06", "Flexible", "Negative PATCH", "PATCH", flex_patch_url, pat6, r, ts, "Duration mismatch in Flexible PATCH (3500 vs 2700)")

ts = time.time()
pat7 = get_base_flexi("FXD0001", flex_type=1, duration=2700)
pat7["timeZoneId"] = "Invalid/Timezone" # Invalid timezone in PATCH
r = requests.patch(flex_patch_url, json=pat7, headers=headers, verify=False, timeout=30)
record("FLX-PAT-07", "Flexible", "Negative PATCH", "PATCH", flex_patch_url, pat7, r, ts, "Invalid timezone in Flexible PATCH")


# -----------------------------------------------------------------------
# SUITE 2: SPLIT WORK TEMPLATE (POST & PATCH) - LOCATION 2
# -----------------------------------------------------------------------
print("\n--- SUITE 2: SPLIT WORK TEMPLATE TESTING ---", flush=True)

split_post_url = f"{base_url}/api/companies/{company_id}/worktemplates/split?locationId={loc2_id}"

def get_base_split(code="SPD0001", duration=2400):
    return {
        "templateName": {"en": f"Split Location Shift {code}", "ar": f"وردية مجزأة {code}"},
        "shortCode": code,
        "templateType": 3,
        "totalWorkDurationInMinutes": duration,
        "totalWorkingDays": 5,
        "totalDaysOff": 2,
        "timeZoneId": "Asia/Riyadh",
        "splitTimeSlots": [
            {
                "dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480,
                "timeSlots": [
                    {"startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240},
                    {"startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240}
                ]
            },
            {
                "dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480,
                "timeSlots": [
                    {"startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240},
                    {"startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240}
                ]
            },
            {
                "dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480,
                "timeSlots": [
                    {"startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240},
                    {"startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240}
                ]
            },
            {
                "dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480,
                "timeSlots": [
                    {"startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240},
                    {"startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240}
                ]
            },
            {
                "dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480,
                "timeSlots": [
                    {"startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240},
                    {"startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240}
                ]
            },
            {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [], "workDurationInMinutes": 0, "timeSlots": []},
            {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [], "workDurationInMinutes": 0, "timeSlots": []}
        ]
    }

# 2.1 POST Positive Scenarios
ts = time.time()
sp1 = get_base_split("SPD0001", duration=2400)
r = requests.post(split_post_url, json=sp1, headers=headers, verify=False, timeout=30)
res_split_p1 = record("SPL-POS-01", "Split", "Positive POST", "POST", split_post_url, sp1, r, ts, "Split standard 2-interval shift (240+240=480m/day, total 2400m)")
split_id_p1 = res_split_p1.get("created_id")

ts = time.time()
sp2 = get_base_split("SPD0002", duration=2400) # 3-interval split shift
for d in sp2["splitTimeSlots"][:5]:
    d["timeSlots"] = [
        {"startTime": "08:00:00", "endTime": "11:00:00", "workDurationInMinutes": 180},
        {"startTime": "12:00:00", "endTime": "15:00:00", "workDurationInMinutes": 180},
        {"startTime": "16:00:00", "endTime": "18:00:00", "workDurationInMinutes": 120}
    ]
r = requests.post(split_post_url, json=sp2, headers=headers, verify=False, timeout=30)
record("SPL-POS-02", "Split", "Positive POST", "POST", split_post_url, sp2, r, ts, "Split 3-interval shift (180+180+120=480m/day)")

ts = time.time()
sp3 = get_base_split("SPD0003", duration=2880)
sp3["totalWorkingDays"] = 6
sp3["totalDaysOff"] = 1
sp3["splitTimeSlots"][5] = {
    "dayEnum": 6, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480,
    "timeSlots": [
        {"startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240},
        {"startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240}
    ]
}
r = requests.post(split_post_url, json=sp3, headers=headers, verify=False, timeout=30)
record("SPL-POS-03", "Split", "Positive POST", "POST", split_post_url, sp3, r, ts, "Split 6-day working schedule (2880m total)")

ts = time.time()
sp4 = get_base_split("SPD0004", duration=1920)
sp4["totalWorkingDays"] = 4
sp4["totalDaysOff"] = 3
sp4["splitTimeSlots"][0] = {"dayEnum": 1, "isWorkingDay": False, "recurrenceOfMonth": [], "workDurationInMinutes": 0, "timeSlots": []}
r = requests.post(split_post_url, json=sp4, headers=headers, verify=False, timeout=30)
record("SPL-POS-04", "Split", "Positive POST", "POST", split_post_url, sp4, r, ts, "Split 4-day working schedule (1920m total)")

ts = time.time()
sp5 = get_base_split("SPD0005", duration=2400)
sp5["timeZoneId"] = "Asia/Kolkata"
r = requests.post(split_post_url, json=sp5, headers=headers, verify=False, timeout=30)
record("SPL-POS-05", "Split", "Positive POST", "POST", split_post_url, sp5, r, ts, "Split India Timezone (Asia/Kolkata)")

# 2.2 POST Negative Scenarios
ts = time.time()
sn1 = get_base_split("SPDNEG1", duration=2400)
sn1["templateName"] = {"en": "", "ar": ""}
r = requests.post(split_post_url, json=sn1, headers=headers, verify=False, timeout=30)
record("SPL-NEG-01", "Split", "Negative POST", "POST", split_post_url, sn1, r, ts, "Empty template name")

ts = time.time()
sn2 = get_base_split("SPL01", duration=2400) # Length 5 < 7
r = requests.post(split_post_url, json=sn2, headers=headers, verify=False, timeout=30)
record("SPL-NEG-02", "Split", "Negative POST", "POST", split_post_url, sn2, r, ts, "ShortCode length < 7 ('SPL01')")

ts = time.time()
sn3 = get_base_split("SPD0001", duration=2400) # Duplicate shortCode
r = requests.post(split_post_url, json=sn3, headers=headers, verify=False, timeout=30)
record("SPL-NEG-03", "Split", "Negative POST", "POST", split_post_url, sn3, r, ts, "Duplicate shortCode (SPD0001)")

ts = time.time()
sn4 = get_base_split("SPDNEG4", duration=2400) # Overlapping intervals
sn4["splitTimeSlots"][0]["timeSlots"] = [
    {"startTime": "08:00:00", "endTime": "13:00:00", "workDurationInMinutes": 300},
    {"startTime": "12:00:00", "endTime": "16:00:00", "workDurationInMinutes": 240} # Overlaps 12:00-13:00
]
sn4["splitTimeSlots"][0]["workDurationInMinutes"] = 540
sn4["totalWorkDurationInMinutes"] = 2460
r = requests.post(split_post_url, json=sn4, headers=headers, verify=False, timeout=30)
record("SPL-NEG-04", "Split", "Negative POST", "POST", split_post_url, sn4, r, ts, "Overlapping split intervals (1 hr overlap)")

ts = time.time()
sn5 = get_base_split("SPDNEG5", duration=2400) # Zero break gap
sn5["splitTimeSlots"][0]["timeSlots"] = [
    {"startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240},
    {"startTime": "12:00:00", "endTime": "16:00:00", "workDurationInMinutes": 240} # Zero gap
]
r = requests.post(split_post_url, json=sn5, headers=headers, verify=False, timeout=30)
record("SPL-NEG-05", "Split", "Negative POST", "POST", split_post_url, sn5, r, ts, "Zero break gap between intervals (12:00 to 12:00)")

ts = time.time()
sn6 = get_base_split("SPDNEG6", duration=2400) # Inverted interval (end < start)
sn6["splitTimeSlots"][0]["timeSlots"] = [
    {"startTime": "12:00:00", "endTime": "08:00:00", "workDurationInMinutes": 240},
    {"startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240}
]
r = requests.post(split_post_url, json=sn6, headers=headers, verify=False, timeout=30)
record("SPL-NEG-06", "Split", "Negative POST", "POST", split_post_url, sn6, r, ts, "Inverted split interval (startTime 12:00 > endTime 08:00)")

ts = time.time()
sn7 = get_base_split("SPDNEG7", duration=2400) # Empty timeSlots on working day
sn7["splitTimeSlots"][0]["timeSlots"] = []
r = requests.post(split_post_url, json=sn7, headers=headers, verify=False, timeout=30)
record("SPL-NEG-07", "Split", "Negative POST", "POST", split_post_url, sn7, r, ts, "Empty timeSlots array on working day")

ts = time.time()
sn8 = get_base_split("SPDNEG8", duration=2400) # Interval duration mismatch
sn8["splitTimeSlots"][0]["timeSlots"][0]["workDurationInMinutes"] = 180 # Slot says 180, but 08:00-12:00 is 240
r = requests.post(split_post_url, json=sn8, headers=headers, verify=False, timeout=30)
record("SPL-NEG-08", "Split", "Negative POST", "POST", split_post_url, sn8, r, ts, "Interval duration does not equal (endTime - startTime)")

ts = time.time()
sn9 = get_base_split("SPDNEG9", duration=2400) # Daily workDurationInMinutes does not equal sum of intervals
sn9["splitTimeSlots"][0]["workDurationInMinutes"] = 600 # 240 + 240 = 480 != 600
sn9["totalWorkDurationInMinutes"] = 2520
r = requests.post(split_post_url, json=sn9, headers=headers, verify=False, timeout=30)
record("SPL-NEG-09", "Split", "Negative POST", "POST", split_post_url, sn9, r, ts, "Daily duration does not equal interval sum (600 vs 480)")

ts = time.time()
sn10 = get_base_split("SPDNE10", duration=3000) # Total duration mismatch (3000 vs 2400)
r = requests.post(split_post_url, json=sn10, headers=headers, verify=False, timeout=30)
record("SPL-NEG-10", "Split", "Negative POST", "POST", split_post_url, sn10, r, ts, "Total duration mismatch in Split (3000 vs 2400)")

# 2.3 PATCH Scenarios for Split Template
target_split_id = split_id_p1
split_patch_url = f"{base_url}/api/companies/{company_id}/worktemplates/split/{target_split_id}?locationId={loc2_id}"

ts = time.time()
spat1 = get_base_split("SPD0001", duration=2400)
spat1["templateName"] = {"en": "Split Location Shift Updated", "ar": "وردية مجزأة محدثة"}
r = requests.patch(split_patch_url, json=spat1, headers=headers, verify=False, timeout=30)
record("SPL-PAT-01", "Split", "Positive PATCH", "PATCH", split_patch_url, spat1, r, ts, "Update Split template name")

ts = time.time()
spat2 = get_base_split("SPD0001", duration=2400)
for d in spat2["splitTimeSlots"][:5]:
    d["timeSlots"] = [
        {"startTime": "09:00:00", "endTime": "13:00:00", "workDurationInMinutes": 240},
        {"startTime": "15:00:00", "endTime": "19:00:00", "workDurationInMinutes": 240}
    ]
r = requests.patch(split_patch_url, json=spat2, headers=headers, verify=False, timeout=30)
record("SPL-PAT-02", "Split", "Positive PATCH", "PATCH", split_patch_url, spat2, r, ts, "Update Split interval timings (09-13 & 15-19)")

ts = time.time()
spat3 = get_base_split("SPD0001", duration=2400)
spat3["timeZoneId"] = "Asia/Dubai"
r = requests.patch(split_patch_url, json=spat3, headers=headers, verify=False, timeout=30)
record("SPL-PAT-03", "Split", "Positive PATCH", "PATCH", split_patch_url, spat3, r, ts, "Update timezone to Asia/Dubai")

ts = time.time()
spat4 = get_base_split("SPDCHG1", duration=2400) # Altered code
r = requests.patch(split_patch_url, json=spat4, headers=headers, verify=False, timeout=30)
record("SPL-PAT-04", "Split", "Negative PATCH", "PATCH", split_patch_url, spat4, r, ts, "Attempt to alter shortCode in Split PATCH (Cit.Attendance:1107)")

ts = time.time()
spat5 = get_base_split("SPD0001", duration=2400)
spat5["splitTimeSlots"][0]["timeSlots"] = [
    {"startTime": "08:00:00", "endTime": "13:00:00", "workDurationInMinutes": 300},
    {"startTime": "12:00:00", "endTime": "16:00:00", "workDurationInMinutes": 240}
]
r = requests.patch(split_patch_url, json=spat5, headers=headers, verify=False, timeout=30)
record("SPL-PAT-05", "Split", "Negative PATCH", "PATCH", split_patch_url, spat5, r, ts, "Overlapping intervals in Split PATCH")

ts = time.time()
spat6 = get_base_split("SPD0001", duration=2400)
spat6["splitTimeSlots"][0]["recurrenceOfMonth"] = [6] # Recurrence 6 in Split PATCH
r = requests.patch(split_patch_url, json=spat6, headers=headers, verify=False, timeout=30)
record("SPL-PAT-06", "Split", "Negative PATCH", "PATCH", split_patch_url, spat6, r, ts, "Recurrence [6] in Split PATCH")

ts = time.time()
spat7 = get_base_split("SPD0001", duration=3200) # Duration mismatch in Split PATCH
r = requests.patch(split_patch_url, json=spat7, headers=headers, verify=False, timeout=30)
record("SPL-PAT-07", "Split", "Negative PATCH", "PATCH", split_patch_url, spat7, r, ts, "Duration mismatch in Split PATCH (3200 vs 2400)")


# -----------------------------------------------------------------------
# SUITE 3: CROSS-TYPE TRANSITION MATRIX (LOCATION-SCOPED)
# -----------------------------------------------------------------------
print("\n--- SUITE 3: CROSS-TYPE TRANSITION MATRIX TESTING ---", flush=True)

# We will test:
# 1. Flexible -> Fixed (TRANS-03): Call PATCH /fixed/{flex_id_p1}?locationId={loc2_id} with Fixed payload
# 2. Flexible -> Split (TRANS-04): Call PATCH /split/{flex_id_p1}?locationId={loc2_id} with Split payload
# 3. Split -> Fixed (TRANS-05): Call PATCH /fixed/{split_id_p1}?locationId={loc2_id} with Fixed payload
# 4. Split -> Flexible (TRANS-06): Call PATCH /flexi/{split_id_p1}?locationId={loc2_id} with Flexible payload

# Fixed payload for transitions
fixed_payload_trans = {
    "templateName": {"en": "Transited to Fixed Shift", "ar": "محولة إلى وردية ثابتة"},
    "shortCode": "FXD0001", # Match existing
    "templateType": 1,
    "totalWorkDurationInMinutes": 2700,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "timeZoneId": "Asia/Riyadh",
    "fixedTimeSlots": [
        {"workDurationInMinutes": 540, "dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:00:00", "endTime": "17:00:00"},
        {"workDurationInMinutes": 540, "dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:00:00", "endTime": "17:00:00"},
        {"workDurationInMinutes": 540, "dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:00:00", "endTime": "17:00:00"},
        {"workDurationInMinutes": 540, "dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:00:00", "endTime": "17:00:00"},
        {"workDurationInMinutes": 540, "dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:00:00", "endTime": "17:00:00"},
        {"workDurationInMinutes": 0, "dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [], "startTime": "00:00:00", "endTime": "00:00:00"},
        {"workDurationInMinutes": 0, "dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [], "startTime": "00:00:00", "endTime": "00:00:00"}
    ]
}

# TRANS-03: Flexible -> Fixed
ts = time.time()
trans_url_3 = f"{base_url}/api/companies/{company_id}/worktemplates/fixed/{flex_id_p1}?locationId={loc2_id}"
r = requests.patch(trans_url_3, json=fixed_payload_trans, headers=headers, verify=False, timeout=30)
record("TRANS-03", "Cross-Type", "Positive PATCH", "PATCH", trans_url_3, fixed_payload_trans, r, ts, "Flexible -> Fixed migration via /fixed/{id}")

# TRANS-04: Flexible -> Split (using FXD0002)
# Let's get FXD0002 ID from results
fxd0002_id = [x['created_id'] for x in results if x['test_id'] == 'FLX-POS-03'][0]
trans_url_4 = f"{base_url}/api/companies/{company_id}/worktemplates/split/{fxd0002_id}?locationId={loc2_id}"
split_trans_payload = get_base_split("FXD0002", duration=2400)
ts = time.time()
r = requests.patch(trans_url_4, json=split_trans_payload, headers=headers, verify=False, timeout=30)
record("TRANS-04", "Cross-Type", "Positive PATCH", "PATCH", trans_url_4, split_trans_payload, r, ts, "Flexible -> Split migration via /split/{id}")

# TRANS-05: Split -> Fixed
trans_url_5 = f"{base_url}/api/companies/{company_id}/worktemplates/fixed/{split_id_p1}?locationId={loc2_id}"
fixed_trans_payload_sp = dict(fixed_payload_trans)
fixed_trans_payload_sp["shortCode"] = "SPD0001"
ts = time.time()
r = requests.patch(trans_url_5, json=fixed_trans_payload_sp, headers=headers, verify=False, timeout=30)
record("TRANS-05", "Cross-Type", "Positive PATCH", "PATCH", trans_url_5, fixed_trans_payload_sp, r, ts, "Split -> Fixed migration via /fixed/{id}")

# TRANS-06: Split -> Flexible (using SPD0002)
spd0002_id = [x['created_id'] for x in results if x['test_id'] == 'SPL-POS-02'][0]
trans_url_6 = f"{base_url}/api/companies/{company_id}/worktemplates/flexi/{spd0002_id}?locationId={loc2_id}"
flex_trans_payload_sp = get_base_flexi("SPD0002", flex_type=1, duration=2400)
ts = time.time()
r = requests.patch(trans_url_6, json=flex_trans_payload_sp, headers=headers, verify=False, timeout=30)
record("TRANS-06", "Cross-Type", "Positive PATCH", "PATCH", trans_url_6, flex_trans_payload_sp, r, ts, "Split -> Flexible migration via /flexi/{id}")


# -----------------------------------------------------------------------
# SAVE RESULTS JSON
# -----------------------------------------------------------------------
with open('scratch/full_master_suite_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\n=========================================================================", flush=True)
print(f"FULL MASTER SUITE EXECUTION COMPLETE! Executed {len(results)} scenarios.", flush=True)
total_pass = sum(1 for x in results if x['passed'])
total_fail = len(results) - total_pass
print(f"Passed: {total_pass} | Failed/Issues Flagged: {total_fail}", flush=True)
print("Saved to scratch/full_master_suite_results.json", flush=True)
print("=========================================================================", flush=True)
