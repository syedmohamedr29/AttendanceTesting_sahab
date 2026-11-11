# -*- coding: utf-8 -*-
"""
Generates CDWT_Manual_Testing_Playbook.md with 100% complete, fully formatted,
copy-pasteable Request Body JSON payloads for EVERY test case.
Pure text, zero tables.
"""

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

fixed_slots_std = [
    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 6, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "timeSlots": []}
]

flexi_slots_std = [
    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
    {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0},
    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0}
]

split_slots_std = [
    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "timeSlots": []},
    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "timeSlots": []}
]

def json_str(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False)

# Build all 53 test cases
cases = []

# CDWT-DTO-01
cases.append({
    "id": "CDWT-DTO-01",
    "title": "Missing Authorization Header in Request",
    "category": "1. Route & Security",
    "priority": "P0 (Blocker / Security)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed",
    "auth": "None (Omit Authorization header)",
    "payload": {},
    "swagger_steps": [
        "Open Swagger: https://attendance2.dev.zoolwork.com/swagger/index.html",
        "Click Authorize button -> click Logout (lock icon must be open/unlocked)",
        "Expand POST /api/companies/{companyId}/worktemplates/fixed",
        "In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3",
        "In Request body, paste the JSON payload below",
        "Click Execute"
    ],
    "expected": "HTTP 401 Unauthorized with header Www-Authenticate: Bearer",
    "excel": ("Pass", "401", "Server cleanly blocked unauthenticated request with 401.")
})

# CDWT-DTO-02
cases.append({
    "id": "CDWT-DTO-02",
    "title": "Expired or Forged Bearer Token",
    "category": "1. Route & Security",
    "priority": "P0 (Blocker / Security)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed",
    "auth": "Bearer invalid_token_99999",
    "payload": {},
    "swagger_steps": [
        "In Swagger, click green Authorize button",
        "In the text box, enter a fake token: 12345",
        "Click Authorize -> click Close",
        "Expand POST /api/companies/{companyId}/worktemplates/fixed",
        "In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3",
        "In Request body, paste the JSON payload below",
        "Click Execute"
    ],
    "expected": "HTTP 401 Unauthorized with header Www-Authenticate: Bearer error=\"invalid_token\"",
    "excel": ("Pass", "401", "Fake token rejected with 401 error=\"invalid_token\". Note: Expired JWTs in DEV bypass verification (DEFECT-20261029-01).")
})

# CDWT-DTO-03
cases.append({
    "id": "CDWT-DTO-03",
    "title": "JWT Token Missing Tenant Claim",
    "category": "1. Route & Security",
    "priority": "P0 (Blocker / Security)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed",
    "auth": "Bearer <token-without-tenant-claim>",
    "payload": {},
    "swagger_steps": [
        "Authorize with a token that lacks tenant claim",
        "Expand POST /api/companies/{companyId}/worktemplates/fixed",
        "In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3",
        "In Request body, paste the JSON payload below",
        "Click Execute"
    ],
    "expected": "HTTP 401 / 403 Forbidden with SbpAuthorizationException",
    "excel": ("Pass", "401 / 403", "Token without tenant claim rejected.")
})

# CDWT-DTO-04
cases.append({
    "id": "CDWT-DTO-04",
    "title": "Client Tenant Spoofing Attempt via Header",
    "category": "1. Route & Security",
    "priority": "P1 (Must Work)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed",
    "auth": "Bearer <valid-token>",
    "payload": {},
    "swagger_steps": [
        "Authorize with valid token",
        "Expand POST /api/companies/{companyId}/worktemplates/fixed",
        "In __tenant parameter box, type: MaliciousSpoofedTenant",
        "In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3",
        "In Request body, paste the JSON payload below",
        "Click Execute"
    ],
    "expected": "Header spoofing ignored; token claims strictly enforced",
    "excel": ("Pass", "400 / 200", "Header spoofing ignored; token claims enforced.")
})

# CDWT-DTO-05
cases.append({
    "id": "CDWT-DTO-05",
    "title": "Zero GUID companyId in Route Parameter",
    "category": "1. Route & Security",
    "priority": "P2 (Should Work)",
    "method": "GET",
    "route": "/api/companies/00000000-0000-0000-0000-000000000000/worktemplates",
    "auth": "Bearer <valid-token>",
    "payload": None,
    "swagger_steps": [
        "Expand GET /api/companies/{companyId}/worktemplates",
        "In companyId, enter: 00000000-0000-0000-0000-000000000000",
        "Click Execute"
    ],
    "expected": "Expected: HTTP 404 Company Not Found | Actual DEV Bug: Returns HTTP 200 OK with [] (DEFECT-20261028-04)",
    "excel": ("Failed", "200", "DEFECT-20261028-04: Returns HTTP 200 [] instead of 404 Company Not Found.")
})

# CDWT-DTO-06
cases.append({
    "id": "CDWT-DTO-06",
    "title": "Malformed Non-Hex companyId in Route",
    "category": "1. Route & Security",
    "priority": "P1 (Must Work)",
    "method": "GET",
    "route": "/api/companies/invalid-company-guid-xyz/worktemplates",
    "auth": "Bearer <valid-token>",
    "payload": None,
    "swagger_steps": [
        "Expand GET /api/companies/{companyId}/worktemplates",
        "In companyId, enter: invalid-company-guid-xyz",
        "Click Execute"
    ],
    "expected": "HTTP 404 Not Found or HTTP 400 Bad Request (Route constraint rejected non-hex string)",
    "excel": ("Pass", "404 / 400", "Non-hex company GUID rejected by route constraint.")
})

# CDWT-DTO-07
cases.append({
    "id": "CDWT-DTO-07",
    "title": "Cross-Company Tenant Boundary Access",
    "category": "1. Route & Security",
    "priority": "P0 (Blocker / Security)",
    "method": "GET",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/27aa7562-b833-46f7-9cb7-d65f27171dab",
    "auth": "Bearer <valid-token>",
    "payload": None,
    "swagger_steps": [
        "In route, enter Company 2 GUID: 3a247435-3cea-83ae-6a9f-6dda99f386a3",
        "In templateId, enter Company 3's template GUID: 27aa7562-b833-46f7-9cb7-d65f27171dab",
        "Execute GET /api/companies/{companyId}/worktemplates/fixed/{id}"
    ],
    "expected": "HTTP 400 Cit.Attendance:9001 (Cross-company access blocked)",
    "excel": ("Pass", "400", "Cross-company boundary cleanly enforced.")
})

