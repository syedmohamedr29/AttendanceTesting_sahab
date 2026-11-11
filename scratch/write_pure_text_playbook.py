# -*- coding: utf-8 -*-
"""
Writes CDWT_Manual_Testing_Playbook.md in 100% pure text format (NO TABLES).
Every test case (CDWT-DTO-01 to CDWT-DTO-53) is written out separately with:
 - Option 1: Swagger UI Steps & Exact Input Data
 - Option 2: Postman / Payload Steps & Exact JSON Body
 - Expected HTTP Code & Result
 - Excel Entry (Col L, M, N)
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

content = """# Company Default Work Template (CDWT) — Manual Testing Playbook
## Complete Step-by-Step Test Data Guide for All 53 Edge Cases

Target Microservice: SP.AttendanceSvc (.NET 9 / ASP.NET Core)
Base DEV URL: https://attendance2.dev.zoolwork.com
Auth Server: https://auth8.dev.zoolwork.com/connect/token (tenant: Attendance)
Swagger UI: https://attendance2.dev.zoolwork.com/swagger/index.html
Excel Workbook: CompanyDefault_DTO_Validation_TestCases.xlsx

Target Companies for Testing:
- Company 2 (Attendance 2): 3a247435-3cea-83ae-6a9f-6dda99f386a3 (Fixed CDWT Active v3.0)
- Company 3 (Attendance 3): 3a247435-e31d-ef15-8cc9-62c587f4eb3f (Fixed CDWT Active v2.0)
- Company 4 (Attendance 4): 3a247436-8669-844a-7d2f-1a209af02d8e (Flexi CDWT Active v2.0)
Tenant Header: __tenant: Attendance

================================================================================
CATEGORY 1: ROUTE, HEADERS & SECURITY (CDWT-DTO-01 to CDWT-DTO-07, CDWT-DTO-53)
================================================================================

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-01
Scenario: Missing Authorization Header in Request
Category: 1. Route & Security
Priority: P0 (Blocker / Security)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Open Swagger: https://attendance2.dev.zoolwork.com/swagger/index.html
2. Click the green "Authorize" button at top right -> Click "Logout" (Lock icon is open/unlocked).
3. Scroll down to: POST /api/companies/{companyId}/worktemplates/fixed
4. In companyId, enter: 3a247435-3cea-83ae-6a9f-6dda99f386a3
5. In Request body, enter: {}
6. Click "Execute".

OPTION 2 (Postman / Payload Steps):
- Method: POST
- URL: https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed
- Headers:
    Content-Type: application/json
    __tenant: Attendance
- Authorization: No Auth (leave Authorization header empty)
- Request Body (JSON): {}

EXPECTED RESULT:
- Status Code: HTTP 401 Unauthorized
- Response Header: Www-Authenticate: Bearer

EXCEL LOGGING (Row 2):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 401
- Col N (Actual Notes): Server cleanly blocks unauthenticated request with 401.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-02
Scenario: Expired or Forged Bearer Token
Category: 1. Route & Security
Priority: P0 (Blocker / Security)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. In Swagger, click the green "Authorize" button.
2. In the text box, enter a fake token: 12345
3. Click "Authorize", then click "Close".
4. Scroll to: POST /api/companies/{companyId}/worktemplates/fixed
5. Enter companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3
6. Enter Request body: {}
7. Click "Execute".

OPTION 2 (Postman / Payload Steps):
- Method: POST
- URL: https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed
- Headers:
    Authorization: Bearer invalid_token_99999
    Content-Type: application/json
    __tenant: Attendance
- Request Body (JSON): {}

EXPECTED RESULT:
- Status Code: HTTP 401 Unauthorized
- Response Header: Www-Authenticate: Bearer error="invalid_token"

EXCEL LOGGING (Row 3):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 401
- Col N (Actual Notes): Fake token rejected with 401 error="invalid_token". Note: Expired JWTs in DEV bypass verification (DEFECT-20261029-01).

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-03
Scenario: JWT Token Missing Tenant Claim
Category: 1. Route & Security
Priority: P0 (Blocker / Security)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. In Swagger, Authorize using a token that does not contain the "tenantid" claim.
2. Execute POST /api/companies/{companyId}/worktemplates/fixed.
3. Observe server response.

OPTION 2 (Postman / Payload Steps):
- Pass a Bearer token without tenantid claim.
- Method: POST
- URL: https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed
- Body (JSON): {}

EXPECTED RESULT:
- Status Code: HTTP 401 / 403 Forbidden (SbpAuthorizationException)

EXCEL LOGGING (Row 4):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 401 / 403
- Col N (Actual Notes): Token without tenant claim rejected.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-04
Scenario: Client Tenant Spoofing Attempt via Header
Category: 1. Route & Security
Priority: P1 (Must Work)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. In Swagger, Authorize with your valid token (syed.mohamed@comm-it.in).
2. Expand POST /api/companies/{companyId}/worktemplates/fixed.
3. In the __tenant header box, type: MaliciousSpoofedTenant
4. In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3
5. Click "Execute".

