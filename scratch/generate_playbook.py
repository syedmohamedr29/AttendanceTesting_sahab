# -*- coding: utf-8 -*-
"""
Generates CDWT_Manual_Testing_Playbook.md with all 53 test cases.
Each test case contains:
 - Option 1: Swagger UI Steps & Exact Input
 - Option 2: Postman / cURL Payload JSON & Steps
 - Expected Code & Verification Criteria
 - Excel Entry Data
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

playbook_content = """# Company Default Work Template (CDWT) — Manual Testing Playbook
## Complete Step-by-Step Test Data Guide for All 53 Edge Cases (Option 1: Swagger | Option 2: Postman/Payload)

> **Target Microservice:** `SP.AttendanceSvc` (.NET 9)  
> **Base DEV URL:** `https://attendance2.dev.zoolwork.com`  
> **Auth Server:** `https://auth8.dev.zoolwork.com/connect/token` (`tenant: Attendance`)  
> **Swagger UI:** `https://attendance2.dev.zoolwork.com/swagger/index.html`  
> **Target Companies:**  
> • `Attendance 2`: `3a247435-3cea-83ae-6a9f-6dda99f386a3` (Fixed Active CDWT v3.0)  
> • `Attendance 3`: `3a247435-e31d-ef15-8cc9-62c587f4eb3f` (Fixed Active CDWT v2.0)  
> • `Attendance 4`: `3a247436-8669-844a-7d2f-1a209af02d8e` (Flexi Active CDWT v2.0)  
> **Master Test Workbook:** [`CompanyDefault_DTO_Validation_TestCases.xlsx`](file:///d:/Code/Attendance%20Testing/CompanyDefault_DTO_Validation_TestCases.xlsx)

---

## 📋 Table of Contents
1. [Category 1: Route & Security (CDWT-DTO-01 to 07, 53)](#category-1-route--security-cdwt-dto-01-to-07-53)
2. [Category 2: Common Top-Level DTO Validations (CDWT-DTO-08 to 18)](#category-2-common-top-level-dto-validations-cdwt-dto-08-to-18)
3. [Category 3: Fixed Work Template Validations (CDWT-DTO-19 to 26)](#category-3-fixed-work-template-validations-cdwt-dto-19-to-26)
4. [Category 4: Flexible Work Template Validations (CDWT-DTO-27 to 34)](#category-4-flexible-work-template-validations-cdwt-dto-27-to-34)
5. [Category 5: Split Work Template Validations (CDWT-DTO-35 to 40)](#category-5-split-work-template-validations-cdwt-dto-35-to-40)
6. [Category 6: PATCH & Immutability Validations (CDWT-DTO-41 to 52)](#category-6-patch--immutability-validations-cdwt-dto-41-to-52)

---

## Category 1: Route & Security (CDWT-DTO-01 to 07, 53)

### `CDWT-DTO-01`: Missing Authorization Header in Request
* **Scope:** Security Filter
* **Expected Result:** `HTTP 401 Unauthorized`

* **Option 1 (Swagger UI Steps):**
  1. Open Swagger, click **Authorize** at top right -> click **Logout** (lock icon must be open/unlocked).
  2. Expand `POST /api/companies/{companyId}/worktemplates/fixed`.
  3. In `companyId`, enter: `3a247435-3cea-83ae-6a9f-6dda99f386a3`.
  4. In Request body, enter: `{}`.
  5. Click **Execute** -> Verify Response is **`401 Unauthorized`**.

* **Option 2 (Postman / Payload Steps):**
  * **Method:** `POST`
  * **URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`
  * **Auth:** Set to `No Auth` (no Authorization header).
  * **Headers:** `Content-Type: application/json`, `__tenant: Attendance`.
  * **Body:** `{}`
  * **Verify:** Returns `HTTP 401 Unauthorized` with `Www-Authenticate: Bearer`.

* **Excel Logging:** Col L (`Manual Status`): `Pass` | Col M: `401` | Col N: `Server cleanly blocks unauthenticated request.`

---

### `CDWT-DTO-02`: Expired or Forged Bearer Token
* **Scope:** JWT Token Verification
* **Expected Result:** `HTTP 401 Unauthorized`

* **Option 1 (Swagger UI Steps):**
  1. Click **Authorize** lock button in Swagger.
  2. In text box, enter a fake token: `12345`.
  3. Click **Authorize**, then click **Close**.
  4. Expand `POST /api/companies/{companyId}/worktemplates/fixed`.
  5. In `companyId`: `3a247435-3cea-83ae-6a9f-6dda99f386a3`, Body: `{}`.
  6. Click **Execute** -> Verify Response is **`401 Unauthorized`**.

* **Option 2 (Postman / Payload Steps):**
  * **Method:** `POST`
  * **URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`
  * **Headers:** `Authorization: Bearer invalid_token_99999`, `Content-Type: application/json`, `__tenant: Attendance`.
  * **Body:** `{}`
  * **Verify:** Returns `HTTP 401 Unauthorized` with `Www-Authenticate: Bearer error="invalid_token"`.

* **Excel Logging:** Col L: `Pass` | Col M: `401` | Col N: `Returns HTTP 401 with error="invalid_token". Note: Expired JWTs in DEV bypass verification (DEFECT-20261029-01).`

---

### `CDWT-DTO-03`: JWT Token Missing Tenant Claim
* **Scope:** Multi-Tenancy Boundary
* **Expected Result:** `HTTP 401 / 403 SbpAuthorizationException`

* **Option 1 (Swagger UI Steps):**
  1. Login with a user token that has no `__tenant` claim assigned (or standard cross-tenant user).
  2. Execute `POST /api/companies/{companyId}/worktemplates/fixed`.
  3. Verify server rejects with `HTTP 401` or `HTTP 403 Forbidden`.

* **Option 2 (Postman / Payload Steps):**
  * Use a bearer token from an unassigned tenant or pass empty tenant claim.
  * **Verify:** Response returns `401` or `403` with tenant validation error.

* **Excel Logging:** Col L: `Pass` | Col M: `401 / 403` | Col N: `Tenant claim requirement enforced.`

---

### `CDWT-DTO-04`: Client Tenant Spoofing Attempt via Header
* **Scope:** Header vs Token Claim Precedence
* **Expected Result:** Header ignored; token claims strictly enforced

* **Option 1 (Swagger UI Steps):**
  1. Authorize with your valid token (`syed.mohamed@comm-it.in`).
  2. Execute `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`.
  3. In Swagger `__tenant` header parameter, type: `MaliciousHackedTenant`.
  4. Click **Execute** -> Verify request does NOT switch to MaliciousHackedTenant; token's `Attendance` tenant claim governs execution.

* **Option 2 (Postman / Payload Steps):**
  * **Header:** `__tenant: FakeAttackerTenant`
  * **Header:** `Authorization: Bearer <valid-Attendance-token>`
  * **Verify:** Server processes under token tenant or rejects. Does not grant access to fake tenant.

* **Excel Logging:** Col L: `Pass` | Col M: `200 / 400` | Col N: `Token tenant claim overrides client header; spoofing blocked.`

---

### `CDWT-DTO-05`: Zero GUID companyId in Route Parameter
* **Scope:** Route Parsing & Company Resolution
* **Expected Result:** `HTTP 404 Company Not Found` (Actual: HTTP 200 `[]` — DEFECT-20261028-04)

* **Option 1 (Swagger UI Steps):**
  1. Expand `GET /api/companies/{companyId}/worktemplates`.
  2. In `companyId`, enter: `00000000-0000-0000-0000-000000000000`.
  3. Click **Execute**.
  4. Notice: Server returns **`HTTP 200 OK` with `[]`** instead of `404 Not Found`.

* **Option 2 (Postman / Payload Steps):**
  * **Method:** `GET`
  * **URL:** `https://attendance2.dev.zoolwork.com/api/companies/00000000-0000-0000-0000-000000000000/worktemplates`
  * **Headers:** `Authorization: Bearer <token>`, `__tenant: Attendance`.
  * **Verify:** Check if response is 404 (Expected) or 200 `[]` (Known Defect `DEFECT-20261028-04`).

* **Excel Logging:** Col L: `Failed` | Col M: `200` | Col N: `DEFECT-20261028-04: Returns HTTP 200 [] instead of HTTP 404 Company Not Found.`

---

### `CDWT-DTO-06`: Malformed Non-Hex companyId in Route
* **Scope:** Route Constraint Parsing
* **Expected Result:** `HTTP 400 Bad Request` or `HTTP 404 Not Found`

* **Option 1 (Swagger UI Steps):**
  1. Expand `GET /api/companies/{companyId}/worktemplates`.
  2. In `companyId`, enter: `invalid-company-guid-xyz`.
  3. Click **Execute** -> Verify response returns `HTTP 404` or `HTTP 400`.

* **Option 2 (Postman / Payload Steps):**
  * **URL:** `https://attendance2.dev.zoolwork.com/api/companies/invalid-company-guid-xyz/worktemplates`
  * **Verify:** ASP.NET Core route constraint `{companyId:guid}` rejects non-hex format.

* **Excel Logging:** Col L: `Pass` | Col M: `404 / 400` | Col N: `Malformed non-hex company GUID rejected by route constraint.`

---

### `CDWT-DTO-07`: Cross-Company Tenant Boundary Access
* **Scope:** Company Tenant Scoping Guard
* **Expected Result:** `HTTP 400 Cit.Attendance:9001` (Unauthorized company access)

* **Option 1 (Swagger UI Steps):**
  1. Try to access Attendance 3's template ID (`27aa7562-b833-46f7-9cb7-d65f27171dab`) using Attendance 2's companyId in route.
  2. Expand `GET /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/27aa7562-b833-46f7-9cb7-d65f27171dab`.
  3. Click **Execute** -> Verify server rejects with `HTTP 400` or `404`.

* **Option 2 (Postman / Payload Steps):**
  * Target template belonging to Company B under Company A route.
  * **Verify:** Server prevents cross-company data leakage.

* **Excel Logging:** Col L: `Pass` | Col M: `400 / 404` | Col N: `Cross-company entity boundary cleanly enforced.`

---

### `CDWT-DTO-53`: Swagger UI Missing OAuth2 (authorizationCode) Flow
* **Scope:** Swagger OpenAPI Specification
* **Expected Result:** Swagger contains `oauth2` with `WebGateway_Swagger` client (DEFECT-20261029-02)

* **Option 1 (Swagger UI Steps):**
  1. Open Swagger: `https://attendance2.dev.zoolwork.com/swagger/index.html`.
  2. Click **Authorize** button.
  3. Notice: Only `Bearer (http, Bearer)` is shown. There is **NO `oauth2 (OAuth2, authorizationCode)`** button like in Company Service.

* **Option 2 (Swagger JSON Verification Steps):**
  * Open: `https://attendance2.dev.zoolwork.com/swagger/v1/swagger.json`.
  * Search `"securityDefinitions"` or `"securitySchemes"`.
  * Notice: `oauth2` scheme is missing; only `Bearer` is defined.

* **Excel Logging:** Col L: `Failed` | Col M: `401 / Manual Bearer only` | Col N: `DEFECT-20261029-02: Missing oauth2 security scheme; only raw Bearer supported.`

---

## Category 2: Common Top-Level DTO Validations (CDWT-DTO-08 to 18)

### `CDWT-DTO-08`: Empty JSON Payload Body ({}) on POST
* **Scope:** Required Request Body
* **Expected Result:** `HTTP 400 Bad Request`

* **Option 1 (Swagger UI Steps):**
  1. Expand `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`.
  2. Request body: `{}`.
  3. Click **Execute** -> Verify returns `HTTP 400 Bad Request` (Validation errors).

* **Option 2 (Postman Payload):**
  ```json
  {}
  ```

* **Excel Logging:** Col L: `Pass` | Col M: `400` | Col N: `Mandatory field checks reject empty object payload.`

---

### `CDWT-DTO-09`: shortCode Length Below Minimum Boundary (1 Char)
* **Scope:** String Length Validation (min 2 chars)
* **Expected Result:** `HTTP 400 Bad Request`

* **Option 1 (Swagger UI Steps):**
  1. In `POST /worktemplates/fixed`, paste Payload:
  ```json
  {
    "shortCode": "A",
    "templateName": {"en": "Min Code Test"}
  }
  ```
  2. Click **Execute** -> Verify returns `HTTP 400 Bad Request`.

* **Option 2 (Postman Payload):**
  * Same JSON payload with `"shortCode": "A"`.

* **Excel Logging:** Col L: `Pass` | Col M: `400` | Col N: `shortCode below 2 characters rejected.`

---

### `CDWT-DTO-10`: shortCode Contains Special Symbols / Punctuation
* **Scope:** Regex Pattern Validation (`^[a-zA-Z0-9]+$`)
* **Expected Result:** `HTTP 400 Bad Request`

* **Option 1 (Swagger UI Steps):**
  1. In `POST /worktemplates/fixed`, paste Payload:
  ```json
  {
    "shortCode": "CDW@01!",
    "templateName": {"en": "Special Char Test"}
  }
  ```
  2. Click **Execute** -> Verify returns `HTTP 400 Bad Request`.

* **Option 2 (Postman Payload):**
  * Same JSON payload with `"shortCode": "CDW@01!"`.

* **Excel Logging:** Col L: `Pass` | Col M: `400` | Col N: `Special characters in shortCode rejected.`

---

### `CDWT-DTO-11`: shortCode Length at Maximum Boundary (30 Chars)
* **Scope:** Max Boundary Validation (30 chars allowed)
* **Expected Result:** `HTTP 200 OK` (or 400 Cit.Attendance:1010 if CDWT exists)

* **Option 1 (Swagger UI Steps):**
  1. Paste 30-character shortCode:
  ```json
  {
    "shortCode": "COMPDEF00000000000000000000001",
    "templateName": {"en": "Max Boundary 30 Chars"}
  }
  ```
  2. Click **Execute** -> Verify accepted by string length validator.

* **Excel Logging:** Col L: `Pass` | Col M: `200 / 400 (1010)` | Col N: `Valid 30-character boundary accepted.`

---

### `CDWT-DTO-12`: shortCode Omitted or Empty String ("")
* **Scope:** Auto-Generation Feature
* **Expected Result:** `HTTP 200 OK` (Server auto-generates CDWxxxx code)

* **Option 1 (Swagger UI Steps):**
  1. In `POST /worktemplates/fixed`, set `"shortCode": ""` or omit field.
  2. Click **Execute** -> Verify server automatically generates unique shortCode (e.g. `CDW0001`).

* **Excel Logging:** Col L: `Pass` | Col M: `200` | Col N: `Server cleanly auto-generates shortCode when omitted.`

---

### `CDWT-DTO-13`: Attempt to Create Duplicate Company Default
* **Scope:** One-Default Guard per Company
* **Expected Result:** `HTTP 400 Cit.Attendance:1010` (Company default already exists)

* **Option 1 (Swagger UI Steps):**
  1. On `Attendance 2` (which already has active CDWT), send valid Fixed WT payload with shortCode `"FIX999"`.
  2. Click **Execute** -> Verify response returns:
  ```json
  {
    "error": {
      "code": "Cit.Attendance:1010",
      "message": "Company default already exists."
    }
  }
  ```

* **Excel Logging:** Col L: `Pass` | Col M: `400` | Col N: `Enforced by One-Default Guard (Cit.Attendance:1010).`

---

### `CDWT-DTO-14`: templateName Object Omitted or Null
* **Scope:** Mandatory Object Validation
* **Expected Result:** `HTTP 400 Bad Request`

* **Option 1 (Swagger UI Steps):**
  1. Paste Payload:
  ```json
  {
    "shortCode": "FIX003",
    "templateName": null
  }
  ```
  2. Click **Execute** -> Verify returns `HTTP 400` ("Template name is required").

* **Excel Logging:** Col L: `Pass` | Col M: `400` | Col N: `Missing templateName object rejected.`

---

### `CDWT-DTO-15`: templateName.en Empty String ("")
* **Scope:** Multilingual Mandatory English Name
* **Expected Result:** `HTTP 400 Bad Request`

* **Option 1 (Swagger UI Steps):**
  1. Paste Payload:
  ```json
  {
    "shortCode": "FIX004",
    "templateName": {
      "en": ""
    }
  }
  ```
  2. Click **Execute** -> Verify returns `HTTP 400` ("English name cannot be empty").

* **Excel Logging:** Col L: `Pass` | Col M: `400` | Col N: `Empty English name rejected.`

---

### `CDWT-DTO-16`: Bilingual Arabic UTF-8 Name Provided
* **Scope:** Multilingual Persistence
* **Expected Result:** `HTTP 200 OK` (Byte-exact UTF-8 Arabic text stored)

* **Option 1 (Swagger UI Steps):**
  1. Paste Bilingual Payload:
  ```json
  {
    "templateName": {
      "en": "Standard Default",
      "ar": "الجدول الافتراضي للشركة"
    }
  }
  ```
  2. Click **Execute** -> Verify response preserves exact Arabic characters `"الجدول الافتراضي للشركة"`.

* **Excel Logging:** Col L: `Pass` | Col M: `200` | Col N: `Arabic UTF-8 multilingual characters persisted byte-exact.`

---

### `CDWT-DTO-17`: tenantName Exposed in Client Request Body
* **Scope:** Architectural Leaky Abstraction
* **Expected Result:** Field should NOT exist in client DTO; populated strictly by backend (DEFECT-20261026-04)

* **Option 1 (Swagger UI Steps):**
  1. Check Swagger schema for `CreateFixedWorkTemplateDto`.
  2. Notice: `tenantName` is visible in request body.
  3. Send:
  ```json
  {
    "tenantName": {"en": "SpoofedTenantName"}
  }
  ```
  4. In Mongo collection `ERP.Attendance.WorkTemplates`: Document stores empty object `"tenantName": {}`.

* **Excel Logging:** Col L: `Failed` | Col M: `200` | Col N: `DEFECT-20261026-04: tenantName exposed in Swagger and stored as empty object in Mongo.`

---

### `CDWT-DTO-18`: Working Days + Days Off Sum Does NOT Equal 7
* **Scope:** Weekly Calendar Invariant
* **Expected Result:** `HTTP 400 Bad Request` (Actual: HTTP 500 Crash — DEFECT-20261028-02)

* **Option 1 (Swagger UI Steps):**
  1. In `POST /worktemplates/fixed`, paste invalid sum:
  ```json
  {
    "totalWorkingDays": 6,
    "totalDaysOff": 2,
    "totalWorkDurationInMinutes": 2880
  }
  ```
  2. Click **Execute** -> Notice: Server returns **`HTTP 500 ValidationException`** instead of HTTP 400!

* **Excel Logging:** Col L: `Failed` | Col M: `500` | Col N: `DEFECT-20261028-02: Throws unhandled HTTP 500 ValidationException instead of HTTP 400.`

---

## Category 3: Fixed Work Template Validations (CDWT-DTO-19 to 26)

### `CDWT-DTO-19`: Standard 6 Working Days + 1 Day Off Schedule
* **Scope:** Happy Path Fixed CDWT
* **Expected Result:** `HTTP 200 OK`

* **Option 1 (Swagger UI Steps):**
  * Submit full 7 daily slots (Sunday to Friday 08:00–16:00 480m, Saturday Day Off).
  * Verify creates active v1.0 CDWT.

* **Excel Logging:** Col L: `Pass` | Col M: `200` | Col N: `Standard 6 working days schedule verified.`

---

### `CDWT-DTO-20`: dayEnum Invalid Integer Value (e.g. 8 or 0)
* **Scope:** Day Enum Boundary (1=Sunday to 7=Saturday)
* **Expected Result:** `HTTP 400 Bad Request` (Actual: HTTP 500 Crash — DEFECT-20261028-02)

* **Option 1 (Swagger UI Steps):**
  1. In `fixedTimeSlots`, put `"dayEnum": 8`.
  2. Click **Execute** -> Notice: Server throws **`HTTP 500 ValidationException`**.

* **Excel Logging:** Col L: `Failed` | Col M: `500` | Col N: `DEFECT-20261028-02: Out-of-range dayEnum throws HTTP 500 crash.`

---

### `CDWT-DTO-21`: Complete 7-Day Week Sequence (Sun=1 to Sat=7)
* **Scope:** 7-Day Uniqueness Rule
* **Expected Result:** `HTTP 200 OK` (All 7 days defined exactly once)

* **Excel Logging:** Col L: `Pass` | Col M: `200` | Col N: `Full 7-day sequence accepted.`

---

### `CDWT-DTO-22`: Working Day Contradiction (isWorkingDay=false with Duration)
* **Scope:** Logical Contradiction Guard
* **Expected Result:** `HTTP 400 Bad Request`

* **Option 1 (Swagger UI Steps):**
  1. Put `{"dayEnum": 7, "isWorkingDay": false, "workDurationInMinutes": 480}`.
  2. Click **Execute** -> Verify rejected (Day off cannot have duration).

* **Excel Logging:** Col L: `Pass` | Col M: `400` | Col N: `Contradictory duration on off day rejected.`

---

### `CDWT-DTO-23`: Empty Recurrence Array on Active Working Day
* **Scope:** Recurrence Array Boundary
* **Expected Result:** `HTTP 400 Bad Request`

* **Option 1 (Swagger UI Steps):**
  1. Set `{"dayEnum": 1, "isWorkingDay": true, "recurrenceOfMonth": []}`.
  2. Click **Execute** -> Verify rejected (Active day requires >= 1 recurrence).

* **Excel Logging:** Col L: `Pass` | Col M: `400` | Col N: `Empty recurrenceOfMonth rejected.`

---

### `CDWT-DTO-24`: Alternate Saturday Off Pattern Configuration
* **Scope:** Recurrence Variation (1st/3rd/5th Saturday Off, 2nd/4th Active)
* **Expected Result:** `HTTP 200 OK`

* **Excel Logging:** Col L: `Pass` | Col M: `200` | Col N: `Alternate Saturday off recurrence accepted cleanly.`

---

### `CDWT-DTO-25`: Temporal Inversion: startTime >= endTime (No Overnight)
* **Scope:** Time Chronology Validation
* **Expected Result:** `HTTP 400 Bad Request`

* **Option 1 (Swagger UI Steps):**
  1. In a daily slot, put: `"startTime": "17:00", "endTime": "09:00"`.
  2. Click **Execute** -> Verify rejected with `HTTP 400`.

* **Excel Logging:** Col L: `Pass` | Col M: `400` | Col N: `Start time after end time rejected.`

---

### `CDWT-DTO-26`: Total Duration Does Not Match Sum of Active Daily Slots
* **Scope:** Mathematical Invariant
* **Expected Result:** `HTTP 400 Bad Request`

* **Option 1 (Swagger UI Steps):**
  1. Set `"totalWorkDurationInMinutes": 2400`, but sum of 6 slots of 480m is `2880`.
  2. Click **Execute** -> Verify rejected with `HTTP 400`.

* **Excel Logging:** Col L: `Pass` | Col M: `400` | Col N: `Mathematical duration mismatch rejected.`

---

## Category 4: Flexible Work Template Validations (CDWT-DTO-27 to 34)

### `CDWT-DTO-27`: flexibleType Invalid Enum Value (e.g. 9 or 0)
* **Scope:** Flexible Type Enum (1=Daily, 2=Weekly)
* **Expected Result:** `HTTP 400 Bad Request` (Actual: HTTP 500 Crash — DEFECT-20261028-02)

* **Option 1 (Swagger UI Steps):**
  1. Expand `POST /api/companies/{companyId}/worktemplates/flexi`.
  2. Put: `{"flexibleType": 9}`.
  3. Click **Execute** -> Notice: Server throws **`HTTP 500 ValidationException`**.

* **Excel Logging:** Col L: `Failed` | Col M: `500` | Col N: `DEFECT-20261028-02: Invalid flexibleType enum throws HTTP 500 crash.`

---

### `CDWT-DTO-28`: Standard Daily Flexi Mode Configuration
* **Scope:** Happy Path Daily Flexi
* **Expected Result:** `HTTP 200 OK` (FlexibleType=1, Daily=480m)

* **Excel Logging:** Col L: `Pass` | Col M: `200` | Col N: `Standard Daily Flexi mode accepted.`

---

### `CDWT-DTO-29`: Standard Weekly Pool Mode Configuration
* **Scope:** Happy Path Weekly Flexi
* **Expected Result:** `HTTP 200 OK` (FlexibleType=2, Total=2880m, Daily=0m)

* **Excel Logging:** Col L: `Pass` | Col M: `200` | Col N: `Standard Weekly Pool mode accepted.`

---

### `CDWT-DTO-30`: CRITICAL: Daily Duration Exceeding 24 Hours (1500m / 25h)
* **Scope:** 24-Hour Boundary Guard
* **Expected Result:** `HTTP 400 Bad Request` (Actual: HTTP 200 OK — DEFECT-20261028-01)

* **Option 1 (Swagger UI Steps):**
  1. In `POST /worktemplates/flexi`, set `"flexibleType": 1, "workDurationInMinutes": 1500`.
  2. Click **Execute** -> **BUG:** Server returns **`HTTP 200 OK`** and creates a 25-hour day!

* **Option 2 (Postman Payload):**
  ```json
  {
    "flexibleType": 1,
    "workDurationInMinutes": 1500,
    "shortCode": "FLX25H",
    "templateName": {"en": "25 Hours Per Day"}
  }
  ```

* **Excel Logging:** Col L: `Failed` | Col M: `200` | Col N: `DEFECT-20261028-01: Accepted 1500 min (25h/day) with HTTP 200 OK without validation.`

---

### `CDWT-DTO-31`: Weekly Pool Exceeding 168 Hours / Week
* **Scope:** 168-Hour Weekly Boundary (Max 10080 min)
* **Expected Result:** `HTTP 400 Bad Request`

* **Option 1 (Swagger UI Steps):**
  1. In `POST /worktemplates/flexi`, set `"flexibleType": 2, "totalWorkDurationInMinutes": 10500`.
  2. Click **Execute** -> Verify rejected with `HTTP 400`.

* **Excel Logging:** Col L: `Pass` | Col M: `400` | Col N: `Weekly pool exceeding 168 hours rejected.`

---

### `CDWT-DTO-32`: Active Working Day Configured with 0 Hours
* **Scope:** Active Day Zero Duration
* **Expected Result:** `HTTP 400 Bad Request`

* **Option 1 (Swagger UI Steps):**
  1. In `flexiTimeSlots`, set `"isWorkingDay": true, "workDurationInMinutes": 0`.
  2. Click **Execute** -> Verify rejected (Active day must have > 0 minutes).

* **Excel Logging:** Col L: `Pass` | Col M: `400` | Col N: `Zero duration on active day rejected.`

---

### `CDWT-DTO-33`: Negative Work Duration (< 0 Minutes)
* **Scope:** Negative Boundary
* **Expected Result:** `HTTP 400 Bad Request`

* **Option 1 (Swagger UI Steps):**
  1. Set `"workDurationInMinutes": -480`.
  2. Click **Execute** -> Verify rejected with `HTTP 400`.

* **Excel Logging:** Col L: `Pass` | Col M: `400` | Col N: `Negative duration rejected.`

---

### `CDWT-DTO-34`: Weekly Mode with Non-Zero Daily Durations Assigned
* **Scope:** Weekly Mode Contradiction
* **Expected Result:** `HTTP 400 Bad Request`

* **Option 1 (Swagger UI Steps):**
  1. Set `"flexibleType": 2`, but daily slot has `"workDurationInMinutes": 480`.
  2. Click **Execute** -> Verify rejected (Weekly pool requires daily slots = 0).

* **Excel Logging:** Col L: `Pass` | Col M: `400` | Col N: `Non-zero daily duration in weekly mode rejected.`

---

## Category 5: Split Work Template Validations (CDWT-DTO-35 to 40)

### `CDWT-DTO-35`: Standard 2-Interval Split Shift Configuration
* **Scope:** Happy Path Split CDWT
* **Expected Result:** `HTTP 200 OK` (Interval 1: 08:00–12:00, Interval 2: 16:00–20:00, Break: 4h)

* **Excel Logging:** Col L: `Pass` | Col M: `200` | Col N: `Standard 2-interval split shift accepted.`

---

### `CDWT-DTO-36`: Contiguous Intervals / Zero Break Gap
* **Scope:** Split Interval Separation
* **Expected Result:** `HTTP 400 Bad Request` (Actual: HTTP 500 Crash — DEFECT-20261028-02)

* **Option 1 (Swagger UI Steps):**
  1. Expand `POST /api/companies/{companyId}/worktemplates/split`.
  2. Set Slot 1: `08:00–12:00`, Slot 2: `12:00–16:00` (Break Gap = 0).
  3. Click **Execute** -> Notice: Server throws **`HTTP 500 ValidationException`**.

* **Excel Logging:** Col L: `Failed` | Col M: `500` | Col N: `DEFECT-20261028-02: Zero break gap throws HTTP 500 crash.`

---

### `CDWT-DTO-37`: Negative Break Gap Between Intervals
* **Scope:** Chronologic Interval Order
* **Expected Result:** `HTTP 400 Bad Request` (Actual: HTTP 500 Crash — DEFECT-20261028-02)

* **Option 1 (Swagger UI Steps):**
  1. Set Slot 1: `08:00–12:00`, Slot 2: `11:30–15:30`.
  2. Click **Execute** -> Notice: Server throws **`HTTP 500 ValidationException`**.

* **Excel Logging:** Col L: `Failed` | Col M: `500` | Col N: `DEFECT-20261028-02: Negative break gap throws HTTP 500 crash.`

---

### `CDWT-DTO-38`: Overlapping Interval Time Ranges
* **Scope:** Interval Overlap Collision
* **Expected Result:** `HTTP 400 Bad Request` (Actual: HTTP 500 Crash — DEFECT-20261028-02)

* **Option 1 (Swagger UI Steps):**
  1. Set Slot 1: `08:00–13:00`, Slot 2: `12:00–17:00` (Overlap 1 hour).
  2. Click **Execute** -> Notice: Server throws **`HTTP 500 ValidationException`**.

* **Excel Logging:** Col L: `Failed` | Col M: `500` | Col N: `DEFECT-20261028-02: Overlapping intervals throw HTTP 500 crash.`

---

### `CDWT-DTO-39`: Inverted Start/End Timings in a Split Interval
* **Scope:** Time Inversion in Interval
* **Expected Result:** `HTTP 400 Bad Request` (Actual: HTTP 200 OK — DEFECT-20261028-01)

* **Option 1 (Swagger UI Steps):**
  1. Set Slot 1: `"startTime": "12:00", "endTime": "08:00"`.
  2. Click **Execute** -> Notice: Server accepts without error (**`HTTP 200 OK`**)!

* **Excel Logging:** Col L: `Failed` | Col M: `200` | Col N: `DEFECT-20261028-01: Inverted interval timings accepted with HTTP 200 OK.`

---

### `CDWT-DTO-40`: Active Intervals Configured on a Day Off
* **Scope:** Day Off Contradiction
* **Expected Result:** `HTTP 400 Bad Request` (Actual: HTTP 500 Crash — DEFECT-20261028-02)

* **Option 1 (Swagger UI Steps):**
  1. Set `"isWorkingDay": false`, but include active split intervals.
  2. Click **Execute** -> Notice: Server throws **`HTTP 500 ValidationException`**.

* **Excel Logging:** Col L: `Failed` | Col M: `500` | Col N: `DEFECT-20261028-02: Active intervals on off day throw HTTP 500 crash.`

---

## Category 6: PATCH & Immutability Validations (CDWT-DTO-41 to 52)

### `CDWT-DTO-41`: Empty JSON Payload Body ({}) on PATCH
* **Scope:** Required Fields in PATCH
* **Expected Result:** `HTTP 400 Bad Request` (Actual: HTTP 500 Crash — DEFECT-20261028-02)

* **Option 1 (Swagger UI Steps):**
  1. Expand `PATCH /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{id}`.
  2. In Request body, put: `{}`.
  3. Click **Execute** -> Notice: Server throws **`HTTP 500 ValidationException`** ("At least one field is required").

* **Excel Logging:** Col L: `Failed` | Col M: `500` | Col N: `DEFECT-20261028-02: Empty PATCH body throws HTTP 500 crash.`

---

### `CDWT-DTO-42`: Attempt to Mutate shortCode via PATCH
* **Scope:** Immutability Lock
* **Expected Result:** `HTTP 400 Cit.Attendance:1107` (shortCode cannot be changed)

* **Option 1 (Swagger UI Steps):**
  1. On active CDWT, send `PATCH` with body:
  ```json
  {
    "shortCode": "HACKCODE"
  }
  ```
  2. Click **Execute** -> Verify server returns **`HTTP 400 Cit.Attendance:1107`**.

* **Excel Logging:** Col L: `Pass` | Col M: `400` | Col N: `shortCode immutability strictly locked (Cit.Attendance:1107).`

---

### `CDWT-DTO-43`: Attempt to Reassign Entity to Another Company via PATCH
* **Scope:** Tenant & Company Immutability
* **Expected Result:** Ignored or `HTTP 400 Cit.Attendance:9001`

* **Option 1 (Swagger UI Steps):**
  1. Send `PATCH` with `"companyId": "other-company-guid"`.
  2. Click **Execute** -> Verify server ignores or rejects cross-company transfer.

* **Excel Logging:** Col L: `Pass` | Col M: `400 / 200 (ignored)` | Col N: `Cross-company transfer locked.`

---

### `CDWT-DTO-44`: Attempt to Spoof tenantName via PATCH
* **Scope:** Leaky Abstraction in PATCH
* **Expected Result:** Server should reject or ignore client tenantName (DEFECT-20261026-04)

* **Option 1 (Swagger UI Steps):**
  1. Send `PATCH` with `"tenantName": {"en": "SpoofedTenant"}`.
  2. Notice: Server accepts with `HTTP 200 OK`.

* **Excel Logging:** Col L: `Failed` | Col M: `200` | Col N: `DEFECT-20261026-04: tenantName accepted in PATCH body.`

---

### `CDWT-DTO-45`: Attempt to Edit an Archived / Superseded Version ID
* **Scope:** Version Immutability
* **Expected Result:** `HTTP 400 Cit.Attendance:1107` (Cannot edit archived template)

* **Option 1 (Swagger UI Steps):**
  1. In Attendance 4, target archived v1.0 ID: `a31a2f5e-bc53-4221-b2d2-ff8c5ed54dbb`.
  2. Send `PATCH` with `{"templateName": {"en": "Edit Archived"}}`.
  3. Click **Execute** -> Verify returns **`HTTP 400 Cit.Attendance:1107`**.

* **Excel Logging:** Col L: `Pass` | Col M: `400` | Col N: `Archived version protected from edits (Cit.Attendance:1107).`

---

### `CDWT-DTO-46`: Attempt to Edit a Non-Existent Template GUID
* **Scope:** Entity Resolution
* **Expected Result:** `HTTP 400 Cit.Attendance:1101` (Template not found)

* **Option 1 (Swagger UI Steps):**
  1. Send `PATCH` targeting fake GUID: `ffffffff-ffff-ffff-ffff-ffffffffffff`.
  2. Click **Execute** -> Verify returns **`HTTP 400 Cit.Attendance:1101`**.

* **Excel Logging:** Col L: `Pass` | Col M: `400` | Col N: `Non-existent template returns Cit.Attendance:1101.`

---

### `CDWT-DTO-47`: Valid In-Place Timing Shift on Thursday
* **Scope:** Happy Path In-Place Edit (Creates v2.0, Archives v1.0)
* **Expected Result:** `HTTP 200 OK`

* **Option 1 (Swagger UI Steps):**
  1. Send `PATCH` updating Thursday slot from `08:00` to `09:00`.
  2. Click **Execute** -> Verify returns `HTTP 200 OK` (New active version created, old version archived).

* **Excel Logging:** Col L: `Pass` | Col M: `200` | Col N: `In-place edit creates next version and archives previous.`

---

### `CDWT-DTO-48`: Migrate Company Default from Fixed to Flexible Daily
* **Scope:** Type Migration (Fixed -> Flexi)
* **Expected Result:** `HTTP 200 OK` (Creates v2.0 Flexi CDWT)

* **Option 1 (Swagger UI Steps):**
  1. Target active Fixed CDWT with `PATCH /worktemplates/fixed/{id}` passing flexi slots.
  2. Verify returns `HTTP 200 OK` and template type changes to Flexible.

* **Excel Logging:** Col L: `Pass` | Col M: `200` | Col N: `Fixed to Flexi migration accepted.`

---

### `CDWT-DTO-49`: Migrate Company Default from Fixed to Split Shift
* **Scope:** Type Migration (Fixed -> Split)
* **Expected Result:** `HTTP 200 OK` (Creates v2.0 Split CDWT)

* **Option 1 (Swagger UI Steps):**
  1. Target active Fixed CDWT with `PATCH` passing split intervals.
  2. Verify returns `HTTP 200 OK` and template type changes to Split.

* **Excel Logging:** Col L: `Pass` | Col M: `200` | Col N: `Fixed to Split migration accepted.`

---

### `CDWT-DTO-50`: Attempt to Migrate Company Default to Roster / Rotation
* **Scope:** CDWT Allowed Types Guard
* **Expected Result:** `HTTP 400 Bad Request` (CDWT can only be Fixed, Flexi, Split)

* **Option 1 (Swagger UI Steps):**
  1. Send `PATCH` trying to convert CDWT to Roster or Rotation.
  2. Verify rejected (Roster/Rotation restricted to Location Shifts).

* **Excel Logging:** Col L: `Pass` | Col M: `400` | Col N: `CDWT restricted to Fixed, Flexi, Split.`

---

### `CDWT-DTO-51`: Attempt to Archive Active Company Default Work Template
* **Scope:** Active Default Protection Guard
* **Expected Result:** `HTTP 400 Cit.Attendance:1202` (Actual: HTTP 200 OK — DEFECT-20261028-03)

* **Option 1 (Swagger UI Steps):**
  1. Expand `PATCH /api/companies/{companyId}/worktemplates/{activeId}/archive`.
  2. In `activeId`, enter active CDWT ID.
  3. Click **Execute** -> **BUG:** Server returns **`HTTP 200 OK`** without guard, leaving company scheduleless!

* **Excel Logging:** Col L: `Failed` | Col M: `200` | Col N: `DEFECT-20261028-03: Active default archived without guard.`

---

### `CDWT-DTO-52`: Attempt to Soft-Delete Active Company Default Work Template
* **Scope:** Active Default Protection Guard
* **Expected Result:** `HTTP 400 Cit.Attendance:1202` (Actual: HTTP 200 OK — DEFECT-20261028-03)

* **Option 1 (Swagger UI Steps):**
  1. Expand `PATCH /api/companies/{companyId}/worktemplates/{activeId}/delete`.
  2. In `activeId`, enter active CDWT ID.
  3. Click **Execute** -> **BUG:** Server returns **`HTTP 200 OK`** without guard, soft-deleting active default!

* **Excel Logging:** Col L: `Failed` | Col M: `200` | Col N: `DEFECT-20261028-03: Active default soft-deleted without guard.`

---
*Playbook generated and synchronized with `CompanyDefault_DTO_Validation_TestCases.xlsx` and `AttendanceTestCases_Master_Consolidated.xlsx`.*
"""

with open('CDWT_Manual_Testing_Playbook.md', 'w', encoding='utf-8') as f:
    f.write(playbook_content)

print("SUCCESS: Created CDWT_Manual_Testing_Playbook.md with all 53 test cases!")

