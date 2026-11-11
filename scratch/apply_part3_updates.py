import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update DEFECT-20261028-01
t1_anchor = '      .WithMessage("Daily flexible work duration cannot exceed 1440 minutes (24 hours).");\n  ```'
t1_add = """
* **Status:** 🟢 **RESOLVED / VERIFIED FIXED LIVE (05-Nov-2026)**
* **Live Re-Verification Execution (05-Nov-2026):**
  - **Endpoint:** `POST /api/companies/3a247436-8669-844a-7d2f-1a209af02d8e/worktemplates/flexi`
  - **Payload Sent:** `totalWorkDurationInMinutes: 1500` with slot `workDurationInMinutes: 1500`
  - **Actual Server Response Received:**
    ```http
    HTTP/1.1 400 Bad Request
    Content-Type: application/json; charset=utf-8

    {
      "error": {
        "code": "Cit.Attendance:Validation",
        "message": "A day's work duration cannot exceed 23 hours 59 minutes.",
        "details": null,
        "data": null,
        "validationErrors": [
          {
            "message": "A day's work duration cannot exceed 23 hours 59 minutes.",
            "members": [
              "FlexiTimeSlots[0]"
            ]
          }
        ]
      }
    }
    ```
  - **Verdict:** 🟢 **RESOLVED**. The server strictly enforces daily duration boundaries <= 1,439 minutes (23h 59m) and cleanly returns RFC 9110 HTTP 400 Bad Request with `Cit.Attendance:Validation`."""

if t1_anchor in text:
    text = text.replace(t1_anchor, t1_anchor + "\n" + t1_add)
    print("Updated DEFECT-20261028-01 deep-dive!")
else:
    print("Warning: t1_anchor not found")

# 2. Update DEFECT-20261028-03
t3_anchor = '      throw new BusinessException("Cit.Attendance:1202", "Active Company Default Work Template cannot be archived or deleted.");\n  }\n  ```'
t3_add = """
* **Status:** 🟢 **RESOLVED / VERIFIED FIXED LIVE (05-Nov-2026)**
* **Live Re-Verification Execution (05-Nov-2026):**
  - **Target Endpoints Tested:** `PATCH /api/companies/3a247436-8669-844a-7d2f-1a209af02d8e/worktemplates/53470658-5f9b-47b4-b254-f96b9501401c/archive` and `/delete`
  - **Actual Server Response Received:**
    ```http
    HTTP/1.1 400 Bad Request
    Content-Type: application/json; charset=utf-8

    {
      "error": {
        "code": "Cit.Attendance:1003",
        "message": "Company default cannot be deleted.",
        "details": null,
        "data": {
          "workTemplateId": "53470658-5f9b-47b4-b254-f96b9501401c",
          "companyId": "3a247436-8669-844a-7d2f-1a209af02d8e"
        },
        "validationErrors": null
      }
    }
    ```
  - **Verdict:** 🟢 **RESOLVED**. Both `/archive` and `/delete` endpoints strictly guard active Company Default templates, rejecting destructive operations with HTTP 400 Bad Request and error code `Cit.Attendance:1003`."""

if t3_anchor in text:
    text = text.replace(t3_anchor, t3_anchor + "\n" + t3_add)
    print("Updated DEFECT-20261028-03 deep-dive!")
else:
    print("Warning: t3_anchor not found")

# 3. Update DEFECT-20261028-04
t4_anchor = '      throw new SbpBusinessException("Cit.Attendance:9001", "The provided company ID does not exist or does not match your assigned tenant.");\n  }\n  ```'
t4_add = """
* **Status:** 🔴 **FAIL / NOT FIXED (Re-verified 05-Nov-2026)**
* **Live Re-Verification Execution (05-Nov-2026):**
  - **Request:** `GET /api/companies/00000000-0000-0000-0000-000000009999/worktemplates`
  - **Actual Response:** `HTTP/1.1 200 OK` with body `{"message":"No Work Templates are found","templates":[]}`
  - **Verdict:** 🔴 **FAIL / OPEN**. Handlers continue to fall back to an empty template list rather than querying company existence or validating company-tenant ownership to throw `Cit.Attendance:9001` or return HTTP 404."""

if t4_anchor in text:
    text = text.replace(t4_anchor, t4_anchor + "\n" + t4_add)
    print("Updated DEFECT-20261028-04 deep-dive!")
else:
    print("Warning: t4_anchor not found")

# 4. Update DEFECT-20261028-05
t5_anchor = '      Ar = new LocalizedString { Name = _currentTenant.ArabicName ?? "حضور" }\n  };\n  ```'
t5_add = """
* **Status:** 🔴 **FAIL / NOT FIXED (Re-verified 05-Nov-2026)**
* **Live Re-Verification Execution (05-Nov-2026):**
  - Re-audited template documents in MongoDB collection `ERP.Attendance.WorkTemplates` across Attendance 3 and Attendance 4.
  - Documents created without client tenant payload persist `TenantName: {}` (empty object).
  - **Verdict:** 🔴 **FAIL / OPEN**. Server-side pre-population from `_currentTenant.Name` remains unimplemented in command handlers."""