OPTION 2 (Postman / Payload Steps):
- Headers:
    __tenant: MaliciousSpoofedTenant
    Authorization: Bearer <valid-Attendance-token>
    Content-Type: application/json
- Body (JSON): {}

EXPECTED RESULT:
- The server ignores the spoofed header and strictly uses the token claim ("Attendance").

EXCEL LOGGING (Row 5):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 400 / 200
- Col N (Actual Notes): Header spoofing ignored; token claims enforced.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-05
Scenario: Zero GUID companyId in Route Parameter
Category: 1. Route & Security
Priority: P2 (Should Work)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Expand GET /api/companies/{companyId}/worktemplates
2. In companyId, enter: 00000000-0000-0000-0000-000000000000
3. Click "Execute".

OPTION 2 (Postman / Payload Steps):
- Method: GET
- URL: https://attendance2.dev.zoolwork.com/api/companies/00000000-0000-0000-0000-000000000000/worktemplates
- Headers:
    Authorization: Bearer <token>
    __tenant: Attendance

EXPECTED RESULT:
- Expected: HTTP 404 Company Not Found
- Actual Live Server Bug: Returns HTTP 200 OK with [] (DEFECT-20261028-04)

EXCEL LOGGING (Row 6):
- Col L (Manual Status): Failed
- Col M (Actual HTTP Code): 200
- Col N (Actual Notes): DEFECT-20261028-04: Returns HTTP 200 [] instead of 404 Company Not Found.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-06
Scenario: Malformed Non-Hex companyId in Route
Category: 1. Route & Security
Priority: P1 (Must Work)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Expand GET /api/companies/{companyId}/worktemplates
2. In companyId, enter: invalid-company-guid-xyz
3. Click "Execute".

OPTION 2 (Postman / Payload Steps):
- Method: GET
- URL: https://attendance2.dev.zoolwork.com/api/companies/invalid-company-guid-xyz/worktemplates

EXPECTED RESULT:
- Status Code: HTTP 404 Not Found or HTTP 400 Bad Request (Route constraint rejected non-hex string)

EXCEL LOGGING (Row 7):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 404 / 400
- Col N (Actual Notes): Non-hex company GUID rejected by route constraint.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-07
Scenario: Cross-Company Tenant Boundary Access
Category: 1. Route & Security
Priority: P0 (Blocker / Security)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. In route, enter Company 2: 3a247435-3cea-83ae-6a9f-6dda99f386a3
2. In template ID, enter Company 3's template ID: 27aa7562-b833-46f7-9cb7-d65f27171dab
3. Execute GET /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/27aa7562-b833-46f7-9cb7-d65f27171dab

OPTION 2 (Postman / Payload Steps):
- Target Company 2's route with Company 3's template GUID.

EXPECTED RESULT:
- Status Code: HTTP 400 Cit.Attendance:9001 (Cross-company access blocked)

EXCEL LOGGING (Row 8):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 400
- Col N (Actual Notes): Cross-company boundary cleanly enforced.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-53
Scenario: Swagger UI Missing OAuth2 (authorizationCode) Flow
Category: 1. Route & Security
Priority: P1 (High Architecture / DX)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Open Swagger: https://attendance2.dev.zoolwork.com/swagger/index.html
2. Click the green "Authorize" button.
3. Observe: Only raw text "Bearer (http, Bearer)" is available.
   There is NO "oauth2 (OAuth2, authorizationCode)" button like in Company Service.

OPTION 2 (Swagger JSON Verification Steps):
- Open in browser: https://attendance2.dev.zoolwork.com/swagger/v1/swagger.json
- Search for "securitySchemes"
- Observe: oauth2 security scheme is missing; only Bearer is defined.

EXPECTED RESULT:
- Expected: Swagger UI should configure oauth2 authorizationCode flow with WebGateway_Swagger client.
- Actual Status: Missing OAuth2 scheme (DEFECT-20261029-02)

EXCEL LOGGING (Row 54):
- Col L (Manual Status): Failed
- Col M (Actual HTTP Code): 401 / Manual Bearer only
- Col N (Actual Notes): DEFECT-20261029-02: Missing Swagger OAuth2 authorizationCode scheme.

================================================================================
CATEGORY 2: COMMON TOP-LEVEL DTO VALIDATIONS (CDWT-DTO-08 to CDWT-DTO-18)
================================================================================

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-08
Scenario: Empty JSON Payload Body ({}) on POST
Category: 2. Common DTO
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed
2. In Request body, enter: {}
3. Click "Execute".

OPTION 2 (Postman / Payload Steps):
- Method: POST
- URL: https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed
- Body (JSON): {}

EXPECTED RESULT:
- Status Code: HTTP 400 Bad Request (Mandatory fields missing)

EXCEL LOGGING (Row 9):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 400
- Col N (Actual Notes): Empty payload cleanly rejected on POST.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-09
Scenario: shortCode Length Below Minimum Boundary (1 Char)
Category: 2. Common DTO
Priority: P1 (Must Work)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. In POST /worktemplates/fixed, paste Request body:
{
  "shortCode": "A",
  "templateName": {"en": "Min Code Test"}
}
2. Click "Execute".