# CDWT-DTO-53
cases.append({
    "id": "CDWT-DTO-53",
    "title": "Swagger UI Missing OAuth2 (authorizationCode) Flow",
    "category": "1. Route & Security",
    "priority": "P1 (High Architecture / DX)",
    "method": "GET",
    "route": "/swagger/index.html",
    "auth": "N/A",
    "payload": None,
    "swagger_steps": [
        "Open Swagger: https://attendance2.dev.zoolwork.com/swagger/index.html",
        "Click Authorize button",
        "Observe: Only raw Bearer (http, Bearer) input is shown. Missing oauth2 authorizationCode flow."
    ],
    "expected": "Swagger should configure oauth2 with WebGateway_Swagger client matching Company Service (DEFECT-20261029-02)",
    "excel": ("Failed", "401 / Manual Bearer only", "DEFECT-20261029-02: Missing Swagger OAuth2 authorizationCode scheme.")
})

# CDWT-DTO-08
cases.append({
    "id": "CDWT-DTO-08",
    "title": "Empty JSON Payload Body ({}) on POST",
    "category": "2. Common DTO",
    "priority": "P0 (Blocker)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed",
    "auth": "Bearer <valid-token>",
    "payload": {},
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/fixed",
        "In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3",
        "In Request body, paste the JSON payload below",
        "Click Execute"
    ],
    "expected": "HTTP 400 Bad Request (Mandatory fields missing)",
    "excel": ("Pass", "400", "Empty payload cleanly rejected on POST.")
})

# CDWT-DTO-09
cases.append({
    "id": "CDWT-DTO-09",
    "title": "shortCode Length Below Minimum Boundary (1 Char)",
    "category": "2. Common DTO",
    "priority": "P1 (Must Work)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed",
    "auth": "Bearer <valid-token>",
    "payload": {
        "shortCode": "A",
        "templateName": {"en": "Min Code Boundary Test"}
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/fixed",
        "In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3",
        "In Request body, paste the JSON payload below",
        "Click Execute"
    ],
    "expected": "HTTP 400 Bad Request (\"shortCode length must be >= 2\")",
    "excel": ("Pass", "400", "shortCode < 2 characters rejected.")
})

# CDWT-DTO-10
cases.append({
    "id": "CDWT-DTO-10",
    "title": "shortCode Contains Special Characters / Symbols",
    "category": "2. Common DTO",
    "priority": "P1 (Must Work)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed",
    "auth": "Bearer <valid-token>",
    "payload": {
        "shortCode": "CDW@01!",
        "templateName": {"en": "Special Char Regex Test"}
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/fixed",
        "In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3",
        "In Request body, paste the JSON payload below",
        "Click Execute"
    ],
    "expected": "HTTP 400 Bad Request (\"Only alphanumeric characters allowed\")",
    "excel": ("Pass", "400", "Special characters in shortCode rejected.")
})

# CDWT-DTO-11
cases.append({
    "id": "CDWT-DTO-11",
    "title": "shortCode Length at Maximum Boundary (30 Chars)",
    "category": "2. Common DTO",
    "priority": "P0 (Blocker)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed",
    "auth": "Bearer <valid-token>",
    "payload": {
        "shortCode": "COMPDEF00000000000000000000001",
        "templateName": {"en": "Max Boundary 30 Characters"}
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/fixed",
        "In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3",
        "In Request body, paste the JSON payload below",
        "Click Execute"
    ],
    "expected": "HTTP 200 OK (or HTTP 400 Cit.Attendance:1010 if default exists)",
    "excel": ("Pass", "200 / 400 (1010)", "30-character max boundary accepted.")
})

# CDWT-DTO-12
cases.append({
    "id": "CDWT-DTO-12",
    "title": "shortCode Omitted or Empty String (\"\")",
    "category": "2. Common DTO",
    "priority": "P1 (Must Work)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed",
    "auth": "Bearer <valid-token>",
    "payload": {
        "shortCode": "",
        "templateName": {"en": "Auto Generated ShortCode Test"}
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/fixed",
        "In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3",
        "In Request body, paste the JSON payload below",
        "Click Execute"
    ],
    "expected": "HTTP 200 OK (Server auto-generates CDWxxxx code)",
    "excel": ("Pass", "200", "Server cleanly auto-generates shortCode.")
})

# CDWT-DTO-13
payload_13 = {
    "templateName": {"en": "Second CDWT Attempt"},
    "shortCode": "FIX999",
    "totalWorkDurationInMinutes": 2880,
    "totalWorkingDays": 6,
    "totalDaysOff": 1,
    "fixedTimeSlots": fixed_slots_std
}
cases.append({
    "id": "CDWT-DTO-13",
    "title": "Attempt to Create Duplicate Company Default",
    "category": "2. Common DTO",
    "priority": "P0 (Blocker)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed",
    "auth": "Bearer <valid-token>",
    "payload": payload_13,
    "swagger_steps": [
        "Target Company 2 (which already has an active default)",
        "Expand POST /api/companies/{companyId}/worktemplates/fixed",
        "In Request body, paste the full JSON payload below",
        "Click Execute"
    ],
    "expected": "HTTP 400 Cit.Attendance:1010 (\"Company default already exists.\")",
    "excel": ("Pass", "400", "One-Default Guard enforced (Cit.Attendance:1010).")
})

# CDWT-DTO-14
cases.append({
    "id": "CDWT-DTO-14",
    "title": "templateName Object Omitted or Null",
    "category": "2. Common DTO",
    "priority": "P0 (Blocker)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed",
    "auth": "Bearer <valid-token>",
    "payload": {
        "shortCode": "FIX003",
        "templateName": None
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/fixed",
        "In Request body, paste the JSON payload below",
        "Click Execute"
    ],
    "expected": "HTTP 400 Bad Request (\"Template name is required\")",
    "excel": ("Pass", "400", "Missing templateName rejected.")
})