if t5_anchor in text:
    text = text.replace(t5_anchor, t5_anchor + "\n" + t5_add)
    print("Updated DEFECT-20261028-05 deep-dive!")
else:
    print("Warning: t5_anchor not found")

# 5. Update DEFECT-20261028-06
t6_anchor = '* **Required Fix:** Remove `tenantName` from all 26 DTO models. Inject `TenantName` purely on the backend from `ICurrentTenant`.'
t6_add = """
* **Status:** 🔴 **FAIL / NOT FIXED (Re-verified 05-Nov-2026)**
* **Live Re-Verification Execution (05-Nov-2026):**
  - Re-scanned `https://attendance2.dev.zoolwork.com/swagger/v1/swagger.json`: all 26 request DTOs continue to declare `tenantName` in the schema.
  - Live probe with spoofed `tenantName` persists client value directly into MongoDB with `HTTP 200 OK`.
  - **Verdict:** 🔴 **FAIL / OPEN**. DTO parameter purge and server-side JWT claim binding remain pending."""

if t6_anchor in text:
    text = text.replace(t6_anchor, t6_anchor + "\n" + t6_add)
    print("Updated DEFECT-20261028-06 deep-dive!")
else:
    print("Warning: t6_anchor not found")

# 6. Update DEFECT-20261028-07
t7_anchor = '  RuleFor(x => x.DurationInMinutes).GreaterThan(0).WithMessage("Break duration must be greater than zero.");\n  ```'
t7_add = """
* **Status:** 🟢 **RESOLVED / VERIFIED FIXED LIVE (05-Nov-2026)**
* **Live Re-Verification Execution (05-Nov-2026):**
  - **Grace Period Endpoint:** `POST /api/companies/3a247435-e31d-ef15-8cc9-62c587f4eb3f/attpolicies/graceperiod`
    - **Payload Sent:** `lateCheckInGraceMinutes: -15`
    - **Actual Server Response Received:** `HTTP 400 Bad Request` with `Cit.Attendance:Validation` ("Late check in grace minutes must be greater than or equal to 0.")
  - **Break Policy Endpoint:** `POST /api/companies/3a247435-e31d-ef15-8cc9-62c587f4eb3f/attpolicies/break`
    - **Payload Sent:** `totalBreakDurationInMinutes: -60`, `breaks: [{"durationMinutes": -60}]`
    - **Actual Server Response Received:** `HTTP 400 Bad Request` with `Cit.Attendance:Validation` ("Total break duration in minutes must be greater than 0.")
  - **Verdict:** 🟢 **RESOLVED**. Negative policy parameters are now strictly validated by FluentValidation and return clean HTTP 400 Bad Request."""

if t7_anchor in text:
    text = text.replace(t7_anchor, t7_anchor + "\n" + t7_add)
    print("Updated DEFECT-20261028-07 deep-dive!")
else:
    print("Warning: t7_anchor not found")

# 7. Update Day 3 Checklist in Part 5
old_chk_01 = '- [ ] **P0 (`DEFECT-20261028-01`):** Add `.InclusiveBetween(1, 1440)` rule in `CreateFlexiWorkTemplateCommandValidator` to reject daily work duration exceeding 24 hours.'
new_chk_01 = '- [x] **P0 (`DEFECT-20261028-01`):** Add `.InclusiveBetween(1, 1440)` rule in `CreateFlexiWorkTemplateCommandValidator` to reject daily work duration exceeding 24 hours. *(Verified Fixed Live 05-Nov-2026: HTTP 400 Bad Request — "A day\'s work duration cannot exceed 23 hours 59 minutes.")*'

old_chk_03 = '- [ ] **P1 (`DEFECT-20261028-03`):** Add guard in `ArchiveWorkTemplateCommandHandler` and `DeleteWorkTemplateCommandHandler` rejecting archiving/deletion of active Company Default Work Template (`Cit.Attendance:1202`).'
new_chk_03 = '- [x] **P1 (`DEFECT-20261028-03`):** Add guard in `ArchiveWorkTemplateCommandHandler` and `DeleteWorkTemplateCommandHandler` rejecting archiving/deletion of active Company Default Work Template (`Cit.Attendance:1202`). *(Verified Fixed Live 05-Nov-2026: HTTP 400 Bad Request — Cit.Attendance:1003 "Company default cannot be deleted.")*'

if old_chk_01 in text:
    text = text.replace(old_chk_01, new_chk_01)
    print("Updated checklist item for DEFECT-20261028-01!")

if old_chk_03 in text:
    text = text.replace(old_chk_03, new_chk_03)
    print("Updated checklist item for DEFECT-20261028-03!")

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(text)
print("Finished updating main report!")