OPTION 2 (Postman Payload):
{
  "shortCode": "A",
  "templateName": {"en": "Min Code Test"}
}

EXPECTED RESULT:
- Status Code: HTTP 400 Bad Request ("shortCode length must be >= 2")

EXCEL LOGGING (Row 10):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 400
- Col N (Actual Notes): shortCode < 2 characters rejected.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-10
Scenario: shortCode Contains Special Characters / Symbols
Category: 2. Common DTO
Priority: P1 (Must Work)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. In POST /worktemplates/fixed, paste Request body:
{
  "shortCode": "CDW@01!",
  "templateName": {"en": "Special Char Test"}
}
2. Click "Execute".

OPTION 2 (Postman Payload):
{
  "shortCode": "CDW@01!",
  "templateName": {"en": "Special Char Test"}
}

EXPECTED RESULT:
- Status Code: HTTP 400 Bad Request ("Only alphanumeric characters allowed")

EXCEL LOGGING (Row 11):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 400
- Col N (Actual Notes): Special characters in shortCode rejected.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-11
Scenario: shortCode Length at Maximum Boundary (30 Chars)
Category: 2. Common DTO
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. In POST /worktemplates/fixed, paste 30-character shortCode:
{
  "shortCode": "COMPDEF00000000000000000000001",
  "templateName": {"en": "Max Boundary Test"}
}
2. Click "Execute".

OPTION 2 (Postman Payload):
{
  "shortCode": "COMPDEF00000000000000000000001",
  "templateName": {"en": "Max Boundary Test"}
}

EXPECTED RESULT:
- Status Code: HTTP 200 OK (or HTTP 400 Cit.Attendance:1010 if company already has default)
- String length validator accepts exact 30 characters.

EXCEL LOGGING (Row 12):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 200 / 400 (1010)
- Col N (Actual Notes): 30-character max boundary accepted.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-12
Scenario: shortCode Omitted or Empty String ("")
Category: 2. Common DTO
Priority: P1 (Must Work)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. In POST /worktemplates/fixed, enter:
{
  "shortCode": "",
  "templateName": {"en": "Auto Code Test"}
}
2. Click "Execute".

OPTION 2 (Postman Payload):
{
  "shortCode": "",
  "templateName": {"en": "Auto Code Test"}
}

EXPECTED RESULT:
- Server automatically generates unique code CDWxxxx.

EXCEL LOGGING (Row 13):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 200
- Col N (Actual Notes): Server cleanly auto-generates shortCode.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-13
Scenario: Attempt to Create Duplicate Company Default
Category: 2. Common DTO
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. On Company 2 (3a247435-3cea-83ae-6a9f-6dda99f386a3), submit valid Fixed WT with shortCode "FIX999".
2. Click "Execute".

OPTION 2 (Postman Payload):
Submit standard valid Fixed WT on a company that already has an active default.

EXPECTED RESULT:
- Status Code: HTTP 400 Cit.Attendance:1010 ("Company default already exists.")

EXCEL LOGGING (Row 14):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 400
- Col N (Actual Notes): One-Default Guard enforced (Cit.Attendance:1010).

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-14
Scenario: templateName Object Omitted or Null
Category: 2. Common DTO
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. In POST /worktemplates/fixed, paste:
{
  "shortCode": "FIX003",
  "templateName": null
}
2. Click "Execute".

OPTION 2 (Postman Payload):
{
  "shortCode": "FIX003",
  "templateName": null
}

EXPECTED RESULT:
- Status Code: HTTP 400 Bad Request ("Template name is required")

EXCEL LOGGING (Row 15):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 400
- Col N (Actual Notes): Missing templateName rejected.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-15
Scenario: templateName.en Empty String ("")
Category: 2. Common DTO
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. In POST /worktemplates/fixed, paste:
{
  "shortCode": "FIX004",
  "templateName": {
    "en": ""
  }
}
2. Click "Execute".

OPTION 2 (Postman Payload):
{
  "shortCode": "FIX004",
  "templateName": {
    "en": ""
  }
}

EXPECTED RESULT:
- Status Code: HTTP 400 Bad Request ("English name cannot be empty")

EXCEL LOGGING (Row 16):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 400
- Col N (Actual Notes): Empty English name rejected.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-16
Scenario: Bilingual Arabic UTF-8 Name Provided
Category: 2. Common DTO
Priority: P1 (Must Work)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. In POST /worktemplates/fixed, paste:
{
  "templateName": {
    "en": "Standard Default",
    "ar": "الجدول الافتراضي للشركة"
  }
}
2. Click "Execute".

OPTION 2 (Postman Payload):
{
  "templateName": {
    "en": "Standard Default",
    "ar": "الجدول الافتراضي للشركة"
  }
}

EXPECTED RESULT:
- Status Code: HTTP 200 OK (Arabic text preserved byte-exact in database)