# CDWT-DTO-15
cases.append({
    "id": "CDWT-DTO-15",
    "title": "templateName.en Empty String (\"\")",
    "category": "2. Common DTO",
    "priority": "P0 (Blocker)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed",
    "auth": "Bearer <valid-token>",
    "payload": {
        "shortCode": "FIX004",
        "templateName": {
            "en": ""
        }
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/fixed",
        "In Request body, paste the JSON payload below",
        "Click Execute"
    ],
    "expected": "HTTP 400 Bad Request (\"English name cannot be empty\")",
    "excel": ("Pass", "400", "Empty English name rejected.")
})

# CDWT-DTO-16
cases.append({
    "id": "CDWT-DTO-16",
    "title": "Bilingual Arabic UTF-8 Name Provided",
    "category": "2. Common DTO",
    "priority": "P1 (Must Work)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed",
    "auth": "Bearer <valid-token>",
    "payload": {
        "shortCode": "FIX005",
        "templateName": {
            "en": "Standard Default",
            "ar": "الجدول الافتراضي للشركة"
        },
        "totalWorkDurationInMinutes": 2880,
        "totalWorkingDays": 6,
        "totalDaysOff": 1,
        "fixedTimeSlots": fixed_slots_std
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/fixed",
        "In Request body, paste the JSON payload below",
        "Click Execute"
    ],
    "expected": "HTTP 200 OK (Arabic text preserved byte-exact)",
    "excel": ("Pass", "200", "Arabic UTF-8 text persisted byte-exact.")
})

# CDWT-DTO-17
cases.append({
    "id": "CDWT-DTO-17",
    "title": "tenantName Exposed in Client Request Body",
    "category": "2. Common DTO",
    "priority": "P2 (Design Gap)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed",
    "auth": "Bearer <valid-token>",
    "payload": {
        "shortCode": "FIX006",
        "tenantName": {
            "en": "SpoofedClientTenant"
        },
        "templateName": {"en": "TenantName Exposure Test"}
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/fixed",
        "In Request body, paste the JSON payload below",
        "Click Execute",
        "Check MongoDB Compass: Persisted as empty object {}"
    ],
    "expected": "Architectural Gap: tenantName should not be sent by client (DEFECT-20261026-04)",
    "excel": ("Failed", "200", "DEFECT-20261026-04: tenantName exposed in Swagger and stored as empty object in Mongo.")
})

# CDWT-DTO-18
cases.append({
    "id": "CDWT-DTO-18",
    "title": "Working Days + Days Off Sum Does NOT Equal 7",
    "category": "2. Common DTO",
    "priority": "P0 (Blocker)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed",
    "auth": "Bearer <valid-token>",
    "payload": {
        "shortCode": "FIX007",
        "templateName": {"en": "Invalid 8-Day Sum Test"},
        "totalWorkingDays": 6,
        "totalDaysOff": 2,
        "totalWorkDurationInMinutes": 2880,
        "fixedTimeSlots": fixed_slots_std
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/fixed",
        "In Request body, paste the JSON payload below",
        "Click Execute"
    ],
    "expected": "Expected: HTTP 400 Bad Request (\"Sum must equal 7\") | Actual DEV Bug: Throws HTTP 500 ValidationException (DEFECT-20261028-02)",
    "excel": ("Failed", "500", "DEFECT-20261028-02: Throws HTTP 500 ValidationException instead of HTTP 400.")
})

# CDWT-DTO-19
cases.append({
    "id": "CDWT-DTO-19",
    "title": "Standard 6 Working Days + 1 Day Off Schedule",
    "category": "3. Fixed WT",
    "priority": "P0 (Blocker)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "Standard 6 Days Working Schedule"},
        "shortCode": "FIX019",
        "totalWorkDurationInMinutes": 2880,
        "totalWorkingDays": 6,
        "totalDaysOff": 1,
        "fixedTimeSlots": fixed_slots_std
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/fixed",
        "In Request body, paste the full 7-slot JSON payload below",
        "Click Execute"
    ],
    "expected": "HTTP 200 OK (Creates active v1.0 Fixed CDWT)",
    "excel": ("Pass", "200", "Standard 6-day Fixed schedule accepted.")
})

# CDWT-DTO-20
slots_20 = [
    {"dayEnum": 8, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 6, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "timeSlots": []}
]
cases.append({
    "id": "CDWT-DTO-20",
    "title": "dayEnum Invalid Integer Value (e.g. 8 or 0)",
    "category": "3. Fixed WT",
    "priority": "P0 (Blocker)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "Invalid DayEnum 8 Test"},
        "shortCode": "FIX020",
        "totalWorkDurationInMinutes": 2880,
        "totalWorkingDays": 6,
        "totalDaysOff": 1,
        "fixedTimeSlots": slots_20
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/fixed",
        "In Request body, paste the JSON payload below (contains dayEnum: 8)",
        "Click Execute"
    ],
    "expected": "Expected: HTTP 400 Bad Request | Actual DEV Bug: Throws HTTP 500 ValidationException (DEFECT-20261028-02)",
    "excel": ("Failed", "500", "DEFECT-20261028-02: Out-of-range dayEnum throws HTTP 500 crash.")
})

# CDWT-DTO-21
cases.append({
    "id": "CDWT-DTO-21",
    "title": "Complete 7-Day Week Sequence (Sun=1 to Sat=7)",
    "category": "3. Fixed WT",
    "priority": "P0 (Blocker)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "Full 7 Days Sequence"},
        "shortCode": "FIX021",
        "totalWorkDurationInMinutes": 2880,
        "totalWorkingDays": 6,
        "totalDaysOff": 1,
        "fixedTimeSlots": fixed_slots_std
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/fixed",
        "In Request body, paste the JSON payload below",
        "Click Execute"
    ],
    "expected": "HTTP 200 OK (All 7 days defined once)",
    "excel": ("Pass", "200", "Full 7-day week sequence verified.")
})

# CDWT-DTO-22
slots_22 = [
    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 6, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": []}
]
cases.append({
    "id": "CDWT-DTO-22",
    "title": "Working Day Contradiction (isWorkingDay=false with Duration)",
    "category": "3. Fixed WT",
    "priority": "P0 (Blocker)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "Contradiction Day 7 Off With Duration"},
        "shortCode": "FIX022",
        "totalWorkDurationInMinutes": 2880,
        "totalWorkingDays": 6,
        "totalDaysOff": 1,
        "fixedTimeSlots": slots_22
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/fixed",
        "In Request body, paste the JSON payload below",
        "Click Execute"
    ],
    "expected": "HTTP 400 Bad Request (\"Off day cannot have working duration\")",
    "excel": ("Pass", "400", "Contradictory duration on day off rejected.")
})

