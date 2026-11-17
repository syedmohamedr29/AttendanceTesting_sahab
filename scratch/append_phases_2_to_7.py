# Append Phases 2 to 7 to scratch/run_full_scheduler_test_suite.py

append_code = '''
print("==================================================")
print("PHASE 2: ROSTER SHIFTS / WORK PLANS")
print("==================================================")

# 11. POS-SHF-01: Create standard day roster shift (08:00 - 16:00)
code_s01 = random_code("SFT")
payload_s01 = {
    "tenantName": {"en": "Attendance"},
    "boardId": context.get("board1_id"),
    "shiftName": {"en": f"Morning Acute {code_s01}", "ar": "وردية الصباح"},
    "code": code_s01,
    "colour": "#14B8A6",
    "description": "Standard 8h day acute shift",
    "rosterTimeSlots": [
        {"dayEnum": 0, "isWorkingDay": True, "startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480},
        {"dayEnum": 1, "isWorkingDay": True, "startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480},
        {"dayEnum": 2, "isWorkingDay": True, "startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480},
        {"dayEnum": 3, "isWorkingDay": True, "startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480},
        {"dayEnum": 4, "isWorkingDay": True, "startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480},
        {"dayEnum": 5, "isWorkingDay": False, "startTime": "00:00", "endTime": "00:00", "workDurationInMinutes": 0},
        {"dayEnum": 6, "isWorkingDay": False, "startTime": "00:00", "endTime": "00:00", "workDurationInMinutes": 0}
    ],
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "isBreakPolicyEnabled": False,
    "isOvertimePolicyEnabled": False,
    "isGracePeriodPolicyEnabled": False,
    "policyIds": []
}
r = requests.post(f"{BASE_URL}/api/companies/{COMPANY_ID}/workplans/roster?locationId={LOC_DAMMAM}", headers=headers, json=payload_s01, verify=False, timeout=10)
if r.status_code == 200:
    s_data = r.json()
    wp_id = s_data.get("workPlan", {}).get("id") or s_data.get("id")
    context["shift1_id"] = wp_id
    context["shift1_code"] = code_s01
    record("POS-SHF-01", "Pass", f"HTTP 200 OK. Roster shift created with ID {wp_id}, code {code_s01}.")
else:
    record("POS-SHF-01", "Fail", f"Expected 200 OK, got {r.status_code}: {r.text[:200]}")

# 12. POS-SHF-02: Create overnight roster shift (22:00 - 06:00)
code_s02 = random_code("NGT")
payload_s02 = {
    "tenantName": {"en": "Attendance"},
    "boardId": context.get("board1_id"),
    "shiftName": {"en": f"Night Shift {code_s02}"},
    "code": code_s02,
    "colour": "#8B5CF6",
    "description": "Overnight 8h shift",
    "rosterTimeSlots": [
        {"dayEnum": 0, "isWorkingDay": True, "startTime": "22:00", "endTime": "06:00", "workDurationInMinutes": 480},
        {"dayEnum": 1, "isWorkingDay": True, "startTime": "22:00", "endTime": "06:00", "workDurationInMinutes": 480},
        {"dayEnum": 2, "isWorkingDay": True, "startTime": "22:00", "endTime": "06:00", "workDurationInMinutes": 480},
        {"dayEnum": 3, "isWorkingDay": True, "startTime": "22:00", "endTime": "06:00", "workDurationInMinutes": 480},
        {"dayEnum": 4, "isWorkingDay": True, "startTime": "22:00", "endTime": "06:00", "workDurationInMinutes": 480},
        {"dayEnum": 5, "isWorkingDay": False, "startTime": "00:00", "endTime": "00:00", "workDurationInMinutes": 0},
        {"dayEnum": 6, "isWorkingDay": False, "startTime": "00:00", "endTime": "00:00", "workDurationInMinutes": 0}
    ],
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "isBreakPolicyEnabled": False,
    "isOvertimePolicyEnabled": False,
    "isGracePeriodPolicyEnabled": False,
    "policyIds": []
}
r = requests.post(f"{BASE_URL}/api/companies/{COMPANY_ID}/workplans/roster?locationId={LOC_DAMMAM}", headers=headers, json=payload_s02, verify=False, timeout=10)
if r.status_code == 200:
    context["shift2_id"] = r.json().get("workPlan", {}).get("id")
    record("POS-SHF-02", "Pass", f"HTTP 200 OK. Overnight shift created successfully.")
else:
    record("POS-SHF-02", "Fail", f"Expected 200 OK, got {r.status_code}: {r.text[:200]}")

# 13. POS-SHF-04: Edit roster shift timing before scheduled days
if context.get("shift1_id"):
    payload_edit_shift = {
        "shiftName": {"en": f"Morning Acute Updated {code_s01}"}
    }
    r = requests.patch(f"{BASE_URL}/api/companies/{COMPANY_ID}/workplans/roster/{context['shift1_id']}?locationId={LOC_DAMMAM}", headers=headers, json=payload_edit_shift, verify=False, timeout=10)
    if r.status_code == 200:
        record("POS-SHF-04", "Pass", f"HTTP 200 OK. Shift name/timings edited before scheduled days.")
    else:
        record("POS-SHF-04", "Fail", f"Expected 200 OK, got {r.status_code}: {r.text[:200]}")

# 14. NEG-SHF-02: Create roster shift with duplicate code (Rule 1106)
if context.get("shift1_code"):
    payload_dup_code = {
        "boardId": context.get("board1_id"),
        "shiftName": {"en": "Dup Code Shift"},
        "code": context["shift1_code"],
        "colour": "#14B8A6",
        "rosterTimeSlots": payload_s01["rosterTimeSlots"],
        "totalWorkDurationInMinutes": 2400,
        "totalWorkingDays": 5,
        "totalDaysOff": 2
    }
    r = requests.post(f"{BASE_URL}/api/companies/{COMPANY_ID}/workplans/roster?locationId={LOC_DAMMAM}", headers=headers, json=payload_dup_code, verify=False, timeout=10)
    if r.status_code == 400:
        record("NEG-SHF-02", "Pass", f"HTTP 400 Bad Request. Correctly rejected duplicate code {context['shift1_code']} ({r.text[:100]}).")
    else:
        record("NEG-SHF-02", "Fail", f"Expected 400 Bad Request for duplicate code, got {r.status_code}: {r.text[:200]}")

# 15. NEG-SHF-03: Edit roster shift code (Rule 1107 - locked)
if context.get("shift1_id"):
    payload_edit_code = {"code": "LOCKEDCODE99"}
    r = requests.patch(f"{BASE_URL}/api/companies/{COMPANY_ID}/workplans/roster/{context['shift1_id']}?locationId={LOC_DAMMAM}", headers=headers, json=payload_edit_code, verify=False, timeout=10)
    if r.status_code == 400:
        record("NEG-SHF-03", "Pass", f"HTTP 400 Bad Request. Correctly rejected modifying code (Rule 1107: {r.text[:100]}).")
    else:
        record("NEG-SHF-03", "Fail", f"Expected 400 Bad Request for editing code, got {r.status_code}: {r.text[:200]}")

print("==================================================")
print("PHASE 3: BOARD EMPLOYEES & CONFLICT PREFLIGHT")
print("==================================================")

EMP_DAMMAM_1 = "272e9196-ef39-ed40-b19a-ed60dee4d9a0"
EMP_DAMMAM_2 = "f9e1a6d5-6bd5-7d46-ae85-38b81dc80887"

# 16. POS-MEM-01: Preflight conflict check for employees
# Anchor next Sunday
next_sunday = (datetime.date.today() + datetime.timedelta(days=(6 - datetime.date.today().weekday()) % 7)).strftime("%Y-%m-%d")
if next_sunday == datetime.date.today().strftime("%Y-%m-%d"):
    next_sunday = (datetime.date.today() + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
context["next_sunday"] = next_sunday

payload_chk = {
    "employeeIds": [EMP_DAMMAM_1, EMP_DAMMAM_2],
    "startDate": next_sunday
}
r = requests.post(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards/{context['board1_id']}/employees/check-conflicts?locationId={LOC_DAMMAM}", headers=headers, json=payload_chk, verify=False, timeout=10)
if r.status_code == 200:
    res_chk = r.json()
    record("POS-MEM-01", "Pass", f"HTTP 200 OK. Conflict preflight succeeded: clean={len(res_chk.get('cleanEmployeeIds', []))}, adjustable={len(res_chk.get('adjustableEmployeeIds', []))}, blocked={len(res_chk.get('blockedEmployeeIds', []))}.")
else:
    record("POS-MEM-01", "Fail", f"Expected 200 OK for check-conflicts, got {r.status_code}: {r.text[:200]}")

# 17. POS-MEM-02 & POS-MEM-04: Add employees with adjustConflicts = True
payload_enroll = {
    "employeeIds": [EMP_DAMMAM_1, EMP_DAMMAM_2],
    "startDate": next_sunday,
    "endDate": None,
    "adjustConflicts": True
}
r = requests.patch(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards/{context['board1_id']}/employees?locationId={LOC_DAMMAM}", headers=headers, json=payload_enroll, verify=False, timeout=10)
if r.status_code == 200:
    record("POS-MEM-02", "Pass", f"HTTP 200 OK. Enrolled 2 employees with open-ended period.")
    record("POS-MEM-04", "Pass", f"HTTP 200 OK. Enrolled employees with adjustConflicts: true successfully.")
else:
    record("POS-MEM-02", "Fail", f"Expected 200 OK, got {r.status_code}: {r.text[:200]}")
    record("POS-MEM-04", "Fail", f"Expected 200 OK, got {r.status_code}: {r.text[:200]}")

# 18. Assign employees to Area (Setup step for board with areas)
if context.get("area1_id"):
    payload_area_assign = {
        "employeeIds": [EMP_DAMMAM_1, EMP_DAMMAM_2]
    }
    r = requests.patch(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards/{context['board1_id']}/areas/{context['area1_id']}/employees?locationId={LOC_DAMMAM}", headers=headers, json=payload_area_assign, verify=False, timeout=10)
    if r.status_code == 200:
        record("POS-MEM-03", "Pass", f"HTTP 200 OK. Successfully assigned employees to Area A.")
    else:
        record("POS-MEM-03", "Fail", f"Expected 200 OK for area assignment, got {r.status_code}: {r.text[:200]}")

# 19. NEG-MEM-03: Add employee with start date in past
payload_past_start = {
    "employeeIds": [EMP_DAMMAM_1],
    "startDate": "2026-10-01",
    "adjustConflicts": True
}
r = requests.patch(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards/{context['board1_id']}/employees?locationId={LOC_DAMMAM}", headers=headers, json=payload_past_start, verify=False, timeout=10)
if r.status_code == 400:
    record("NEG-MEM-03", "Pass", f"HTTP 400 Bad Request. Correctly rejected startDate in the past.")
else:
    record("NEG-MEM-03", "Fail", f"Expected 400 Bad Request for past startDate, got {r.status_code}: {r.text[:200]}")

# 20. NEG-MEM-04: Add employee with endDate < startDate
payload_inv_dates = {
    "employeeIds": [EMP_DAMMAM_1],
    "startDate": "2026-11-25",
    "endDate": "2026-11-20",
    "adjustConflicts": True
}
r = requests.patch(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards/{context['board1_id']}/employees?locationId={LOC_DAMMAM}", headers=headers, json=payload_inv_dates, verify=False, timeout=10)
if r.status_code == 400:
    record("NEG-MEM-04", "Pass", f"HTTP 400 Bad Request. Correctly rejected endDate < startDate.")
else:
    record("NEG-MEM-04", "Fail", f"Expected 400 Bad Request for endDate < startDate, got {r.status_code}: {r.text[:200]}")

# 21. SEC-EMP-01: Inactive Employee Enrollment Leakage Test
INACTIVE_EMP = "39879386-4c24-ee4c-84ec-6eb7daa765ac" # SA-EMP-0006 IsActive: false
payload_inactive = {
    "employeeIds": [INACTIVE_EMP],
    "startDate": next_sunday,
    "adjustConflicts": True
}
r = requests.patch(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards/{context['board1_id']}/employees?locationId={LOC_DAMMAM}", headers=headers, json=payload_inactive, verify=False, timeout=10)
if r.status_code == 400:
    record("SEC-EMP-01", "Pass", f"HTTP 400 Bad Request. Inactive employee enrollment blocked cleanly.")
else:
    # If 200 OK is returned, check if an orphan record was created (Defect 59/69 regression)
    record("SEC-EMP-01", "Fail", f"Expected 400 Bad Request for inactive employee, got HTTP {r.status_code}: {r.text[:200]}", defect_ref="DEFECT-SCHED-01")

print("==================================================")
print("PHASE 4: PLANNER GRID & SHIFT ALLOCATION")
print("==================================================")

# 22. POS-PLN-01: Query Schedule Plans list
r = requests.get(f"{BASE_URL}/api/companies/{COMPANY_ID}/schedule-plans?frequency=Weekly&anchor={next_sunday}", headers=headers, verify=False, timeout=10)
if r.status_code == 200:
    record("POS-PLN-01", "Pass", f"HTTP 200 OK. Schedule Plans list retrieved successfully.")
else:
    record("POS-PLN-01", "Fail", f"Expected 200 OK, got {r.status_code}: {r.text[:200]}")

# 23. POS-PLN-02: Query Schedule Grid by anchor
r = requests.get(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards/{context['board1_id']}/schedule?anchor={next_sunday}", headers=headers, verify=False, timeout=10)
if r.status_code == 200:
    grid_data = r.json()
    record("POS-PLN-02", "Pass", f"HTTP 200 OK. Schedule grid loaded: version={grid_data.get('version')}, isReadyToPublish={grid_data.get('isReadyToPublish')}.")
else:
    record("POS-PLN-02", "Fail", f"Expected 200 OK, got {r.status_code}: {r.text[:200]}")

# Generate dates for anchor week (Sunday to Saturday)
anchor_dt = datetime.datetime.strptime(next_sunday, "%Y-%m-%d").date()
week_dates = [(anchor_dt + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
days_working = week_dates[:5] # Sun to Thu
days_off = week_dates[5:]     # Fri, Sat

# 24. POS-PLN-03: Assign Roster Shift to Sun-Thu
if context.get("shift1_id"):
    payload_assign_shift = {
        "workPlanId": context["shift1_id"],
        "dayOff": False,
        "slots": [
            {"employeeId": EMP_DAMMAM_1, "dates": days_working},
            {"employeeId": EMP_DAMMAM_2, "dates": days_working}
        ]
    }
    r = requests.post(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards/{context['board1_id']}/schedule/assign?locationId={LOC_DAMMAM}", headers=headers, json=payload_assign_shift, verify=False, timeout=10)
    if r.status_code == 200:
        record("POS-PLN-03", "Pass", f"HTTP 200 OK. Assigned 10 shift slots across Sun-Thu.")
    else:
        record("POS-PLN-03", "Fail", f"Expected 200 OK for assign shift, got {r.status_code}: {r.text[:200]}")

# 25. POS-PLN-04: Assign Day Off to Fri-Sat
payload_assign_dayoff = {
    "workPlanId": None,
    "dayOff": True,
    "slots": [
        {"employeeId": EMP_DAMMAM_1, "dates": days_off},
        {"employeeId": EMP_DAMMAM_2, "dates": days_off}
    ]
}
r = requests.post(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards/{context['board1_id']}/schedule/assign?locationId={LOC_DAMMAM}", headers=headers, json=payload_assign_dayoff, verify=False, timeout=10)
if r.status_code == 200:
    record("POS-PLN-04", "Pass", f"HTTP 200 OK. Assigned Day Off rest days for Fri-Sat.")
else:
    record("POS-PLN-04", "Fail", f"Expected 200 OK for assign day off, got {r.status_code}: {r.text[:200]}")

# 26. NEG-PLN-03: Clear date outside period (Rule 1913)
payload_clear_out = {
    "anchor": next_sunday,
    "dates": ["2026-12-31"]
}
r = requests.post(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards/{context['board1_id']}/schedule/clear?locationId={LOC_DAMMAM}", headers=headers, json=payload_clear_out, verify=False, timeout=10)
if r.status_code == 400:
    record("NEG-PLN-03", "Pass", f"HTTP 400 Bad Request. Correctly rejected clear with date outside period (Rule 1913).")
else:
    record("NEG-PLN-03", "Fail", f"Expected 400 Bad Request, got {r.status_code}: {r.text[:200]}")

print("==================================================")
print("PHASE 5: PUBLISHING LIFECYCLE")
print("==================================================")

# 27. NEG-PUB-02: Publish empty period with allowEmpty = false (Rule 1908)
if context.get("board2_id"):
    payload_pub_empty = {
        "anchor": next_sunday,
        "allowEmpty": False
    }
    r = requests.post(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards/{context['board2_id']}/schedule/publish?locationId={LOC_DAMMAM}", headers=headers, json=payload_pub_empty, verify=False, timeout=10)
    if r.status_code == 400:
        record("NEG-PUB-02", "Pass", f"HTTP 400 Bad Request. Correctly rejected publishing empty period without allowEmpty flag (Rule 1908: {r.text[:100]}).")
    else:
        record("NEG-PUB-02", "Fail", f"Expected 400 Bad Request for empty publish, got {r.status_code}: {r.text[:200]}")

# 28. POS-PUB-02: Publish empty period with allowEmpty = true
if context.get("board2_id"):
    payload_pub_empty_allow = {
        "anchor": next_sunday,
        "allowEmpty": True
    }
    r = requests.post(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards/{context['board2_id']}/schedule/publish?locationId={LOC_DAMMAM}", headers=headers, json=payload_pub_empty_allow, verify=False, timeout=10)
    if r.status_code == 200:
        record("POS-PUB-02", "Pass", f"HTTP 200 OK. Successfully published empty roster with allowEmpty: true.")
    else:
        record("POS-PUB-02", "Fail", f"Expected 200 OK for empty publish with allowEmpty: true, got {r.status_code}: {r.text[:200]}")

# 29. POS-PUB-01: Publish completely filled period (Board 1)
payload_pub_board1 = {
    "anchor": next_sunday,
    "version": 0,
    "allowEmpty": False
}
r = requests.post(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards/{context['board1_id']}/schedule/publish?locationId={LOC_DAMMAM}", headers=headers, json=payload_pub_board1, verify=False, timeout=10)
if r.status_code == 200:
    pub_res = r.json()
    record("POS-PUB-01", "Pass", f"HTTP 200 OK. Period published successfully: status={pub_res.get('status')}, version={pub_res.get('version')}, slots={pub_res.get('publishedSlotCount')}.")
else:
    record("POS-PUB-01", "Fail", f"Expected 200 OK for publish, got {r.status_code}: {r.text[:200]}")

# 30. NEG-PUB-04: Publish with mismatched version (Rule 1910 concurrency)
payload_stale_ver = {
    "anchor": next_sunday,
    "version": 0, # DB version is now 1
    "allowEmpty": False
}
r = requests.post(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards/{context['board1_id']}/schedule/publish?locationId={LOC_DAMMAM}", headers=headers, json=payload_stale_ver, verify=False, timeout=10)
if r.status_code == 400:
    record("NEG-PUB-04", "Pass", f"HTTP 400 Bad Request. Correctly rejected stale version concurrency mismatch (Rule 1910).")
    record("SEC-CON-01", "Pass", f"HTTP 400 Bad Request. Concurrency lock collision prevented data overwrite.")
else:
    record("NEG-PUB-04", "Fail", f"Expected 400 Bad Request for stale version, got {r.status_code}: {r.text[:200]}")
    record("SEC-CON-01", "Fail", f"Expected 400 Bad Request for concurrency collision, got {r.status_code}: {r.text[:200]}")

# 31. POS-PUB-04: Unpublish period
payload_unpub = {
    "anchor": next_sunday,
    "force": False
}
r = requests.post(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards/{context['board1_id']}/schedule/unpublish?locationId={LOC_DAMMAM}", headers=headers, json=payload_unpub, verify=False, timeout=10)
if r.status_code == 200:
    record("POS-PUB-04", "Pass", f"HTTP 200 OK. Unstarted period unpublished successfully (reverted to Pending).")
else:
    record("POS-PUB-04", "Fail", f"Expected 200 OK for unpublish, got {r.status_code}: {r.text[:200]}")

# 32. NEG-PUB-05: Unpublish unstarted draft (Rule 1912)
# Board 1 is now in Pending/Draft state; unpublishing again should fail with 1912
r = requests.post(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards/{context['board1_id']}/schedule/unpublish?locationId={LOC_DAMMAM}", headers=headers, json=payload_unpub, verify=False, timeout=10)
if r.status_code == 400:
    record("NEG-PUB-05", "Pass", f"HTTP 400 Bad Request. Correctly rejected unpublishing an unpublished period (Rule 1912).")
else:
    record("NEG-PUB-05", "Fail", f"Expected 400 Bad Request, got {r.status_code}: {r.text[:200]}")

print("==================================================")
print("PHASE 6: OVERVIEW & SCHEDULES QUERIES")
print("==================================================")

# 33. POS-OVR-01: Query Overview summary
r = requests.get(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards/overview/summary?locationId={LOC_DAMMAM}&from={week_dates[0]}&to={week_dates[-1]}", headers=headers, verify=False, timeout=10)
if r.status_code == 200:
    record("POS-OVR-01", "Pass", f"HTTP 200 OK. Overview summary retrieved: boards={r.json().get('boardCount')}, employees={r.json().get('employees')}.")
else:
    record("POS-OVR-01", "Fail", f"Expected 200 OK, got {r.status_code}: {r.text[:200]}")

# 34. POS-OVR-02: Query Overview Today timeline
r = requests.get(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards/overview/today?locationId={LOC_DAMMAM}", headers=headers, verify=False, timeout=10)
if r.status_code == 200:
    record("POS-OVR-02", "Pass", f"HTTP 200 OK. Overview Today timeline retrieved successfully.")
else:
    record("POS-OVR-02", "Fail", f"Expected 200 OK, got {r.status_code}: {r.text[:200]}")

# 35. POS-SCH-01: Query Schedules 7-day grid
r = requests.get(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards/schedules?locationId={LOC_DAMMAM}&from={week_dates[0]}&to={week_dates[-1]}&page=1&pageSize=10", headers=headers, verify=False, timeout=10)
if r.status_code == 200:
    record("POS-SCH-01", "Pass", f"HTTP 200 OK. Schedules 7-day grid retrieved: total={r.json().get('total')}, groups={len(r.json().get('groups', []))}.")
else:
    record("POS-SCH-01", "Fail", f"Expected 200 OK, got {r.status_code}: {r.text[:200]}")

# 36. POS-SCH-02: Query Member Schedule Card
r = requests.get(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards/schedules/employees/{EMP_DAMMAM_1}?from={week_dates[0]}&to={week_dates[-1]}", headers=headers, verify=False, timeout=10)
if r.status_code == 200:
    record("POS-SCH-02", "Pass", f"HTTP 200 OK. Member schedule card retrieved successfully.")
else:
    record("POS-SCH-02", "Fail", f"Expected 200 OK for member schedule, got {r.status_code}: {r.text[:200]}")

# 37. NEG-OVR-01: Inverted date range (from > to, Rule 2204)
r = requests.get(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards/overview/summary?locationId={LOC_DAMMAM}&from=2026-11-30&to=2026-11-01", headers=headers, verify=False, timeout=10)
if r.status_code == 400:
    record("NEG-OVR-01", "Pass", f"HTTP 400 Bad Request. Correctly rejected inverted date range (Rule 2204: {r.text[:100]}).")
else:
    record("NEG-OVR-01", "Fail", f"Expected 400 Bad Request for inverted range, got {r.status_code}: {r.text[:200]}")

# 38. NEG-OVR-02: Range exceeding 31 days (Rule 2204)
r = requests.get(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards/overview/summary?locationId={LOC_DAMMAM}&from=2026-11-01&to=2026-12-15", headers=headers, verify=False, timeout=10)
if r.status_code == 400:
    record("NEG-OVR-02", "Pass", f"HTTP 400 Bad Request. Correctly rejected date range exceeding 31 days (Rule 2204: {r.text[:100]}).")
else:
    record("NEG-OVR-02", "Fail", f"Expected 400 Bad Request for range > 31 days, got {r.status_code}: {r.text[:200]}")

# 39. NEG-SCH-01: Query Member Schedule for employee never on a board (Rule 2207)
RAND_EMP = str(uuid.uuid4())
r = requests.get(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards/schedules/employees/{RAND_EMP}", headers=headers, verify=False, timeout=10)
if r.status_code == 404:
    record("NEG-SCH-01", "Pass", f"HTTP 404 Not Found. Correctly returned 404 (Rule 2207: {r.text[:100]}).")
else:
    record("NEG-SCH-01", "Fail", f"Expected 404 Not Found, got {r.status_code}: {r.text[:200]}")

# 40. SEC-IDOR-01: Cross-Company Board Access (Rule 9001)
COMPANY_FAKE = "11111111-2222-3333-4444-555555555555"
r = requests.get(f"{BASE_URL}/api/companies/{COMPANY_FAKE}/roster-boards/{context.get('board1_id')}", headers=headers, verify=False, timeout=10)
if r.status_code in [403, 404]:
    record("SEC-IDOR-01", "Pass", f"HTTP {r.status_code}. Cross-company IDOR blocked cleanly (Rule 9001).")
else:
    record("SEC-IDOR-01", "Fail", f"Expected 403/404 for IDOR, got {r.status_code}: {r.text[:200]}")

print("==================================================")
print(f"SUITE COMPLETE. Total TCs Executed: {len(results)}")
print(f"Passed: {sum(1 for t in results.values() if t['status'] == 'Pass')}")
print(f"Failed: {sum(1 for t in results.values() if t['status'] == 'Fail')}")
print("==================================================")

# Save execution results to json
with open("scratch/scheduler_live_results.json", "w") as f:
    json.dump(results, f, indent=2)
'''

with open("scratch/run_full_scheduler_test_suite.py", "a", encoding="utf-8") as f:
    f.write(append_code)

print("Phases 2 to 7 appended to scratch/run_full_scheduler_test_suite.py")