EXCEL LOGGING (Row 17):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 200
- Col N (Actual Notes): Arabic UTF-8 text persisted byte-exact.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-17
Scenario: tenantName Exposed in Client Request Body
Category: 2. Common DTO
Priority: P2 (Design Gap)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. In POST /worktemplates/fixed, enter:
{
  "tenantName": {"en": "SpoofedTenantName"}
}
2. Click "Execute".
3. Check MongoDB: Document persists empty object "tenantName": {}.

OPTION 2 (Postman Payload):
Pass tenantName object in request body.

EXPECTED RESULT:
- Architectural gap: Client should NOT send tenantName; backend should populate it.
- Actual Status: DEFECT-20261026-04

EXCEL LOGGING (Row 18):
- Col L (Manual Status): Failed
- Col M (Actual HTTP Code): 200
- Col N (Actual Notes): DEFECT-20261026-04: tenantName exposed in Swagger and stored as empty object in Mongo.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-18
Scenario: Working Days + Days Off Sum Does NOT Equal 7
Category: 2. Common DTO
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. In POST /worktemplates/fixed, paste:
{
  "totalWorkingDays": 6,
  "totalDaysOff": 2,
  "totalWorkDurationInMinutes": 2880
}
2. Click "Execute".

OPTION 2 (Postman Payload):
{
  "totalWorkingDays": 6,
  "totalDaysOff": 2,
  "totalWorkDurationInMinutes": 2880
}

EXPECTED RESULT:
- Expected: HTTP 400 Bad Request ("Sum must equal 7")
- Actual Live Server Bug: Throws unhandled HTTP 500 ValidationException (DEFECT-20261028-02)

EXCEL LOGGING (Row 19):
- Col L (Manual Status): Failed
- Col M (Actual HTTP Code): 500
- Col N (Actual Notes): DEFECT-20261028-02: Throws HTTP 500 ValidationException instead of HTTP 400.

================================================================================
CATEGORY 3: FIXED WORK TEMPLATE VALIDATIONS (CDWT-DTO-19 to CDWT-DTO-26)
================================================================================

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-19
Scenario: Standard 6 Working Days + 1 Day Off Schedule
Category: 3. Fixed WT
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. In POST /worktemplates/fixed, submit full 7 daily slots (Sunday to Friday 08:00–16:00 480m, Saturday Day Off).
2. Click "Execute".

OPTION 2 (Postman Payload):
Submit standard valid 7-day Fixed schedule JSON.

EXPECTED RESULT:
- Status Code: HTTP 200 OK (Creates active v1.0 CDWT)

EXCEL LOGGING (Row 20):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 200
- Col N (Actual Notes): Standard 6-day Fixed schedule accepted.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-20
Scenario: dayEnum Invalid Integer Value (e.g. 8 or 0)
Category: 3. Fixed WT
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. In fixedTimeSlots, set "dayEnum": 8:
{
  "fixedTimeSlots": [
    {"dayEnum": 8, "isWorkingDay": true, "startTime": "08:00", "endTime": "16:00"}
  ]
}
2. Click "Execute".

OPTION 2 (Postman Payload):
Same JSON body with "dayEnum": 8.

EXPECTED RESULT:
- Expected: HTTP 400 Bad Request ("dayEnum must be between 1 and 7")
- Actual Live Server Bug: Throws HTTP 500 ValidationException (DEFECT-20261028-02)

EXCEL LOGGING (Row 21):
- Col L (Manual Status): Failed
- Col M (Actual HTTP Code): 500
- Col N (Actual Notes): DEFECT-20261028-02: Out-of-range dayEnum throws HTTP 500 crash.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-21
Scenario: Complete 7-Day Week Sequence (Sun=1 to Sat=7)
Category: 3. Fixed WT
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Include all 7 days with dayEnum 1 to 7 without skipping or repeating any day.
2. Click "Execute".

OPTION 2 (Postman Payload):
7 daily slot items covering Sunday(1) to Saturday(7).

EXPECTED RESULT:
- Status Code: HTTP 200 OK

EXCEL LOGGING (Row 22):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 200
- Col N (Actual Notes): Full 7-day week sequence verified.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-22
Scenario: Working Day Contradiction (isWorkingDay=false with Duration)
Category: 3. Fixed WT
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Set:
{
  "dayEnum": 7,
  "isWorkingDay": false,
  "workDurationInMinutes": 480
}
2. Click "Execute".

OPTION 2 (Postman Payload):
Contradictory slot: isWorkingDay=false with 480m duration.

EXPECTED RESULT:
- Status Code: HTTP 400 Bad Request ("Off day cannot have working duration")

EXCEL LOGGING (Row 23):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 400
- Col N (Actual Notes): Contradictory duration on day off rejected.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-23
Scenario: Empty Recurrence Array on Active Working Day
Category: 3. Fixed WT
Priority: P1 (Must Work)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Set:
{
  "dayEnum": 1,
  "isWorkingDay": true,
  "recurrenceOfMonth": []
}
2. Click "Execute".

OPTION 2 (Postman Payload):
Slot with "recurrenceOfMonth": [] on active day.

EXPECTED RESULT:
- Status Code: HTTP 400 Bad Request ("Active day requires at least one recurrence")