# CDWT-DTO-23
slots_23 = [
    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 6, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "timeSlots": []}
]
cases.append({
    "id": "CDWT-DTO-23",
    "title": "Empty Recurrence Array on Active Working Day",
    "category": "3. Fixed WT",
    "priority": "P1 (Must Work)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "Empty Recurrence Array Test"},
        "shortCode": "FIX023",
        "totalWorkDurationInMinutes": 2880,
        "totalWorkingDays": 6,
        "totalDaysOff": 1,
        "fixedTimeSlots": slots_23
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/fixed",
        "In Request body, paste the JSON payload below (Day 1 has recurrenceOfMonth: [])",
        "Click Execute"
    ],
    "expected": "HTTP 400 Bad Request (\"Active day requires at least one recurrence\")",
    "excel": ("Pass", "400", "Empty recurrenceOfMonth rejected.")
})

# CDWT-DTO-24
slots_24 = [
    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "timeSlots": []},
    {"dayEnum": 7, "isWorkingDay": True, "recurrenceOfMonth": [2, 4], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]}
]
cases.append({
    "id": "CDWT-DTO-24",
    "title": "Alternate Saturday Off Pattern Configuration",
    "category": "3. Fixed WT",
    "priority": "P1 (Must Work)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "Alternate Saturday Off Schedule"},
        "shortCode": "FIX024",
        "totalWorkDurationInMinutes": 2880,
        "totalWorkingDays": 6,
        "totalDaysOff": 1,
        "fixedTimeSlots": slots_24
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/fixed",
        "In Request body, paste the JSON payload below (Sat has recurrence [2, 4])",
        "Click Execute"
    ],
    "expected": "HTTP 200 OK",
    "excel": ("Pass", "200", "Alternate Saturday off recurrence accepted cleanly.")
})

# CDWT-DTO-25
slots_25 = [
    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "17:00", "endTime": "09:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 6, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "timeSlots": []}
]
cases.append({
    "id": "CDWT-DTO-25",
    "title": "Start >= End Time Inversion (No Overnight)",
    "category": "3. Fixed WT",
    "priority": "P0 (Blocker)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "Inverted Timings 17:00 to 09:00"},
        "shortCode": "FIX025",
        "totalWorkDurationInMinutes": 2880,
        "totalWorkingDays": 6,
        "totalDaysOff": 1,
        "fixedTimeSlots": slots_25
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/fixed",
        "In Request body, paste the JSON payload below (Day 1 has 17:00 to 09:00)",
        "Click Execute"
    ],
    "expected": "HTTP 400 Bad Request (\"End time must be greater than start time\")",
    "excel": ("Pass", "400", "Inverted start/end time rejected.")
})

# CDWT-DTO-26
cases.append({
    "id": "CDWT-DTO-26",
    "title": "Total Duration Does Not Match Sum of Active Daily Slots",
    "category": "3. Fixed WT",
    "priority": "P1 (Must Work)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "Math Mismatch Total 2400 but Sum 2880"},
        "shortCode": "FIX026",
        "totalWorkDurationInMinutes": 2400,
        "totalWorkingDays": 6,
        "totalDaysOff": 1,
        "fixedTimeSlots": fixed_slots_std
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/fixed",
        "In Request body, paste the JSON payload below",
        "Click Execute"
    ],
    "expected": "HTTP 400 Bad Request (\"Total duration must match sum of active daily slots\")",
    "excel": ("Pass", "400", "Mathematical mismatch rejected.")
})

# CDWT-DTO-27
cases.append({
    "id": "CDWT-DTO-27",
    "title": "flexibleType Invalid Enum Value (e.g. 9 or 0)",
    "category": "4. Flexible WT",
    "priority": "P0 (Blocker)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "Invalid FlexiType 9"},
        "shortCode": "FLX027",
        "flexibleType": 9,
        "totalWorkDurationInMinutes": 2400,
        "totalWorkingDays": 5,
        "totalDaysOff": 2,
        "flexiTimeSlots": flexi_slots_std
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/flexi",
        "In Request body, paste the JSON payload below (has flexibleType: 9)",
        "Click Execute"
    ],
    "expected": "Expected: HTTP 400 Bad Request | Actual DEV Bug: Throws HTTP 500 ValidationException (DEFECT-20261028-02)",
    "excel": ("Failed", "500", "DEFECT-20261028-02: Invalid flexibleType enum throws HTTP 500 crash.")
})

# CDWT-DTO-28
cases.append({
    "id": "CDWT-DTO-28",
    "title": "Standard Daily Flexi Mode Configuration",
    "category": "4. Flexible WT",
    "priority": "P0 (Blocker)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "Standard Daily Flexi Mode"},
        "shortCode": "FLX028",
        "flexibleType": 1,
        "totalWorkDurationInMinutes": 2400,
        "totalWorkingDays": 5,
        "totalDaysOff": 2,
        "flexiTimeSlots": flexi_slots_std
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/flexi",
        "In Request body, paste the JSON payload below",
        "Click Execute"
    ],
    "expected": "HTTP 200 OK (Creates active v1.0 Daily Flexi CDWT)",
    "excel": ("Pass", "200", "Standard Daily Flexi accepted.")
})

# CDWT-DTO-29
flexi_weekly_slots = [
    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0},
    {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0},
    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0}
]
cases.append({
    "id": "CDWT-DTO-29",
    "title": "Standard Weekly Pool Mode Configuration",
    "category": "4. Flexible WT",
    "priority": "P0 (Blocker)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "Standard Weekly Pool Flexi Mode"},
        "shortCode": "FLX029",
        "flexibleType": 2,
        "totalWorkDurationInMinutes": 2400,
        "totalWorkingDays": 5,
        "totalDaysOff": 2,
        "flexiTimeSlots": flexi_weekly_slots
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/flexi",
        "In Request body, paste the JSON payload below",
        "Click Execute"
    ],
    "expected": "HTTP 200 OK (Creates active v1.0 Weekly Flexi CDWT)",
    "excel": ("Pass", "200", "Standard Weekly Pool accepted.")
})

