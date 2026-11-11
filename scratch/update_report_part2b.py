import sys

sys.stdout.reconfigure(encoding='utf-8')

new_part2b_content = """### Summary Matrix: Attendance 4 Live Execution (13 Scenarios)

> [!IMPORTANT]
> **Part 2B Live Re-Verification Update (05-November-2026):**
> Comprehensive live re-execution of all 13 Attendance 4 user scenarios confirmed that the unhandled HTTP 500 `ValidationException` crashes (`DEFECT-20261028-02`) affecting `USER-22` (Empty PATCH body) and `USER-37` (Invalid DayEnum 8) have been **🟢 FULLY RESOLVED**. The server now intercepts FluentValidation exceptions cleanly in `GlobalExceptionHandlerMiddleware` and returns RFC 9110 compliant **HTTP 400 Bad Request** with standard error code `Cit.Attendance:Validation`.
>
> **Attendance 4 Suite Scorecard:**
> * **Historical Execution (28-Oct-2026):** 13 Total | 11 Passed | 2 Failed (84.6% Pass Rate)
> * **Live Re-Verified (05-Nov-2026):** 13 Total | **13 Passed** | **0 Failed** (🟢 **100.0% Pass Rate**)

| TC ID | Severity | Scenario / Test Focus | HTTP Route & Method | Server Response Code | Live Outcome | Verification Finding (05-Nov-2026 Re-Verification) |
|:---:|:---:|---|---|:---:|:---:|---|
| **`USER-08`** | **P1** | One Default Rule: Attempt 2nd CDWT when Flexi v2.0 active | `POST /worktemplates/fixed` | **HTTP 400 Bad Request** | **✅ PASS** | **Re-Verified Live:** Blocked by `Cit.Attendance:1010` ("Company default already exists.") |
| **`USER-21`** | **P1** | Immutability: Attempt to modify `shortCode` via PATCH | `PATCH /worktemplates/flexi/{id}` | **HTTP 400 Bad Request** | **✅ PASS** | **Re-Verified Live:** Blocked by `Cit.Attendance:1107` ("A work template's short code cannot be changed after it is created.") |
| **`USER-22`** | **P2** | Guard: Reject empty request body `{}` on PATCH | `PATCH /worktemplates/flexi/{id}` | **HTTP 400 Bad Request** | **🟢 RESOLVED / PASS** | **Verified Fixed Live:** HTTP 500 crash eliminated. Server returns HTTP 400 with `Cit.Attendance:Validation` (`DEFECT-20261028-02` Fixed) |
| **`USER-37`** | **P1** | Boundary: DayEnum validation with invalid integer `8` | `POST /worktemplates/flexi` | **HTTP 400 Bad Request** | **🟢 RESOLVED / PASS** | **Verified Fixed Live:** HTTP 500 crash eliminated. Server returns HTTP 400 with `Cit.Attendance:Validation` (`DEFECT-20261028-02` Fixed) |
| **`USER-81`** | **P1** | Immutability: Attempt to edit an archived version ID | `PATCH /worktemplates/flexi/{v1Id}` | **HTTP 400 Bad Request** | **✅ PASS** | **Re-Verified Live:** Blocked by `Cit.Attendance:1104` ("Invalid work template state transition.") / `Cit.Attendance:1107` |
| **`USER-82`** | **P1** | Error Handling: Edit non-existent template GUID | `PATCH /worktemplates/flexi/{fakeId}` | **HTTP 400 Bad Request** | **✅ PASS** | **Re-Verified Live:** Blocked by `Cit.Attendance:1101` ("Work template not found.") |
| **`USER-83`** | **P1** | Security: Cross-company template mutation attempt | `PATCH /worktemplates/flexi/{c2Id}` | **HTTP 400 Bad Request** | **✅ PASS** | **Re-Verified Live:** Blocked by `Cit.Attendance:9001` ("The provided company does not match the entity company.") |
| **`USER-102`** | **P0** | Verification: GET by ID on Flexible Daily CDWT v2.0 | `GET /worktemplates/{v2Id}` | **HTTP 200 OK** | **✅ PASS** | **Re-Verified Live:** Returns full schedule structure with 7 days and daily duration `480m` |
| **`USER-117`** | **P0** | Audit: GET Version History full chain verification | `GET /company-default/versions` | **HTTP 200 OK** | **✅ PASS** | **Re-Verified Live:** Returns 2 versions [v2.0 Active, v1.0 Archived] with full change summary diff |
| **`USER-118`** | **P1** | Sync: GET Sync Status banner dynamic state | `GET /company-default/sync-status` | **HTTP 200 OK** | **✅ PASS** | **Re-Verified Live:** Returns `hasCompanyDefault: true` and dynamic sync state |
| **`USER-119`** | **P1** | Helper: GET Short Code availability check | `GET /short-code/availability` | **HTTP 200 OK** | **✅ PASS** | **Re-Verified Live:** Validates code format and availability |
| **`USER-120`** | **P2** | Helper: GET Short Code suggestions generation | `GET /short-code/suggestions` | **HTTP 200 OK** | **✅ PASS** | **Re-Verified Live:** Generates base suggestions |
| **`USER-123`** | **P0** | Security: ShortCode strict lockout across all types | `PATCH /worktemplates/flexi/{id}` | **HTTP 400 Bad Request** | **✅ PASS** | **Re-Verified Live:** Confirms strict shortCode immutability (`Cit.Attendance:1107`) |

---

### Detailed Test Scenarios & Visual Evidence

#### 1. Scenario `USER-08`: One Default Rule Guard (`Cit.Attendance:1010`)
* **Objective:** Ensure a company cannot have more than one Company Default Work Template active at the same time.
* **Exact Request Sent:**
  ```http
  POST /api/companies/3a247436-8669-844a-7d2f-1a209af02d8e/worktemplates/fixed HTTP/1.1
  Host: attendance2.dev.zoolwork.com
  Authorization: Bearer <JWT>
  __tenant: Attendance
  Content-Type: application/json

  {
    "templateName": { "en": "Second CDWT Attempt" },
    "shortCode": "ATT4FX2",
    "isDefault": true,
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "fixedTimeSlots": [
      { "dayEnum": 1, "isWorkingDay": true, "workDurationInMinutes": 480, "startTime": "09:00:00", "endTime": "17:00:00", "recurrenceOfMonth": [1, 2, 3, 4, 5] },
      { "dayEnum": 2, "isWorkingDay": true, "workDurationInMinutes": 480, "startTime": "09:00:00", "endTime": "17:00:00", "recurrenceOfMonth": [1, 2, 3, 4, 5] },
      { "dayEnum": 3, "isWorkingDay": true, "workDurationInMinutes": 480, "startTime": "09:00:00", "endTime": "17:00:00", "recurrenceOfMonth": [1, 2, 3, 4, 5] },
      { "dayEnum": 4, "isWorkingDay": true, "workDurationInMinutes": 480, "startTime": "09:00:00", "endTime": "17:00:00", "recurrenceOfMonth": [1, 2, 3, 4, 5] },
      { "dayEnum": 5, "isWorkingDay": true, "workDurationInMinutes": 480, "startTime": "09:00:00", "endTime": "17:00:00", "recurrenceOfMonth": [1, 2, 3, 4, 5] },
      { "dayEnum": 6, "isWorkingDay": false, "workDurationInMinutes": 0, "startTime": "00:00:00", "endTime": "00:00:00", "recurrenceOfMonth": [1, 2, 3, 4, 5] },
      { "dayEnum": 7, "isWorkingDay": false, "workDurationInMinutes": 0, "startTime": "00:00:00", "endTime": "00:00:00", "recurrenceOfMonth": [1, 2, 3, 4, 5] }
    ]
  }
  ```
* **Actual Server Response Received:**
  ```http
  HTTP/1.1 400 Bad Request
  Content-Type: application/json; charset=utf-8

  {
    "error": {
      "code": "Cit.Attendance:1010",
      "message": "Company default already exists.",
      "data": {
        "CompanyId": "3a247436-8669-844a-7d2f-1a209af02d8e",
        "DefaultTemplateId": "53470658-5f9b-47b4-b254-f96b9501401c"
      }
    }
  }
  ```
* **Status:** **✅ PASS (RE-VERIFIED LIVE 05-NOV-2026)**. Successfully rejected duplicate default creation with `Cit.Attendance:1010`.
* **Visual Evidence:**

![One Default Rule Guard 1010](defect_evidence/evidence_13_att4_one_default_guard_1010.png)

---

#### 2. Scenario `USER-21` / `USER-123`: ShortCode Immutability Guard (`Cit.Attendance:1107`)
* **Objective:** Verify that `shortCode` cannot be modified via PATCH after creation.
* **Exact Request Sent:**
  ```http
  PATCH /api/companies/3a247436-8669-844a-7d2f-1a209af02d8e/worktemplates/flexi/53470658-5f9b-47b4-b254-f96b9501401c HTTP/1.1
  Host: attendance2.dev.zoolwork.com
  Authorization: Bearer <JWT>
  Content-Type: application/json

  {
    "templateName": { "en": "Attendance 4 Flexi Renamed" },
    "shortCode": "HACKCOD",
    "flexibleType": 1,
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "flexiTimeSlots": [
      { "dayEnum": 1, "isWorkingDay": true, "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5] },
      { "dayEnum": 2, "isWorkingDay": true, "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5] },
      { "dayEnum": 3, "isWorkingDay": true, "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5] },
      { "dayEnum": 4, "isWorkingDay": true, "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5] },
      { "dayEnum": 5, "isWorkingDay": true, "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5] },
      { "dayEnum": 6, "isWorkingDay": false, "workDurationInMinutes": 0, "recurrenceOfMonth": [1, 2, 3, 4, 5] },
      { "dayEnum": 7, "isWorkingDay": false, "workDurationInMinutes": 0, "recurrenceOfMonth": [1, 2, 3, 4, 5] }
    ]
  }
  ```
* **Actual Server Response Received:**
  ```http
  HTTP/1.1 400 Bad Request
  Content-Type: application/json; charset=utf-8

  {
    "error": {
      "code": "Cit.Attendance:1107",
      "message": "A work template's short code cannot be changed after it is created.",
      "data": {
        "workTemplateId": "53470658-5f9b-47b4-b254-f96b9501401c",
        "shortCode": "ATT4FLX",
        "requestedShortCode": "HACKCOD"
      }
    }
  }
  ```
* **Status:** **✅ PASS (RE-VERIFIED LIVE 05-NOV-2026)**. Server rejects tampering with `shortCode` and enforces strict immutability.
* **Visual Evidence:**

![ShortCode Locked Cit.Attendance:1107](defect_evidence/evidence_14_att4_patch_shortcode_locked_1107.png)

---

#### 3. Scenario `USER-22`: Empty Request Body on PATCH ➔ 🟢 RESOLVED / VERIFIED FIXED LIVE (HTTP 400 Bad Request)
* **Objective:** Ensure calling PATCH with an empty body `{}` returns a clean RFC 9110 HTTP 400 Bad Request instead of an unhandled HTTP 500 crash.
* **Historical Baseline (28-Oct-2026):** Server threw an unhandled `ValidationException` resulting in **HTTP 500 Internal Server Error** (`DEFECT-20261028-02`).
* **Historical Visual Evidence (28-Oct-2026):**

![Empty Payload HTTP 500 ValidationException](defect_evidence/evidence_15_att4_patch_empty_payload_500.png)
*Figure: Historical Swagger UI live test of scenario USER-22 on Attendance 4 returning unhandled HTTP 500 ValidationException.*

* **Live Re-Verification Execution (05-Nov-2026):**
  * **Endpoint:** `PATCH /api/companies/3a247436-8669-844a-7d2f-1a209af02d8e/worktemplates/flexi/53470658-5f9b-47b4-b254-f96b9501401c`
  * **Payload Sent:** `{}`
  * **Actual Server Response Received:**
    ```http
    HTTP/1.1 400 Bad Request
    Content-Type: application/json; charset=utf-8

    {
      "error": {
        "code": "Cit.Attendance:Validation",
        "message": "An English template name is required. All 7 days of the week must be defined, each day once.",
        "details": null,
        "data": null,
        "validationErrors": [
          {
            "message": "An English template name is required.",
            "members": [
              "TemplateName"
            ]
          },
          {
            "message": "All 7 days of the week must be defined, each day once.",
            "members": [
              "FlexiTimeSlots"
            ]
          }
        ]
      }
    }
    ```
* **Status:** 🟢 **RESOLVED / VERIFIED FIXED LIVE (05-Nov-2026)**. The HTTP 500 server crash is completely eliminated; `GlobalExceptionHandlerMiddleware` catches `ValidationException` and returns standard HTTP 400 Bad Request with `Cit.Attendance:Validation`.

---

#### 4. Scenario `USER-83`: Cross-Company Boundary Isolation (`Cit.Attendance:9001`)
* **Objective:** Ensure a user cannot patch a template belonging to Company 2 using Company 4 route URL.
* **Exact Request Sent:**
  ```http
  PATCH /api/companies/3a247436-8669-844a-7d2f-1a209af02d8e/worktemplates/flexi/99a56911-0d30-40e6-8fa4-ca64da88930c HTTP/1.1
  Host: attendance2.dev.zoolwork.com
  Authorization: Bearer <JWT>
  Content-Type: application/json

  {
    "templateName": { "en": "Cross-Company Attack" },
    "shortCode": "ATT4FLX",
    "flexibleType": 1,
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "flexiTimeSlots": [
      { "dayEnum": 1, "isWorkingDay": true, "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5] },
      { "dayEnum": 2, "isWorkingDay": true, "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5] },
      { "dayEnum": 3, "isWorkingDay": true, "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5] },
      { "dayEnum": 4, "isWorkingDay": true, "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5] },
      { "dayEnum": 5, "isWorkingDay": true, "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5] },
      { "dayEnum": 6, "isWorkingDay": false, "workDurationInMinutes": 0, "recurrenceOfMonth": [1, 2, 3, 4, 5] },
      { "dayEnum": 7, "isWorkingDay": false, "workDurationInMinutes": 0, "recurrenceOfMonth": [1, 2, 3, 4, 5] }
    ]
  }
  ```
* **Actual Server Response Received:**
  ```http
  HTTP/1.1 400 Bad Request
  Content-Type: application/json; charset=utf-8

  {
    "error": {
      "code": "Cit.Attendance:9001",
      "message": "The provided company does not match the entity company.",
      "data": {
        "entityCompanyId": "3a247435-3cea-83ae-6a9f-6dda99f386a3",
        "requestCompanyId": "3a247436-8669-844a-7d2f-1a209af02d8e"
      }
    }
  }
  ```
* **Status:** **✅ PASS (RE-VERIFIED LIVE 05-NOV-2026)**. Cross-company tenancy boundary strictly enforced with `Cit.Attendance:9001`.

---

#### 5. Scenario `USER-37`: Boundary DayEnum Validation with Invalid Integer 8 ➔ 🟢 RESOLVED / VERIFIED FIXED LIVE (HTTP 400 Bad Request)
* **Objective:** Ensure invalid DayEnum integer (`8`) in `flexiTimeSlots` returns clean HTTP 400 Bad Request instead of an unhandled HTTP 500 crash.
* **Historical Baseline (28-Oct-2026):** Server threw unhandled `ValidationException` resulting in **HTTP 500 Internal Server Error** (`DEFECT-20261028-02`).
* **Live Re-Verification Execution (05-Nov-2026):**
  * **Endpoint:** `POST /api/companies/3a247436-8669-844a-7d2f-1a209af02d8e/worktemplates/flexi`
  * **Payload Sent:**
    ```json
    {
      "templateName": { "en": "Invalid Day 8 Flexi" },
      "shortCode": "INVDAY8",
      "isDefault": false,
      "flexibleType": 1,
      "totalWorkDurationInMinutes": 480,
      "totalWorkingDays": 5,
      "totalDaysOff": 2,
      "flexiTimeSlots": [
        { "day": 8, "isWorkingDay": true, "expectedDurationInMinutes": 480 },
        { "day": 2, "isWorkingDay": true, "expectedDurationInMinutes": 480 },
        { "day": 3, "isWorkingDay": true, "expectedDurationInMinutes": 480 },
        { "day": 4, "isWorkingDay": true, "expectedDurationInMinutes": 480 },
        { "day": 5, "isWorkingDay": true, "expectedDurationInMinutes": 480 },
        { "day": 6, "isWorkingDay": false, "expectedDurationInMinutes": 0 },
        { "day": 7, "isWorkingDay": false, "expectedDurationInMinutes": 0 }
      ]
    }
    ```
  * **Actual Server Response Received:**
    ```http
    HTTP/1.1 400 Bad Request
    Content-Type: application/json; charset=utf-8

    {
      "error": {
        "code": "Cit.Attendance:Validation",
        "message": "All 7 days of the week must be defined, each day once. A working day's work duration must be greater than 0 minutes.",
        "details": null,
        "data": null,
        "validationErrors": [
          {
            "message": "All 7 days of the week must be defined, each day once.",
            "members": [
              "FlexiTimeSlots"
            ]
          },
          {
            "message": "A working day's work duration must be greater than 0 minutes.",
            "members": [
              "FlexiTimeSlots"
            ]
          }
        ]
      }
    }
    ```
* **Status:** 🟢 **RESOLVED / VERIFIED FIXED LIVE (05-Nov-2026)**. The HTTP 500 crash is eliminated; server cleanly returns HTTP 400 Bad Request with `Cit.Attendance:Validation`.

---

"""

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    content = f.read()

target_start = "### Summary Matrix: Attendance 4 Live Execution (13 Scenarios)"
target_end = "# 📅 Part 3: Defects Identified on 28 October 2026 (LIVE EXECUTION & USER SCENARIOS)"

idx_start = content.find(target_start)
idx_end = content.find(target_end)

if idx_start != -1 and idx_end != -1:
    new_content = content[:idx_start] + new_part2b_content + content[idx_end:]
    with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully replaced Part 2B in report!")
else:
    print(f"Indices not found: start={idx_start}, end={idx_end}")