EXCEL LOGGING (Row 24):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 400
- Col N (Actual Notes): Empty recurrenceOfMonth rejected.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-24
Scenario: Alternate Saturday Off Pattern Configuration
Category: 3. Fixed WT
Priority: P1 (Must Work)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Friday [1, 2, 3, 4, 5] = Off.
2. Saturday [1, 3, 5] = Off.
3. Saturday [2, 4] = Active (480m).
4. Click "Execute".

OPTION 2 (Postman Payload):
Multi-recurrence pattern payload for alternate weekends.

EXPECTED RESULT:
- Status Code: HTTP 200 OK

EXCEL LOGGING (Row 25):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 200
- Col N (Actual Notes): Alternate Saturday off recurrence accepted cleanly.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-25
Scenario: Start >= End Time Inversion (No Overnight)
Category: 3. Fixed WT
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. In a daily slot:
{
  "startTime": "17:00",
  "endTime": "09:00",
  "workDurationInMinutes": 480
}
2. Click "Execute".

OPTION 2 (Postman Payload):
Slot timings where startTime > endTime.

EXPECTED RESULT:
- Status Code: HTTP 400 Bad Request ("End time must be greater than start time")

EXCEL LOGGING (Row 26):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 400
- Col N (Actual Notes): Inverted start/end time rejected.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-26
Scenario: Total Duration Does Not Match Sum of Active Daily Slots
Category: 3. Fixed WT
Priority: P1 (Must Work)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Set "totalWorkDurationInMinutes": 2400, but sum of daily slots is 2880.
2. Click "Execute".

OPTION 2 (Postman Payload):
Payload with mismatch between total minutes and daily minutes sum.

EXPECTED RESULT:
- Status Code: HTTP 400 Bad Request ("Total duration must match sum of active daily slots")

EXCEL LOGGING (Row 27):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 400
- Col N (Actual Notes): Mathematical mismatch rejected.

================================================================================
CATEGORY 4: FLEXIBLE WORK TEMPLATE VALIDATIONS (CDWT-DTO-27 to CDWT-DTO-34)
================================================================================

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-27
Scenario: flexibleType Invalid Enum Value (e.g. 9 or 0)
Category: 4. Flexible WT
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/flexi
2. In body: {"flexibleType": 9}
3. Click "Execute".

OPTION 2 (Postman Payload):
{
  "flexibleType": 9,
  "totalWorkDurationInMinutes": 2400
}

EXPECTED RESULT:
- Expected: HTTP 400 Bad Request ("flexibleType must be 1 (Daily) or 2 (Weekly)")
- Actual Live Server Bug: Throws HTTP 500 ValidationException (DEFECT-20261028-02)

EXCEL LOGGING (Row 28):
- Col L (Manual Status): Failed
- Col M (Actual HTTP Code): 500
- Col N (Actual Notes): DEFECT-20261028-02: Invalid flexibleType enum throws HTTP 500 crash.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-28
Scenario: Standard Daily Flexi Mode Configuration
Category: 4. Flexible WT
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Set "flexibleType": 1, "workDurationInMinutes": 480, "totalWorkingDays": 5
2. Click "Execute".

OPTION 2 (Postman Payload):
Standard valid Daily Flexi JSON body.

EXPECTED RESULT:
- Status Code: HTTP 200 OK (Creates active v1.0 Daily Flexi CDWT)

EXCEL LOGGING (Row 29):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 200
- Col N (Actual Notes): Standard Daily Flexi accepted.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-29
Scenario: Standard Weekly Pool Mode Configuration
Category: 4. Flexible WT
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Set "flexibleType": 2, "totalWorkDurationInMinutes": 2880, "dailyWorkDurationInMinutes": 0
2. Click "Execute".

OPTION 2 (Postman Payload):
Standard valid Weekly Pool Flexi JSON body.

EXPECTED RESULT:
- Status Code: HTTP 200 OK (Creates active v1.0 Weekly Flexi CDWT)

EXCEL LOGGING (Row 30):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 200
- Col N (Actual Notes): Standard Weekly Pool accepted.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-30
Scenario: CRITICAL: Daily Duration Exceeding 24 Hours (1500m / 25h)
Category: 4. Flexible WT
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. In POST /worktemplates/flexi, set:
{
  "flexibleType": 1,
  "workDurationInMinutes": 1500,
  "shortCode": "FLX25H",
  "templateName": {"en": "25 Hours Daily"}
}
2. Click "Execute".

OPTION 2 (Postman Payload):
Same JSON body with workDurationInMinutes: 1500.

EXPECTED RESULT:
- Expected: HTTP 400 Bad Request ("Daily duration cannot exceed 1440 minutes / 24 hours")
- Actual Live Server Bug: Server returns HTTP 200 OK and creates a 25-hour day (DEFECT-20261028-01)