# CDWT-DTO-30
flexi_25h_slots = [
    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 1500},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
    {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0},
    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0}
]
cases.append({
    "id": "CDWT-DTO-30",
    "title": "CRITICAL: Daily Duration Exceeding 24 Hours (1500m / 25h)",
    "category": "4. Flexible WT",
    "priority": "P0 (Blocker)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "25 Hours Daily Flexi Shift"},
        "shortCode": "FLX030",
        "flexibleType": 1,
        "workDurationInMinutes": 1500,
        "totalWorkDurationInMinutes": 3420,
        "totalWorkingDays": 5,
        "totalDaysOff": 2,
        "flexiTimeSlots": flexi_25h_slots
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/flexi",
        "In Request body, paste the JSON payload below (Day 1 has 1500 minutes)",
        "Click Execute"
    ],
    "expected": "Expected: HTTP 400 Bad Request | Actual DEV Bug: Server returns HTTP 200 OK without validation (DEFECT-20261028-01)",
    "excel": ("Failed", "200", "DEFECT-20261028-01: Accepted 1500 min (25h/day) with HTTP 200 OK without validation.")
})

# CDWT-DTO-31
cases.append({
    "id": "CDWT-DTO-31",
    "title": "Weekly Pool Exceeding 168 Hours / Week",
    "category": "4. Flexible WT",
    "priority": "P0 (Blocker)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "Exceeding 168 Hours Weekly"},
        "shortCode": "FLX031",
        "flexibleType": 2,
        "totalWorkDurationInMinutes": 10500,
        "totalWorkingDays": 5,
        "totalDaysOff": 2,
        "flexiTimeSlots": flexi_weekly_slots
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/flexi",
        "In Request body, paste the JSON payload below (has 10500 minutes)",
        "Click Execute"
    ],
    "expected": "HTTP 400 Bad Request (\"Weekly pool cannot exceed 10080 minutes / 168 hours\")",
    "excel": ("Pass", "400", "Weekly pool > 168 hours cleanly rejected.")
})

# CDWT-DTO-32
flexi_0h_slots = [
    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
    {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0},
    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0}
]
cases.append({
    "id": "CDWT-DTO-32",
    "title": "Active Working Day Configured with 0 Hours",
    "category": "4. Flexible WT",
    "priority": "P1 (Must Work)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "Active Day With 0 Hours"},
        "shortCode": "FLX032",
        "flexibleType": 1,
        "totalWorkDurationInMinutes": 1920,
        "totalWorkingDays": 5,
        "totalDaysOff": 2,
        "flexiTimeSlots": flexi_0h_slots
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/flexi",
        "In Request body, paste the JSON payload below (Day 1 is active with 0m)",
        "Click Execute"
    ],
    "expected": "HTTP 400 Bad Request (\"Active working day must have > 0 duration\")",
    "excel": ("Pass", "400", "0 hours on active day rejected.")
})

# CDWT-DTO-33
cases.append({
    "id": "CDWT-DTO-33",
    "title": "Negative Work Duration (< 0 Minutes)",
    "category": "4. Flexible WT",
    "priority": "P0 (Blocker)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "Negative Duration Test"},
        "shortCode": "FLX033",
        "flexibleType": 1,
        "workDurationInMinutes": -480,
        "totalWorkDurationInMinutes": 2400,
        "totalWorkingDays": 5,
        "totalDaysOff": 2,
        "flexiTimeSlots": flexi_slots_std
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/flexi",
        "In Request body, paste the JSON payload below",
        "Click Execute"
    ],
    "expected": "HTTP 400 Bad Request (\"Duration must be greater than 0\")",
    "excel": ("Pass", "400", "Negative duration rejected.")
})

# CDWT-DTO-34
flexi_weekly_conflict = [
    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0},
    {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0},
    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0}
]
cases.append({
    "id": "CDWT-DTO-34",
    "title": "Weekly Mode with Non-Zero Daily Durations",
    "category": "4. Flexible WT",
    "priority": "P1 (Must Work)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "Weekly Mode With Non Zero Daily Slot"},
        "shortCode": "FLX034",
        "flexibleType": 2,
        "totalWorkDurationInMinutes": 2400,
        "totalWorkingDays": 5,
        "totalDaysOff": 2,
        "flexiTimeSlots": flexi_weekly_conflict
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/flexi",
        "In Request body, paste the JSON payload below (flexibleType 2 with daily duration)",
        "Click Execute"
    ],
    "expected": "HTTP 400 Bad Request (\"Weekly pool requires daily duration = 0\")",
    "excel": ("Pass", "400", "Weekly mode contradiction rejected.")
})

# CDWT-DTO-35
cases.append({
    "id": "CDWT-DTO-35",
    "title": "Standard 2-Interval Split Shift Configuration",
    "category": "5. Split WT",
    "priority": "P0 (Blocker)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "Standard 2-Interval Split Shift"},
        "shortCode": "SPL035",
        "totalWorkDurationInMinutes": 2400,
        "totalWorkingDays": 5,
        "totalDaysOff": 2,
        "splitTimeSlots": split_slots_std
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/split",
        "In Request body, paste the full 7-slot JSON payload below",
        "Click Execute"
    ],
    "expected": "HTTP 200 OK (Creates active v1.0 Split CDWT)",
    "excel": ("Pass", "200", "Standard 2-interval Split shift accepted.")
})

# CDWT-DTO-36
split_slots_zero_gap = [
    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "12:00", "endTime": "16:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "timeSlots": []},
    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "timeSlots": []}
]
cases.append({
    "id": "CDWT-DTO-36",
    "title": "Contiguous Intervals / Zero Break Gap",
    "category": "5. Split WT",
    "priority": "P0 (Blocker)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "Contiguous Zero Break Gap"},
        "shortCode": "SPL036",
        "totalWorkDurationInMinutes": 2400,
        "totalWorkingDays": 5,
        "totalDaysOff": 2,
        "splitTimeSlots": split_slots_zero_gap
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/split",
        "In Request body, paste the JSON payload below (Slot 1 ends 12:00, Slot 2 starts 12:00)",
        "Click Execute"
    ],
    "expected": "Expected: HTTP 400 Bad Request | Actual DEV Bug: Throws HTTP 500 ValidationException (DEFECT-20261028-02)",
    "excel": ("Failed", "500", "DEFECT-20261028-02: Zero break gap throws HTTP 500 crash.")
})

# CDWT-DTO-37
split_slots_neg_gap = [
    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "11:30", "endTime": "15:30", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "timeSlots": []},
    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "timeSlots": []}
]
cases.append({
    "id": "CDWT-DTO-37",
    "title": "Negative Break Gap Between Intervals",
    "category": "5. Split WT",
    "priority": "P0 (Blocker)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "Negative Break Gap 11:30 before 12:00"},
        "shortCode": "SPL037",
        "totalWorkDurationInMinutes": 2400,
        "totalWorkingDays": 5,
        "totalDaysOff": 2,
        "splitTimeSlots": split_slots_neg_gap
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/split",
        "In Request body, paste the JSON payload below (Interval 2 starts at 11:30)",
        "Click Execute"
    ],
    "expected": "Expected: HTTP 400 Bad Request | Actual DEV Bug: Throws HTTP 500 ValidationException (DEFECT-20261028-02)",
    "excel": ("Failed", "500", "DEFECT-20261028-02: Negative break gap throws HTTP 500 crash.")
})

# CDWT-DTO-38
split_slots_overlap = [
    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "13:00", "workDurationInMinutes": 300},
        {"startTime": "12:00", "endTime": "17:00", "workDurationInMinutes": 300}
    ]},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "timeSlots": []},
    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "timeSlots": []}
]
cases.append({
    "id": "CDWT-DTO-38",
    "title": "Overlapping Interval Time Ranges",
    "category": "5. Split WT",
    "priority": "P0 (Blocker)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "1-Hour Overlapping Intervals"},
        "shortCode": "SPL038",
        "totalWorkDurationInMinutes": 2400,
        "totalWorkingDays": 5,
        "totalDaysOff": 2,
        "splitTimeSlots": split_slots_overlap
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/split",
        "In Request body, paste the JSON payload below (Intervals overlap from 12:00 to 13:00)",
        "Click Execute"
    ],
    "expected": "Expected: HTTP 400 Bad Request | Actual DEV Bug: Throws HTTP 500 ValidationException (DEFECT-20261028-02)",
    "excel": ("Failed", "500", "DEFECT-20261028-02: Overlapping intervals throw HTTP 500 crash.")
})

# CDWT-DTO-39
split_slots_invert = [
    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "12:00", "endTime": "08:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "timeSlots": []},
    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "timeSlots": []}
]
cases.append({
    "id": "CDWT-DTO-39",
    "title": "Inverted Start/End Timings in a Split Interval",
    "category": "5. Split WT",
    "priority": "P0 (Blocker)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "Inverted Interval 12:00 to 08:00"},
        "shortCode": "SPL039",
        "totalWorkDurationInMinutes": 2400,
        "totalWorkingDays": 5,
        "totalDaysOff": 2,
        "splitTimeSlots": split_slots_invert
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/split",
        "In Request body, paste the JSON payload below (Slot 1 has startTime: 12:00, endTime: 08:00)",
        "Click Execute"
    ],
    "expected": "Expected: HTTP 400 Bad Request | Actual DEV Bug: Server returns HTTP 200 OK without validation (DEFECT-20261028-01)",
    "excel": ("Failed", "200", "DEFECT-20261028-01: Inverted interval timings accepted with HTTP 200 OK.")
})

# CDWT-DTO-40
split_slots_off_active = [
    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]},
    {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "timeSlots": []},
    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
    ]}
]
cases.append({
    "id": "CDWT-DTO-40",
    "title": "Active Intervals Configured on a Day Off",
    "category": "5. Split WT",
    "priority": "P0 (Blocker)",
    "method": "POST",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "Contradiction Day 7 Off With Active Intervals"},
        "shortCode": "SPL040",
        "totalWorkDurationInMinutes": 2400,
        "totalWorkingDays": 5,
        "totalDaysOff": 2,
        "splitTimeSlots": split_slots_off_active
    },
    "swagger_steps": [
        "Expand POST /api/companies/{companyId}/worktemplates/split",
        "In Request body, paste the JSON payload below (Day 7 has isWorkingDay: false with active intervals)",
        "Click Execute"
    ],
    "expected": "Expected: HTTP 400 Bad Request | Actual DEV Bug: Throws HTTP 500 ValidationException (DEFECT-20261028-02)",
    "excel": ("Failed", "500", "DEFECT-20261028-02: Active intervals on day off throw HTTP 500 crash.")
})

# CDWT-DTO-41
cases.append({
    "id": "CDWT-DTO-41",
    "title": "Empty JSON Payload Body ({}) on PATCH",
    "category": "6. PATCH & Immutability",
    "priority": "P0 (Blocker)",
    "method": "PATCH",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{activeTemplateId}",
    "auth": "Bearer <valid-token>",
    "payload": {},
    "swagger_steps": [
        "Expand PATCH /api/companies/{companyId}/worktemplates/fixed/{id}",
        "In id, enter active CDWT ID: e1a64e28-ecd6-49b5-9155-fd30a11d9e8d",
        "In Request body, paste: {}",
        "Click Execute"
    ],
    "expected": "Expected: HTTP 400 Bad Request (\"At least one update field is required\") | Actual DEV Bug: Throws HTTP 500 ValidationException (DEFECT-20261028-02)",
    "excel": ("Failed", "500", "DEFECT-20261028-02: Empty PATCH body throws HTTP 500 crash.")
})

# CDWT-DTO-42
cases.append({
    "id": "CDWT-DTO-42",
    "title": "Attempt to Mutate shortCode via PATCH",
    "category": "6. PATCH & Immutability",
    "priority": "P0 (Blocker)",
    "method": "PATCH",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{activeTemplateId}",
    "auth": "Bearer <valid-token>",
    "payload": {
        "shortCode": "HACKCODE"
    },
    "swagger_steps": [
        "Expand PATCH /api/companies/{companyId}/worktemplates/fixed/{id}",
        "In id, enter active CDWT ID: e1a64e28-ecd6-49b5-9155-fd30a11d9e8d",
        "In Request body, paste: {\"shortCode\": \"HACKCODE\"}",
        "Click Execute"
    ],
    "expected": "HTTP 400 Cit.Attendance:1107 (\"shortCode is locked and cannot be modified\")",
    "excel": ("Pass", "400", "shortCode immutability strictly locked (Cit.Attendance:1107).")
})