EXCEL LOGGING (Row 31):
- Col L (Manual Status): Failed
- Col M (Actual HTTP Code): 200
- Col N (Actual Notes): DEFECT-20261028-01: Accepted 1500 min (25h/day) with HTTP 200 OK without validation.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-31
Scenario: Weekly Pool Exceeding 168 Hours / Week
Category: 4. Flexible WT
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. In POST /worktemplates/flexi, set:
{
  "flexibleType": 2,
  "totalWorkDurationInMinutes": 10500
}
2. Click "Execute".

OPTION 2 (Postman Payload):
Same JSON body with 10500 minutes (175 hours).

EXPECTED RESULT:
- Status Code: HTTP 400 Bad Request ("Weekly pool cannot exceed 10080 minutes / 168 hours")

EXCEL LOGGING (Row 32):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 400
- Col N (Actual Notes): Weekly pool > 168 hours cleanly rejected.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-32
Scenario: Active Working Day Configured with 0 Hours
Category: 4. Flexible WT
Priority: P1 (Must Work)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. In flexiTimeSlots: {"isWorkingDay": true, "workDurationInMinutes": 0}
2. Click "Execute".

OPTION 2 (Postman Payload):
Active day with 0 minutes.

EXPECTED RESULT:
- Status Code: HTTP 400 Bad Request ("Active working day must have > 0 duration")

EXCEL LOGGING (Row 33):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 400
- Col N (Actual Notes): 0 hours on active day rejected.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-33
Scenario: Negative Work Duration (< 0 Minutes)
Category: 4. Flexible WT
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Set "workDurationInMinutes": -480
2. Click "Execute".

OPTION 2 (Postman Payload):
JSON body with negative duration.

EXPECTED RESULT:
- Status Code: HTTP 400 Bad Request ("Duration must be greater than 0")

EXCEL LOGGING (Row 34):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 400
- Col N (Actual Notes): Negative duration rejected.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-34
Scenario: Weekly Mode with Non-Zero Daily Durations
Category: 4. Flexible WT
Priority: P1 (Must Work)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Set "flexibleType": 2, but include daily slot with "workDurationInMinutes": 480
2. Click "Execute".

OPTION 2 (Postman Payload):
Weekly pool containing non-zero daily durations.

EXPECTED RESULT:
- Status Code: HTTP 400 Bad Request ("Weekly pool requires daily duration = 0")

EXCEL LOGGING (Row 35):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 400
- Col N (Actual Notes): Weekly mode contradiction rejected.

================================================================================
CATEGORY 5: SPLIT WORK TEMPLATE VALIDATIONS (CDWT-DTO-35 to CDWT-DTO-40)
================================================================================

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-35
Scenario: Standard 2-Interval Split Shift Configuration
Category: 5. Split WT
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/split
2. Slot 1: 08:00–12:00 (4h), Slot 2: 16:00–20:00 (4h), Break: 4h.
3. Click "Execute".

OPTION 2 (Postman Payload):
Standard valid 2-interval Split shift JSON.

EXPECTED RESULT:
- Status Code: HTTP 200 OK (Creates active v1.0 Split CDWT)

EXCEL LOGGING (Row 36):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 200
- Col N (Actual Notes): Standard 2-interval Split shift accepted.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-36
Scenario: Contiguous Intervals / Zero Break Gap
Category: 5. Split WT
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. In POST /worktemplates/split, set Slot 1: 08:00–12:00 and Slot 2: 12:00–16:00 (Break = 0 min).
2. Click "Execute".

OPTION 2 (Postman Payload):
Split shift where Interval 2 starts at exact minute Interval 1 ends.

EXPECTED RESULT:
- Expected: HTTP 400 Bad Request ("Split intervals must have a break gap")
- Actual Live Server Bug: Throws HTTP 500 ValidationException (DEFECT-20261028-02)

EXCEL LOGGING (Row 37):
- Col L (Manual Status): Failed
- Col M (Actual HTTP Code): 500
- Col N (Actual Notes): DEFECT-20261028-02: Zero break gap throws HTTP 500 crash.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-37
Scenario: Negative Break Gap Between Intervals
Category: 5. Split WT
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Set Slot 1: 08:00–12:00 and Slot 2: 11:30–15:30.
2. Click "Execute".

OPTION 2 (Postman Payload):
Interval 2 starts 30 minutes before Interval 1 ends.

EXPECTED RESULT:
- Expected: HTTP 400 Bad Request
- Actual Live Server Bug: Throws HTTP 500 ValidationException (DEFECT-20261028-02)

EXCEL LOGGING (Row 38):
- Col L (Manual Status): Failed
- Col M (Actual HTTP Code): 500
- Col N (Actual Notes): DEFECT-20261028-02: Negative break gap throws HTTP 500 crash.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-38
Scenario: Overlapping Interval Time Ranges
Category: 5. Split WT
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Set Slot 1: 08:00–13:00 and Slot 2: 12:00–17:00 (1h overlap).
2. Click "Execute".

OPTION 2 (Postman Payload):
Overlapping intervals in the same daily split slot.

EXPECTED RESULT:
- Expected: HTTP 400 Bad Request ("Split intervals cannot overlap")
- Actual Live Server Bug: Throws HTTP 500 ValidationException (DEFECT-20261028-02)

EXCEL LOGGING (Row 39):
- Col L (Manual Status): Failed
- Col M (Actual HTTP Code): 500
- Col N (Actual Notes): DEFECT-20261028-02: Overlapping intervals throw HTTP 500 crash.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-39
Scenario: Inverted Start/End Timings in a Split Interval
Category: 5. Split WT
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. In Slot 1: "startTime": "12:00", "endTime": "08:00".
2. Click "Execute".

OPTION 2 (Postman Payload):
Split interval where startTime > endTime.

EXPECTED RESULT:
- Expected: HTTP 400 Bad Request
- Actual Live Server Bug: Server accepts with HTTP 200 OK (DEFECT-20261028-01)

EXCEL LOGGING (Row 40):
- Col L (Manual Status): Failed
- Col M (Actual HTTP Code): 200
- Col N (Actual Notes): DEFECT-20261028-01: Inverted interval timings accepted with HTTP 200 OK.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-40
Scenario: Active Intervals Configured on a Day Off
Category: 5. Split WT
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Set "isWorkingDay": false, but include active split intervals.
2. Click "Execute".

OPTION 2 (Postman Payload):
Off-day with active split intervals.

EXPECTED RESULT:
- Expected: HTTP 400 Bad Request
- Actual Live Server Bug: Throws HTTP 500 ValidationException (DEFECT-20261028-02)

EXCEL LOGGING (Row 41):
- Col L (Manual Status): Failed
- Col M (Actual HTTP Code): 500
- Col N (Actual Notes): DEFECT-20261028-02: Active intervals on day off throw HTTP 500 crash.

================================================================================
CATEGORY 6: PATCH & IMMUTABILITY VALIDATIONS (CDWT-DTO-41 to CDWT-DTO-52)
================================================================================

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-41
Scenario: Empty JSON Payload Body ({}) on PATCH
Category: 6. PATCH & Immutability
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Expand PATCH /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{id}
2. In Request body, enter: {}
3. Click "Execute".

OPTION 2 (Postman Payload):
PATCH request with raw JSON body {}.

EXPECTED RESULT:
- Expected: HTTP 400 Bad Request ("At least one update field is required")
- Actual Live Server Bug: Throws HTTP 500 ValidationException (DEFECT-20261028-02)

EXCEL LOGGING (Row 42):
- Col L (Manual Status): Failed
- Col M (Actual HTTP Code): 500
- Col N (Actual Notes): DEFECT-20261028-02: Empty PATCH body throws HTTP 500 crash.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-42
Scenario: Attempt to Mutate shortCode via PATCH
Category: 6. PATCH & Immutability
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Send PATCH on active CDWT with body: {"shortCode": "HACKCODE"}
2. Click "Execute".

OPTION 2 (Postman Payload):
PATCH with {"shortCode": "HACKCODE"}.

EXPECTED RESULT:
- Status Code: HTTP 400 with code Cit.Attendance:1107 (shortCode is immutable after create)

EXCEL LOGGING (Row 43):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 400
- Col N (Actual Notes): shortCode immutability strictly locked (Cit.Attendance:1107).

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-43
Scenario: Attempt to Reassign Entity to Another Company via PATCH
Category: 6. PATCH & Immutability
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Send PATCH with body: {"companyId": "3a247435-e31d-ef15-8cc9-62c587f4eb3f"}
2. Click "Execute".

OPTION 2 (Postman Payload):
PATCH trying to reassign company ownership.

EXPECTED RESULT:
- Server ignores cross-company reassignment or returns HTTP 400.

EXCEL LOGGING (Row 44):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 400 / 200 (ignored)
- Col N (Actual Notes): Cross-company transfer locked.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-44
Scenario: Attempt to Spoof tenantName via PATCH
Category: 6. PATCH & Immutability
Priority: P2 (Design Gap)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Send PATCH with body: {"tenantName": {"en": "SpoofedTenant"}}
2. Click "Execute".

OPTION 2 (Postman Payload):
PATCH containing tenantName.

EXPECTED RESULT:
- Server should ignore or reject client tenantName.
- Actual: DEFECT-20261026-04

EXCEL LOGGING (Row 45):
- Col L (Manual Status): Failed
- Col M (Actual HTTP Code): 200
- Col N (Actual Notes): DEFECT-20261026-04: tenantName accepted in PATCH body.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-45
Scenario: Attempt to Edit an Archived / Superseded Version ID
Category: 6. PATCH & Immutability
Priority: P1 (Must Work)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. In Company 4, target archived v1.0 ID: a31a2f5e-bc53-4221-b2d2-ff8c5ed54dbb
2. Send PATCH with {"templateName": {"en": "Edit Archived"}}
3. Click "Execute".

OPTION 2 (Postman Payload):
PATCH targeting archived template GUID.

EXPECTED RESULT:
- Status Code: HTTP 400 with code Cit.Attendance:1107 ("Archived template cannot be edited")