# CDWT-DTO-43
cases.append({
    "id": "CDWT-DTO-43",
    "title": "Attempt to Reassign Entity to Another Company via PATCH",
    "category": "6. PATCH & Immutability",
    "priority": "P0 (Blocker)",
    "method": "PATCH",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{activeTemplateId}",
    "auth": "Bearer <valid-token>",
    "payload": {
        "companyId": "3a247435-e31d-ef15-8cc9-62c587f4eb3f"
    },
    "swagger_steps": [
        "Expand PATCH /api/companies/{companyId}/worktemplates/fixed/{id}",
        "In Request body, paste the JSON payload below",
        "Click Execute"
    ],
    "expected": "Cross-company reassignment ignored or rejected with HTTP 400",
    "excel": ("Pass", "400 / 200 (ignored)", "Cross-company transfer locked.")
})

# CDWT-DTO-44
cases.append({
    "id": "CDWT-DTO-44",
    "title": "Attempt to Spoof tenantName via PATCH",
    "category": "6. PATCH & Immutability",
    "priority": "P2 (Design Gap)",
    "method": "PATCH",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{activeTemplateId}",
    "auth": "Bearer <valid-token>",
    "payload": {
        "tenantName": {
            "en": "SpoofedTenantName"
        }
    },
    "swagger_steps": [
        "Expand PATCH /api/companies/{companyId}/worktemplates/fixed/{id}",
        "In Request body, paste the JSON payload below",
        "Click Execute"
    ],
    "expected": "Server should ignore or reject client tenantName (DEFECT-20261026-04)",
    "excel": ("Failed", "200", "DEFECT-20261026-04: tenantName accepted in PATCH body.")
})

# CDWT-DTO-45
cases.append({
    "id": "CDWT-DTO-45",
    "title": "Attempt to Edit an Archived / Superseded Version ID",
    "category": "6. PATCH & Immutability",
    "priority": "P1 (Must Work)",
    "method": "PATCH",
    "route": "/api/companies/3a247436-8669-844a-7d2f-1a209af02d8e/worktemplates/flexi/a31a2f5e-bc53-4221-b2d2-ff8c5ed54dbb",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {
            "en": "Attempt Edit Archived Version v1.0"
        }
    },
    "swagger_steps": [
        "Target Company 4 archived v1.0 ID: a31a2f5e-bc53-4221-b2d2-ff8c5ed54dbb",
        "Expand PATCH /api/companies/{companyId}/worktemplates/flexi/{id}",
        "In Request body, paste the JSON payload below",
        "Click Execute"
    ],
    "expected": "HTTP 400 Cit.Attendance:1107 (\"Archived template cannot be edited\")",
    "excel": ("Pass", "400", "Archived versions protected from edits (Cit.Attendance:1107).")
})

# CDWT-DTO-46
cases.append({
    "id": "CDWT-DTO-46",
    "title": "Attempt to Edit a Non-Existent Template GUID",
    "category": "6. PATCH & Immutability",
    "priority": "P1 (Must Work)",
    "method": "PATCH",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/ffffffff-ffff-ffff-ffff-ffffffffffff",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {
            "en": "Edit Non Existent Entity"
        }
    },
    "swagger_steps": [
        "In id, enter fake GUID: ffffffff-ffff-ffff-ffff-ffffffffffff",
        "Expand PATCH /api/companies/{companyId}/worktemplates/fixed/{id}",
        "In Request body, paste the JSON payload below",
        "Click Execute"
    ],
    "expected": "HTTP 400 Cit.Attendance:1101 (\"Template not found\")",
    "excel": ("Pass", "400", "Non-existent template returns Cit.Attendance:1101.")
})

# CDWT-DTO-47
slots_47 = [
    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 6, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "timeSlots": []}
]
cases.append({
    "id": "CDWT-DTO-47",
    "title": "Valid In-Place Timing Shift on Thursday",
    "category": "6. PATCH & Immutability",
    "priority": "P0 (Blocker)",
    "method": "PATCH",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{activeTemplateId}",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "Shift Timing Updated to 09:00 Thursday"},
        "totalWorkDurationInMinutes": 2880,
        "totalWorkingDays": 6,
        "totalDaysOff": 1,
        "fixedTimeSlots": slots_47
    },
    "swagger_steps": [
        "In id, enter active Fixed CDWT ID",
        "In Request body, paste the JSON payload below (Thursday shift changed to 09:00-17:00)",
        "Click Execute"
    ],
    "expected": "HTTP 200 OK (Creates active v2.0, archives v1.0)",
    "excel": ("Pass", "200", "In-place edit creates next version and archives previous.")
})

# CDWT-DTO-48
cases.append({
    "id": "CDWT-DTO-48",
    "title": "Migrate Company Default from Fixed to Flexible Daily",
    "category": "6. PATCH & Immutability",
    "priority": "P0 (Blocker)",
    "method": "PATCH",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{activeFixedId}",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "Migrated to Flexible Daily CDWT"},
        "flexibleType": 1,
        "totalWorkDurationInMinutes": 2400,
        "totalWorkingDays": 5,
        "totalDaysOff": 2,
        "flexiTimeSlots": flexi_slots_std
    },
    "swagger_steps": [
        "In id, enter active Fixed CDWT ID",
        "In Request body, paste the Flexible Daily migration JSON below",
        "Click Execute"
    ],
    "expected": "HTTP 200 OK (Creates active v2.0 Flexi CDWT)",
    "excel": ("Pass", "200", "Fixed to Flexi migration accepted.")
})

# CDWT-DTO-49
cases.append({
    "id": "CDWT-DTO-49",
    "title": "Migrate Company Default from Fixed to Split Shift",
    "category": "6. PATCH & Immutability",
    "priority": "P0 (Blocker)",
    "method": "PATCH",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{activeFixedId}",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "Migrated to Split Shift CDWT"},
        "totalWorkDurationInMinutes": 2400,
        "totalWorkingDays": 5,
        "totalDaysOff": 2,
        "splitTimeSlots": split_slots_std
    },
    "swagger_steps": [
        "In id, enter active Fixed CDWT ID",
        "In Request body, paste the Split Shift migration JSON below",
        "Click Execute"
    ],
    "expected": "HTTP 200 OK (Creates active v2.0 Split CDWT)",
    "excel": ("Pass", "200", "Fixed to Split migration accepted.")
})

# CDWT-DTO-50
cases.append({
    "id": "CDWT-DTO-50",
    "title": "Attempt to Migrate Company Default to Roster / Rotation",
    "category": "6. PATCH & Immutability",
    "priority": "P1 (Must Work)",
    "method": "PATCH",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{activeFixedId}",
    "auth": "Bearer <valid-token>",
    "payload": {
        "templateName": {"en": "Attempt Migrate to Roster CDWT"},
        "templateType": "Roster",
        "rosterSlots": [
            {"cycleDays": 14, "shifts": []}
        ]
    },
    "swagger_steps": [
        "In id, enter active Fixed CDWT ID",
        "In Request body, paste the JSON payload below",
        "Click Execute"
    ],
    "expected": "HTTP 400 Bad Request (CDWT is restricted to Fixed, Flexi, Split)",
    "excel": ("Pass", "400", "CDWT restricted to Fixed, Flexi, Split.")
})

# CDWT-DTO-51
cases.append({
    "id": "CDWT-DTO-51",
    "title": "Attempt to Archive Active Company Default Work Template",
    "category": "6. PATCH & Immutability",
    "priority": "P1 (Must Work)",
    "method": "PATCH",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/{activeTemplateId}/archive",
    "auth": "Bearer <valid-token>",
    "payload": None,
    "swagger_steps": [
        "Expand PATCH /api/companies/{companyId}/worktemplates/{activeId}/archive",
        "In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3",
        "In activeId, enter active CDWT ID: e1a64e28-ecd6-49b5-9155-fd30a11d9e8d",
        "Click Execute"
    ],
    "expected": "Expected: HTTP 400 Cit.Attendance:1202 | Actual DEV Bug: Server returns HTTP 200 OK without guard (DEFECT-20261028-03)",
    "excel": ("Failed", "200", "DEFECT-20261028-03: Active default archived without guard.")
})

# CDWT-DTO-52
cases.append({
    "id": "CDWT-DTO-52",
    "title": "Attempt to Soft-Delete Active Company Default Work Template",
    "category": "6. PATCH & Immutability",
    "priority": "P1 (Must Work)",
    "method": "PATCH",
    "route": "/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/{activeTemplateId}/delete",
    "auth": "Bearer <valid-token>",
    "payload": None,
    "swagger_steps": [
        "Expand PATCH /api/companies/{companyId}/worktemplates/{activeId}/delete",
        "In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3",
        "In activeId, enter active CDWT ID: e1a64e28-ecd6-49b5-9155-fd30a11d9e8d",
        "Click Execute"
    ],
    "expected": "Expected: HTTP 400 Cit.Attendance:1202 | Actual DEV Bug: Server returns HTTP 200 OK without guard (DEFECT-20261028-03)",
    "excel": ("Failed", "200", "DEFECT-20261028-03: Active default soft-deleted without guard.")
})

# Generate Output Text
lines = []
lines.append("# Company Default Work Template (CDWT) — Manual Testing Playbook")
lines.append("## Complete Step-by-Step Test Data Guide for All 53 Edge Cases (With Full Request Body Payloads)")
lines.append("")
lines.append("Target Microservice: SP.AttendanceSvc (.NET 9 / ASP.NET Core)")
lines.append("Base DEV URL: https://attendance2.dev.zoolwork.com")
lines.append("Auth Server: https://auth8.dev.zoolwork.com/connect/token (tenant: Attendance)")
lines.append("Swagger UI: https://attendance2.dev.zoolwork.com/swagger/index.html")
lines.append("Excel Workbook: CompanyDefault_DTO_Validation_TestCases.xlsx")
lines.append("")
lines.append("Target Companies for Testing:")
lines.append("- Company 2 (Attendance 2): 3a247435-3cea-83ae-6a9f-6dda99f386a3 (Fixed CDWT Active v3.0)")
lines.append("- Company 3 (Attendance 3): 3a247435-e31d-ef15-8cc9-62c587f4eb3f (Fixed CDWT Active v2.0)")
lines.append("- Company 4 (Attendance 4): 3a247436-8669-844a-7d2f-1a209af02d8e (Flexi CDWT Active v2.0)")
lines.append("Tenant Header: __tenant: Attendance")
lines.append("")

current_cat = None
for c in cases:
    if c["category"] != current_cat:
        current_cat = c["category"]
        lines.append("=" * 80)
        lines.append(f"CATEGORY: {current_cat.upper()}")
        lines.append("=" * 80)
        lines.append("")

    lines.append("-" * 80)
    lines.append(f"TEST CASE: {c['id']}")
    lines.append(f"Scenario: {c['title']}")
    lines.append(f"Category: {c['category']}")
    lines.append(f"Priority: {c['priority']}")
    lines.append("-" * 80)
    lines.append("OPTION 1 (Swagger UI Steps):")
    for step in c["swagger_steps"]:
        lines.append(f"- {step}")
    lines.append("")
    lines.append("OPTION 2 (Postman / Payload Steps):")
    lines.append(f"- Method: {c['method']}")
    lines.append(f"- Full URL: https://attendance2.dev.zoolwork.com{c['route']}")
    lines.append(f"- Authorization: {c['auth']}")
    lines.append("- Headers:")
    lines.append("    Content-Type: application/json")
    lines.append("    __tenant: Attendance")
    lines.append("- Request Body (JSON Payload):")
    if c["payload"] is None:
        lines.append("    None (Query / Route Parameter only)")
    else:
        lines.append("```json")
        lines.append(json_str(c["payload"]))
        lines.append("```")
    lines.append("")
    lines.append("EXPECTED RESULT:")
    lines.append(f"- {c['expected']}")
    lines.append("")
    lines.append("EXCEL LOGGING:")
    lines.append(f"- Col L (Manual Status): {c['excel'][0]}")
    lines.append(f"- Col M (Actual HTTP Code): {c['excel'][1]}")
    lines.append(f"- Col N (Actual Notes): {c['excel'][2]}")
    lines.append("")

lines.append("=" * 80)
lines.append("END OF PLAYBOOK — ALL 53 TEST CASES WITH FULL REQUEST BODY PAYLOADS")
lines.append("=" * 80)

full_text = "\\n".join(lines)
with open('CDWT_Manual_Testing_Playbook.md', 'w', encoding='utf-8') as f:
    f.write(full_text)

print(f"SUCCESS: Generated CDWT_Manual_Testing_Playbook.md ({len(full_text)} characters, {len(lines)} lines)!")