EXCEL LOGGING (Row 46):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 400
- Col N (Actual Notes): Archived versions protected from edits (Cit.Attendance:1107).

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-46
Scenario: Attempt to Edit a Non-Existent Template GUID
Category: 6. PATCH & Immutability
Priority: P1 (Must Work)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Send PATCH targeting fake GUID: ffffffff-ffff-ffff-ffff-ffffffffffff
2. Click "Execute".

OPTION 2 (Postman Payload):
PATCH targeting non-existent GUID.

EXPECTED RESULT:
- Status Code: HTTP 400 with code Cit.Attendance:1101 ("Template not found")

EXCEL LOGGING (Row 47):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 400
- Col N (Actual Notes): Non-existent template returns Cit.Attendance:1101.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-47
Scenario: Valid In-Place Timing Shift on Thursday
Category: 6. PATCH & Immutability
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Send PATCH on active CDWT updating Thursday slot from 08:00 to 09:00.
2. Click "Execute".

OPTION 2 (Postman Payload):
In-place slot update payload.

EXPECTED RESULT:
- Status Code: HTTP 200 OK (Creates active v2.0, archives v1.0)

EXCEL LOGGING (Row 48):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 200
- Col N (Actual Notes): In-place edit creates next version and archives previous.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-48
Scenario: Migrate Company Default from Fixed to Flexible Daily
Category: 6. PATCH & Immutability
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. On active Fixed CDWT, call PATCH /worktemplates/fixed/{id} passing flexi slots payload.
2. Click "Execute".

OPTION 2 (Postman Payload):
Type migration payload from Fixed to Flexible.

EXPECTED RESULT:
- Status Code: HTTP 200 OK (Creates active v2.0 Flexi CDWT)

EXCEL LOGGING (Row 49):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 200
- Col N (Actual Notes): Fixed to Flexi migration accepted.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-49
Scenario: Migrate Company Default from Fixed to Split Shift
Category: 6. PATCH & Immutability
Priority: P0 (Blocker)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. On active Fixed CDWT, call PATCH /worktemplates/fixed/{id} passing split intervals payload.
2. Click "Execute".

OPTION 2 (Postman Payload):
Type migration payload from Fixed to Split.

EXPECTED RESULT:
- Status Code: HTTP 200 OK (Creates active v2.0 Split CDWT)

EXCEL LOGGING (Row 50):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 200
- Col N (Actual Notes): Fixed to Split migration accepted.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-50
Scenario: Attempt to Migrate Company Default to Roster / Rotation
Category: 6. PATCH & Immutability
Priority: P1 (Must Work)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Call PATCH attempting to pass Roster or Rotation schedule to CDWT.
2. Click "Execute".

OPTION 2 (Postman Payload):
Migration payload trying to assign Roster/Rotation to CDWT.

EXPECTED RESULT:
- Status Code: HTTP 400 Bad Request (CDWT is restricted to Fixed, Flexi, Split)

EXCEL LOGGING (Row 51):
- Col L (Manual Status): Pass
- Col M (Actual HTTP Code): 400
- Col N (Actual Notes): CDWT restricted to Fixed, Flexi, Split.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-51
Scenario: Attempt to Archive Active Company Default Work Template
Category: 6. PATCH & Immutability
Priority: P1 (Must Work)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Expand PATCH /api/companies/{companyId}/worktemplates/{activeId}/archive
2. In activeId, enter active CDWT ID.
3. Click "Execute".

OPTION 2 (Postman Payload):
PATCH on /archive route targeting active CDWT.

EXPECTED RESULT:
- Expected: HTTP 400 Cit.Attendance:1202 (Active default must be protected)
- Actual Live Server Bug: Server returns HTTP 200 OK without guard (DEFECT-20261028-03)

EXCEL LOGGING (Row 52):
- Col L (Manual Status): Failed
- Col M (Actual HTTP Code): 200
- Col N (Actual Notes): DEFECT-20261028-03: Active default archived without guard.

--------------------------------------------------------------------------------
TEST CASE: CDWT-DTO-52
Scenario: Attempt to Soft-Delete Active Company Default Work Template
Category: 6. PATCH & Immutability
Priority: P1 (Must Work)
--------------------------------------------------------------------------------
OPTION 1 (Swagger UI Steps):
1. Expand PATCH /api/companies/{companyId}/worktemplates/{activeId}/delete
2. In activeId, enter active CDWT ID.
3. Click "Execute".

OPTION 2 (Postman Payload):
PATCH on /delete route targeting active CDWT.

EXPECTED RESULT:
- Expected: HTTP 400 Cit.Attendance:1202 (Active default must be protected)
- Actual Live Server Bug: Server returns HTTP 200 OK without guard (DEFECT-20261028-03)

EXCEL LOGGING (Row 53):
- Col L (Manual Status): Failed
- Col M (Actual HTTP Code): 200
- Col N (Actual Notes): DEFECT-20261028-03: Active default soft-deleted without guard.

================================================================================
END OF PLAYBOOK — ALL 53 TEST CASES PREPARED
================================================================================
"""

with open('CDWT_Manual_Testing_Playbook.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Written CDWT_Manual_Testing_Playbook.md in 100% pure text format (NO TABLES)!")

