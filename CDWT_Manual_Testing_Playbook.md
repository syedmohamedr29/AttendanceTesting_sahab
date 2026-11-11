# Company Default Work Template (CDWT) — Manual Testing Playbook
## Complete Step-by-Step Test Data Guide for All 53 Edge Cases (With Full Request Body Payloads)

> **Target Microservice:** SP.AttendanceSvc (.NET 9 / ASP.NET Core)  
> **Base DEV URL:** `https://attendance2.dev.zoolwork.com`  
> **Auth Server:** `https://auth8.dev.zoolwork.com/connect/token` (tenant: `Attendance`)  
> **Swagger UI:** `https://attendance2.dev.zoolwork.com/swagger/index.html`  
> **Excel Workbook:** `CompanyDefault_DTO_Validation_TestCases.xlsx`  

### Target Companies for Testing:
- **Company 2 (Attendance 2):** `3a247435-3cea-83ae-6a9f-6dda99f386a3` (Fixed CDWT Active v3.0 `e1a64e28-ecd6-49b5-9155-fd30a11d9e8d`)
- **Company 3 (Attendance 3):** `3a247435-e31d-ef15-8cc9-62c587f4eb3f` (Fixed CDWT Active v2.0 `27aa7562-b833-46f7-9cb7-d65f27171dab`)
- **Company 4 (Attendance 4):** `3a247436-8669-844a-7d2f-1a209af02d8e` (Flexi CDWT Active v2.0 `53470658-5f9b-47b4-b254-f96b9501401c`)
- **Tenant Header:** `__tenant: Attendance`


================================================================================
# CATEGORY: 1. ROUTE & SECURITY
================================================================================

---

## CDWT-DTO-01: Missing Authorization Header in Request

- **Category:** 1. Route & Security
- **Priority:** P0 (Blocker / Security)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`

### OPTION 1 (Swagger UI Steps):
1. Open Swagger: https://attendance2.dev.zoolwork.com/swagger/index.html
2. Click Authorize button -> click Logout (lock icon must be open/unlocked)
3. Expand POST /api/companies/{companyId}/worktemplates/fixed
4. In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3
5. In Request body, paste the JSON payload below
6. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`
- **Authorization:** `None (Omit Authorization header)`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{}
```

### EXPECTED RESULT:
- HTTP 401 Unauthorized with header Www-Authenticate: Bearer

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `401`
- **Col N (Actual Notes):** Server cleanly blocked unauthenticated request with 401.

---

## CDWT-DTO-02: Expired or Forged Bearer Token

- **Category:** 1. Route & Security
- **Priority:** P0 (Blocker / Security)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`

### OPTION 1 (Swagger UI Steps):
1. In Swagger, click green Authorize button
2. In the text box, enter a fake token: 12345
3. Click Authorize -> click Close
4. Expand POST /api/companies/{companyId}/worktemplates/fixed
5. In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3
6. In Request body, paste the JSON payload below
7. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`
- **Authorization:** `Bearer invalid_token_99999`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{}
```

### EXPECTED RESULT:
- HTTP 401 Unauthorized with header Www-Authenticate: Bearer error="invalid_token"

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `401`
- **Col N (Actual Notes):** Fake token rejected with 401 error="invalid_token". Note: Expired JWTs in DEV bypass verification (DEFECT-20261029-01).

---

## CDWT-DTO-03: JWT Token Missing Tenant Claim

- **Category:** 1. Route & Security
- **Priority:** P0 (Blocker / Security)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`

### OPTION 1 (Swagger UI Steps):
1. Authorize with a token that lacks tenant claim
2. Expand POST /api/companies/{companyId}/worktemplates/fixed
3. In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3
4. In Request body, paste the JSON payload below
5. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`
- **Authorization:** `Bearer <token-without-tenant-claim>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{}
```

### EXPECTED RESULT:
- HTTP 401 / 403 Forbidden with SbpAuthorizationException

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `401 / 403`
- **Col N (Actual Notes):** Token without tenant claim rejected.

---

## CDWT-DTO-04: Client Tenant Spoofing Attempt via Header

- **Category:** 1. Route & Security
- **Priority:** P1 (Must Work)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`

### OPTION 1 (Swagger UI Steps):
1. Authorize with valid token
2. Expand POST /api/companies/{companyId}/worktemplates/fixed
3. In __tenant parameter box, type: MaliciousSpoofedTenant
4. In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3
5. In Request body, paste the JSON payload below
6. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{}
```

### EXPECTED RESULT:
- Header spoofing ignored; token claims strictly enforced

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `400 / 200`
- **Col N (Actual Notes):** Header spoofing ignored; token claims enforced.

---

## CDWT-DTO-05: Zero GUID companyId in Route Parameter

- **Category:** 1. Route & Security
- **Priority:** P2 (Should Work)
- **Method & Route:** `GET /api/companies/00000000-0000-0000-0000-000000000000/worktemplates`

### OPTION 1 (Swagger UI Steps):
1. Expand GET /api/companies/{companyId}/worktemplates
2. In companyId, enter: 00000000-0000-0000-0000-000000000000
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `GET`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/00000000-0000-0000-0000-000000000000/worktemplates`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
  `None (Query / Route Parameter only)`

### EXPECTED RESULT:
- Expected: HTTP 404 Company Not Found | Actual DEV Bug: Returns HTTP 200 OK with [] (DEFECT-20261028-04)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Failed`
- **Col M (Actual HTTP Code):** `200`
- **Col N (Actual Notes):** DEFECT-20261028-04: Returns HTTP 200 [] instead of 404 Company Not Found.

---

## CDWT-DTO-06: Malformed Non-Hex companyId in Route

- **Category:** 1. Route & Security
- **Priority:** P1 (Must Work)
- **Method & Route:** `GET /api/companies/invalid-company-guid-xyz/worktemplates`

### OPTION 1 (Swagger UI Steps):
1. Expand GET /api/companies/{companyId}/worktemplates
2. In companyId, enter: invalid-company-guid-xyz
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `GET`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/invalid-company-guid-xyz/worktemplates`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
  `None (Query / Route Parameter only)`

### EXPECTED RESULT:
- HTTP 404 Not Found or HTTP 400 Bad Request (Route constraint rejected non-hex string)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `404 / 400`
- **Col N (Actual Notes):** Non-hex company GUID rejected by route constraint.

---

## CDWT-DTO-07: Cross-Company Tenant Boundary Access

- **Category:** 1. Route & Security
- **Priority:** P0 (Blocker / Security)
- **Method & Route:** `GET /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/27aa7562-b833-46f7-9cb7-d65f27171dab`

### OPTION 1 (Swagger UI Steps):
1. In route, enter Company 2 GUID: 3a247435-3cea-83ae-6a9f-6dda99f386a3
2. In templateId, enter Company 3's template GUID: 27aa7562-b833-46f7-9cb7-d65f27171dab
3. Execute GET /api/companies/{companyId}/worktemplates/fixed/{id}

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `GET`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/27aa7562-b833-46f7-9cb7-d65f27171dab`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
  `None (Query / Route Parameter only)`

### EXPECTED RESULT:
- HTTP 400 Cit.Attendance:9001 (Cross-company access blocked)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `400`
- **Col N (Actual Notes):** Cross-company boundary cleanly enforced.

---

## CDWT-DTO-53: Swagger UI Missing OAuth2 (authorizationCode) Flow

- **Category:** 1. Route & Security
- **Priority:** P1 (High Architecture / DX)
- **Method & Route:** `GET /swagger/index.html`

### OPTION 1 (Swagger UI Steps):
1. Open Swagger: https://attendance2.dev.zoolwork.com/swagger/index.html
2. Click Authorize button
3. Observe: Only raw Bearer (http, Bearer) input is shown. Missing oauth2 authorizationCode flow.

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `GET`
- **Full URL:** `https://attendance2.dev.zoolwork.com/swagger/index.html`
- **Authorization:** `N/A`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
  `None (Query / Route Parameter only)`

### EXPECTED RESULT:
- Swagger should configure oauth2 with WebGateway_Swagger client matching Company Service (DEFECT-20261029-02)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Failed`
- **Col M (Actual HTTP Code):** `401 / Manual Bearer only`
- **Col N (Actual Notes):** DEFECT-20261029-02: Missing Swagger OAuth2 authorizationCode scheme.


================================================================================
# CATEGORY: 2. COMMON DTO
================================================================================

---

## CDWT-DTO-08: Empty JSON Payload Body ({}) on POST

- **Category:** 2. Common DTO
- **Priority:** P0 (Blocker)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/fixed
2. In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3
3. In Request body, paste the JSON payload below
4. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{}
```

### EXPECTED RESULT:
- HTTP 400 Bad Request (Mandatory fields missing)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `400`
- **Col N (Actual Notes):** Empty payload cleanly rejected on POST.

---

## CDWT-DTO-09: shortCode Length Below Minimum Boundary (1 Char)

- **Category:** 2. Common DTO
- **Priority:** P1 (Must Work)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/fixed
2. In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3
3. In Request body, paste the JSON payload below
4. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "shortCode": "A",
  "templateName": {
    "en": "Min Code Boundary Test"
  }
}
```

### EXPECTED RESULT:
- HTTP 400 Bad Request ("shortCode length must be >= 2")

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `400`
- **Col N (Actual Notes):** shortCode < 2 characters rejected.

---

## CDWT-DTO-10: shortCode Contains Special Characters / Symbols

- **Category:** 2. Common DTO
- **Priority:** P1 (Must Work)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/fixed
2. In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3
3. In Request body, paste the JSON payload below
4. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "shortCode": "CDW@01!",
  "templateName": {
    "en": "Special Char Regex Test"
  }
}
```

### EXPECTED RESULT:
- HTTP 400 Bad Request ("Only alphanumeric characters allowed")

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `400`
- **Col N (Actual Notes):** Special characters in shortCode rejected.

---

## CDWT-DTO-11: shortCode Length at Maximum Boundary (30 Chars)

- **Category:** 2. Common DTO
- **Priority:** P0 (Blocker)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/fixed
2. In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3
3. In Request body, paste the JSON payload below
4. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "shortCode": "COMPDEF00000000000000000000001",
  "templateName": {
    "en": "Max Boundary 30 Characters"
  }
}
```

### EXPECTED RESULT:
- HTTP 200 OK (or HTTP 400 Cit.Attendance:1010 if default exists)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `200 / 400 (1010)`
- **Col N (Actual Notes):** 30-character max boundary accepted.

---

## CDWT-DTO-12: shortCode Omitted or Empty String ("")

- **Category:** 2. Common DTO
- **Priority:** P1 (Must Work)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/fixed
2. In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3
3. In Request body, paste the JSON payload below
4. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "shortCode": "",
  "templateName": {
    "en": "Auto Generated ShortCode Test"
  }
}
```

### EXPECTED RESULT:
- HTTP 200 OK (Server auto-generates CDWxxxx code)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `200`
- **Col N (Actual Notes):** Server cleanly auto-generates shortCode.

---

## CDWT-DTO-13: Attempt to Create Duplicate Company Default

- **Category:** 2. Common DTO
- **Priority:** P0 (Blocker)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`

### OPTION 1 (Swagger UI Steps):
1. Target Company 2 (which already has an active default)
2. Expand POST /api/companies/{companyId}/worktemplates/fixed
3. In Request body, paste the full JSON payload below
4. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Second CDWT Attempt"
  },
  "shortCode": "FIX999",
  "totalWorkDurationInMinutes": 2880,
  "totalWorkingDays": 6,
  "totalDaysOff": 1,
  "fixedTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```

### EXPECTED RESULT:
- HTTP 400 Cit.Attendance:1010 ("Company default already exists.")

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `400`
- **Col N (Actual Notes):** One-Default Guard enforced (Cit.Attendance:1010).

---

## CDWT-DTO-14: templateName Object Omitted or Null

- **Category:** 2. Common DTO
- **Priority:** P0 (Blocker)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/fixed
2. In Request body, paste the JSON payload below
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "shortCode": "FIX003",
  "templateName": null
}
```

### EXPECTED RESULT:
- HTTP 400 Bad Request ("Template name is required")

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `400`
- **Col N (Actual Notes):** Missing templateName rejected.

---

## CDWT-DTO-15: templateName.en Empty String ("")

- **Category:** 2. Common DTO
- **Priority:** P0 (Blocker)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/fixed
2. In Request body, paste the JSON payload below
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "shortCode": "FIX004",
  "templateName": {
    "en": ""
  }
}
```

### EXPECTED RESULT:
- HTTP 400 Bad Request ("English name cannot be empty")

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `400`
- **Col N (Actual Notes):** Empty English name rejected.

---

## CDWT-DTO-16: Bilingual Arabic UTF-8 Name Provided

- **Category:** 2. Common DTO
- **Priority:** P1 (Must Work)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/fixed
2. In Request body, paste the JSON payload below
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "shortCode": "FIX005",
  "templateName": {
    "en": "Standard Default",
    "ar": "الجدول الافتراضي للشركة"
  },
  "totalWorkDurationInMinutes": 2880,
  "totalWorkingDays": 6,
  "totalDaysOff": 1,
  "fixedTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```

### EXPECTED RESULT:
- HTTP 200 OK (Arabic text preserved byte-exact)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `200`
- **Col N (Actual Notes):** Arabic UTF-8 text persisted byte-exact.

---

## CDWT-DTO-17: tenantName Exposed in Client Request Body

- **Category:** 2. Common DTO
- **Priority:** P2 (Design Gap)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/fixed
2. In Request body, paste the JSON payload below
3. Click Execute
4. Check MongoDB Compass: Persisted as empty object {}

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "shortCode": "FIX006",
  "tenantName": {
    "en": "SpoofedClientTenant"
  },
  "templateName": {
    "en": "TenantName Exposure Test"
  }
}
```

### EXPECTED RESULT:
- Architectural Gap: tenantName should not be sent by client (DEFECT-20261026-04)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Failed`
- **Col M (Actual HTTP Code):** `200`
- **Col N (Actual Notes):** DEFECT-20261026-04: tenantName exposed in Swagger and stored as empty object in Mongo.

---

## CDWT-DTO-18: Working Days + Days Off Sum Does NOT Equal 7

- **Category:** 2. Common DTO
- **Priority:** P0 (Blocker)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/fixed
2. In Request body, paste the JSON payload below
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "shortCode": "FIX007",
  "templateName": {
    "en": "Invalid 8-Day Sum Test"
  },
  "totalWorkingDays": 6,
  "totalDaysOff": 2,
  "totalWorkDurationInMinutes": 2880,
  "fixedTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```

### EXPECTED RESULT:
- Expected: HTTP 400 Bad Request ("Sum must equal 7") | Actual DEV Bug: Throws HTTP 500 ValidationException (DEFECT-20261028-02)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Failed`
- **Col M (Actual HTTP Code):** `500`
- **Col N (Actual Notes):** DEFECT-20261028-02: Throws HTTP 500 ValidationException instead of HTTP 400.


================================================================================
# CATEGORY: 3. FIXED WT
================================================================================

---

## CDWT-DTO-19: Standard 6 Working Days + 1 Day Off Schedule

- **Category:** 3. Fixed WT
- **Priority:** P0 (Blocker)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/fixed
2. In Request body, paste the full 7-slot JSON payload below
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Standard 6 Days Working Schedule"
  },
  "shortCode": "FIX019",
  "totalWorkDurationInMinutes": 2880,
  "totalWorkingDays": 6,
  "totalDaysOff": 1,
  "fixedTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```

### EXPECTED RESULT:
- HTTP 200 OK (Creates active v1.0 Fixed CDWT)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `200`
- **Col N (Actual Notes):** Standard 6-day Fixed schedule accepted.

---

## CDWT-DTO-20: dayEnum Invalid Integer Value (e.g. 8 or 0)

- **Category:** 3. Fixed WT
- **Priority:** P0 (Blocker)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/fixed
2. In Request body, paste the JSON payload below (contains dayEnum: 8)
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Invalid DayEnum 8 Test"
  },
  "shortCode": "FIX020",
  "totalWorkDurationInMinutes": 2880,
  "totalWorkingDays": 6,
  "totalDaysOff": 1,
  "fixedTimeSlots": [
    {
      "dayEnum": 8,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```

### EXPECTED RESULT:
- Expected: HTTP 400 Bad Request | Actual DEV Bug: Throws HTTP 500 ValidationException (DEFECT-20261028-02)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Failed`
- **Col M (Actual HTTP Code):** `500`
- **Col N (Actual Notes):** DEFECT-20261028-02: Out-of-range dayEnum throws HTTP 500 crash.

---

## CDWT-DTO-21: Complete 7-Day Week Sequence (Sun=1 to Sat=7)

- **Category:** 3. Fixed WT
- **Priority:** P0 (Blocker)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/fixed
2. In Request body, paste the JSON payload below
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Full 7 Days Sequence"
  },
  "shortCode": "FIX021",
  "totalWorkDurationInMinutes": 2880,
  "totalWorkingDays": 6,
  "totalDaysOff": 1,
  "fixedTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```

### EXPECTED RESULT:
- HTTP 200 OK (All 7 days defined once)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `200`
- **Col N (Actual Notes):** Full 7-day week sequence verified.

---

## CDWT-DTO-22: Working Day Contradiction (isWorkingDay=false with Duration)

- **Category:** 3. Fixed WT
- **Priority:** P0 (Blocker)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/fixed
2. In Request body, paste the JSON payload below
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Contradiction Day 7 Off With Duration"
  },
  "shortCode": "FIX022",
  "totalWorkDurationInMinutes": 2880,
  "totalWorkingDays": 6,
  "totalDaysOff": 1,
  "fixedTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": []
    }
  ]
}
```

### EXPECTED RESULT:
- HTTP 400 Bad Request ("Off day cannot have working duration")

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `400`
- **Col N (Actual Notes):** Contradictory duration on day off rejected.

---

## CDWT-DTO-23: Empty Recurrence Array on Active Working Day

- **Category:** 3. Fixed WT
- **Priority:** P1 (Must Work)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/fixed
2. In Request body, paste the JSON payload below (Day 1 has recurrenceOfMonth: [])
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Empty Recurrence Array Test"
  },
  "shortCode": "FIX023",
  "totalWorkDurationInMinutes": 2880,
  "totalWorkingDays": 6,
  "totalDaysOff": 1,
  "fixedTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```

### EXPECTED RESULT:
- HTTP 400 Bad Request ("Active day requires at least one recurrence")

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `400`
- **Col N (Actual Notes):** Empty recurrenceOfMonth rejected.

---

## CDWT-DTO-24: Alternate Saturday Off Pattern Configuration

- **Category:** 3. Fixed WT
- **Priority:** P1 (Must Work)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/fixed
2. In Request body, paste the JSON payload below (Sat has recurrence [2, 4])
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Alternate Saturday Off Schedule"
  },
  "shortCode": "FIX024",
  "totalWorkDurationInMinutes": 2880,
  "totalWorkingDays": 6,
  "totalDaysOff": 1,
  "fixedTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        2,
        4
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    }
  ]
}
```

### EXPECTED RESULT:
- HTTP 200 OK

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `200`
- **Col N (Actual Notes):** Alternate Saturday off recurrence accepted cleanly.

---

## CDWT-DTO-25: Start >= End Time Inversion (No Overnight)

- **Category:** 3. Fixed WT
- **Priority:** P0 (Blocker)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/fixed
2. In Request body, paste the JSON payload below (Day 1 has 17:00 to 09:00)
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Inverted Timings 17:00 to 09:00"
  },
  "shortCode": "FIX025",
  "totalWorkDurationInMinutes": 2880,
  "totalWorkingDays": 6,
  "totalDaysOff": 1,
  "fixedTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "17:00",
          "endTime": "09:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```

### EXPECTED RESULT:
- HTTP 400 Bad Request ("End time must be greater than start time")

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `400`
- **Col N (Actual Notes):** Inverted start/end time rejected.

---

## CDWT-DTO-26: Total Duration Does Not Match Sum of Active Daily Slots

- **Category:** 3. Fixed WT
- **Priority:** P1 (Must Work)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/fixed
2. In Request body, paste the JSON payload below
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Math Mismatch Total 2400 but Sum 2880"
  },
  "shortCode": "FIX026",
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 6,
  "totalDaysOff": 1,
  "fixedTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```

### EXPECTED RESULT:
- HTTP 400 Bad Request ("Total duration must match sum of active daily slots")

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `400`
- **Col N (Actual Notes):** Mathematical mismatch rejected.


================================================================================
# CATEGORY: 4. FLEXIBLE WT
================================================================================

---

## CDWT-DTO-27: flexibleType Invalid Enum Value (e.g. 9 or 0)

- **Category:** 4. Flexible WT
- **Priority:** P0 (Blocker)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/flexi
2. In Request body, paste the JSON payload below (has flexibleType: 9)
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Invalid FlexiType 9"
  },
  "shortCode": "FLX027",
  "flexibleType": 9,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    }
  ]
}
```

### EXPECTED RESULT:
- Expected: HTTP 400 Bad Request | Actual DEV Bug: Throws HTTP 500 ValidationException (DEFECT-20261028-02)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Failed`
- **Col M (Actual HTTP Code):** `500`
- **Col N (Actual Notes):** DEFECT-20261028-02: Invalid flexibleType enum throws HTTP 500 crash.

---

## CDWT-DTO-28: Standard Daily Flexi Mode Configuration

- **Category:** 4. Flexible WT
- **Priority:** P0 (Blocker)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/flexi
2. In Request body, paste the JSON payload below
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Standard Daily Flexi Mode"
  },
  "shortCode": "FLX028",
  "flexibleType": 1,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    }
  ]
}
```

### EXPECTED RESULT:
- HTTP 200 OK (Creates active v1.0 Daily Flexi CDWT)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `200`
- **Col N (Actual Notes):** Standard Daily Flexi accepted.

---

## CDWT-DTO-29: Standard Weekly Pool Mode Configuration

- **Category:** 4. Flexible WT
- **Priority:** P0 (Blocker)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/flexi
2. In Request body, paste the JSON payload below
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Standard Weekly Pool Flexi Mode"
  },
  "shortCode": "FLX029",
  "flexibleType": 2,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    }
  ]
}
```

### EXPECTED RESULT:
- HTTP 200 OK (Creates active v1.0 Weekly Flexi CDWT)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `200`
- **Col N (Actual Notes):** Standard Weekly Pool accepted.

---

## CDWT-DTO-30: CRITICAL: Daily Duration Exceeding 24 Hours (1500m / 25h)

- **Category:** 4. Flexible WT
- **Priority:** P0 (Blocker)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/flexi
2. In Request body, paste the JSON payload below (Day 1 has 1500 minutes)
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "25 Hours Daily Flexi Shift"
  },
  "shortCode": "FLX030",
  "flexibleType": 1,
  "workDurationInMinutes": 1500,
  "totalWorkDurationInMinutes": 3420,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 1500
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    }
  ]
}
```

### EXPECTED RESULT:
- Expected: HTTP 400 Bad Request | Actual DEV Bug: Server returns HTTP 200 OK without validation (DEFECT-20261028-01)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Failed`
- **Col M (Actual HTTP Code):** `200`
- **Col N (Actual Notes):** DEFECT-20261028-01: Accepted 1500 min (25h/day) with HTTP 200 OK without validation.

---

## CDWT-DTO-31: Weekly Pool Exceeding 168 Hours / Week

- **Category:** 4. Flexible WT
- **Priority:** P0 (Blocker)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/flexi
2. In Request body, paste the JSON payload below (has 10500 minutes)
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Exceeding 168 Hours Weekly"
  },
  "shortCode": "FLX031",
  "flexibleType": 2,
  "totalWorkDurationInMinutes": 10500,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    }
  ]
}
```

### EXPECTED RESULT:
- HTTP 400 Bad Request ("Weekly pool cannot exceed 10080 minutes / 168 hours")

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `400`
- **Col N (Actual Notes):** Weekly pool > 168 hours cleanly rejected.

---

## CDWT-DTO-32: Active Working Day Configured with 0 Hours

- **Category:** 4. Flexible WT
- **Priority:** P1 (Must Work)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/flexi
2. In Request body, paste the JSON payload below (Day 1 is active with 0m)
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Active Day With 0 Hours"
  },
  "shortCode": "FLX032",
  "flexibleType": 1,
  "totalWorkDurationInMinutes": 1920,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    }
  ]
}
```

### EXPECTED RESULT:
- HTTP 400 Bad Request ("Active working day must have > 0 duration")

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `400`
- **Col N (Actual Notes):** 0 hours on active day rejected.

---

## CDWT-DTO-33: Negative Work Duration (< 0 Minutes)

- **Category:** 4. Flexible WT
- **Priority:** P0 (Blocker)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/flexi
2. In Request body, paste the JSON payload below
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Negative Duration Test"
  },
  "shortCode": "FLX033",
  "flexibleType": 1,
  "workDurationInMinutes": -480,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    }
  ]
}
```

### EXPECTED RESULT:
- HTTP 400 Bad Request ("Duration must be greater than 0")

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `400`
- **Col N (Actual Notes):** Negative duration rejected.

---

## CDWT-DTO-34: Weekly Mode with Non-Zero Daily Durations

- **Category:** 4. Flexible WT
- **Priority:** P1 (Must Work)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/flexi
2. In Request body, paste the JSON payload below (flexibleType 2 with daily duration)
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Weekly Mode With Non Zero Daily Slot"
  },
  "shortCode": "FLX034",
  "flexibleType": 2,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    }
  ]
}
```

### EXPECTED RESULT:
- HTTP 400 Bad Request ("Weekly pool requires daily duration = 0")

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `400`
- **Col N (Actual Notes):** Weekly mode contradiction rejected.


================================================================================
# CATEGORY: 5. SPLIT WT
================================================================================

---

## CDWT-DTO-35: Standard 2-Interval Split Shift Configuration

- **Category:** 5. Split WT
- **Priority:** P0 (Blocker)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/split
2. In Request body, paste the full 7-slot JSON payload below
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Standard 2-Interval Split Shift"
  },
  "shortCode": "SPL035",
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "splitTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```

### EXPECTED RESULT:
- HTTP 200 OK (Creates active v1.0 Split CDWT)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `200`
- **Col N (Actual Notes):** Standard 2-interval Split shift accepted.

---

## CDWT-DTO-36: Contiguous Intervals / Zero Break Gap

- **Category:** 5. Split WT
- **Priority:** P0 (Blocker)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/split
2. In Request body, paste the JSON payload below (Slot 1 ends 12:00, Slot 2 starts 12:00)
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Contiguous Zero Break Gap"
  },
  "shortCode": "SPL036",
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "splitTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "12:00",
          "endTime": "16:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```

### EXPECTED RESULT:
- Expected: HTTP 400 Bad Request | Actual DEV Bug: Throws HTTP 500 ValidationException (DEFECT-20261028-02)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Failed`
- **Col M (Actual HTTP Code):** `500`
- **Col N (Actual Notes):** DEFECT-20261028-02: Zero break gap throws HTTP 500 crash.

---

## CDWT-DTO-37: Negative Break Gap Between Intervals

- **Category:** 5. Split WT
- **Priority:** P0 (Blocker)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/split
2. In Request body, paste the JSON payload below (Interval 2 starts at 11:30)
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Negative Break Gap 11:30 before 12:00"
  },
  "shortCode": "SPL037",
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "splitTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "11:30",
          "endTime": "15:30",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```

### EXPECTED RESULT:
- Expected: HTTP 400 Bad Request | Actual DEV Bug: Throws HTTP 500 ValidationException (DEFECT-20261028-02)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Failed`
- **Col M (Actual HTTP Code):** `500`
- **Col N (Actual Notes):** DEFECT-20261028-02: Negative break gap throws HTTP 500 crash.

---

## CDWT-DTO-38: Overlapping Interval Time Ranges

- **Category:** 5. Split WT
- **Priority:** P0 (Blocker)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/split
2. In Request body, paste the JSON payload below (Intervals overlap from 12:00 to 13:00)
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "1-Hour Overlapping Intervals"
  },
  "shortCode": "SPL038",
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "splitTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "13:00",
          "workDurationInMinutes": 300
        },
        {
          "startTime": "12:00",
          "endTime": "17:00",
          "workDurationInMinutes": 300
        }
      ]
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```

### EXPECTED RESULT:
- Expected: HTTP 400 Bad Request | Actual DEV Bug: Throws HTTP 500 ValidationException (DEFECT-20261028-02)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Failed`
- **Col M (Actual HTTP Code):** `500`
- **Col N (Actual Notes):** DEFECT-20261028-02: Overlapping intervals throw HTTP 500 crash.

---

## CDWT-DTO-39: Inverted Start/End Timings in a Split Interval

- **Category:** 5. Split WT
- **Priority:** P0 (Blocker)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/split
2. In Request body, paste the JSON payload below (Slot 1 has startTime: 12:00, endTime: 08:00)
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Inverted Interval 12:00 to 08:00"
  },
  "shortCode": "SPL039",
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "splitTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "12:00",
          "endTime": "08:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```

### EXPECTED RESULT:
- Expected: HTTP 400 Bad Request | Actual DEV Bug: Server returns HTTP 200 OK without validation (DEFECT-20261028-01)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Failed`
- **Col M (Actual HTTP Code):** `200`
- **Col N (Actual Notes):** DEFECT-20261028-01: Inverted interval timings accepted with HTTP 200 OK.

---

## CDWT-DTO-40: Active Intervals Configured on a Day Off

- **Category:** 5. Split WT
- **Priority:** P0 (Blocker)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/split
2. In Request body, paste the JSON payload below (Day 7 has isWorkingDay: false with active intervals)
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Contradiction Day 7 Off With Active Intervals"
  },
  "shortCode": "SPL040",
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "splitTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    }
  ]
}
```

### EXPECTED RESULT:
- Expected: HTTP 400 Bad Request | Actual DEV Bug: Throws HTTP 500 ValidationException (DEFECT-20261028-02)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Failed`
- **Col M (Actual HTTP Code):** `500`
- **Col N (Actual Notes):** DEFECT-20261028-02: Active intervals on day off throw HTTP 500 crash.

---

## CDWT-DTO-54: Split Shift Active Day with Empty Intervals Array ([]) (POST & PATCH)

- **Category:** 5. Split WT
- **Priority:** P1 (High Functional / Crash)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/split
2. In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3
3. In Request body, paste the JSON payload below (Day 1 has isWorkingDay: true with timeSlots: [])
4. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Split Shift Empty Interval Crash Test"
  },
  "shortCode": "SPL054",
  "totalWorkDurationInMinutes": 1920,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "splitTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 480,
      "timeSlots": []
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
      ]
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
      ]
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
      ]
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```

### EXPECTED RESULT:
- Expected: HTTP 400 Bad Request ("Active working day must contain time intervals.") | Actual DEV Bug: Throws unhandled HTTP 500 crash (DEFECT-20261102-18)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Failed`
- **Col M (Actual HTTP Code):** `500`
- **Col N (Actual Notes):** DEFECT-20261102-18: Active day with empty intervals array crashes with HTTP 500 instead of HTTP 400.

---

## CDWT-DTO-55: Split Shift Half-Day Single Interval Configuration (POST & PATCH)

- **Category:** 5. Split WT
- **Priority:** P1 (High Business / Functional Gap)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/split
2. In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3
3. In Request body, paste the JSON payload below (Day 6 Saturday is a half-day with 1 continuous interval 08:00-12:00)
4. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Split Shift with Saturday Half-Day"
  },
  "shortCode": "SPL055",
  "totalWorkDurationInMinutes": 2160,
  "totalWorkingDays": 6,
  "totalDaysOff": 1,
  "splitTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
      ]
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
      ]
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
      ]
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
      ]
    },
    {
      "dayEnum": 5,
      "isWorkingDay": false,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 6,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 240,
      "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}
      ]
    },
    {
      "dayEnum": 7,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
      ]
    }
  ]
}
```

### EXPECTED RESULT:
- Expected Business Behavior: HTTP 200 OK (Half-day allowed with 1 interval) | Actual DEV Bug: HTTP 400 / 500 ("Split shift working days must contain at least 2 time intervals") (DEFECT-20261102-18)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Failed`
- **Col M (Actual HTTP Code):** `400 / 500`
- **Col N (Actual Notes):** DEFECT-20261102-18: System blocks half-day single-interval shift on Saturday in Split Template.


================================================================================
# CATEGORY: 6. PATCH & IMMUTABILITY
================================================================================

---

## CDWT-DTO-41: Empty JSON Payload Body ({}) on PATCH

- **Category:** 6. PATCH & Immutability
- **Priority:** P0 (Blocker)
- **Method & Route:** `PATCH /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{activeTemplateId}`

### OPTION 1 (Swagger UI Steps):
1. Expand PATCH /api/companies/{companyId}/worktemplates/fixed/{id}
2. In id, enter active CDWT ID: e1a64e28-ecd6-49b5-9155-fd30a11d9e8d
3. In Request body, paste: {}
4. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `PATCH`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{activeTemplateId}`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{}
```

### EXPECTED RESULT:
- Expected: HTTP 400 Bad Request ("At least one update field is required") | Actual DEV Bug: Throws HTTP 500 ValidationException (DEFECT-20261028-02)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Failed`
- **Col M (Actual HTTP Code):** `500`
- **Col N (Actual Notes):** DEFECT-20261028-02: Empty PATCH body throws HTTP 500 crash.

---

## CDWT-DTO-42: Attempt to Mutate shortCode via PATCH

- **Category:** 6. PATCH & Immutability
- **Priority:** P0 (Blocker)
- **Method & Route:** `PATCH /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{activeTemplateId}`

### OPTION 1 (Swagger UI Steps):
1. Expand PATCH /api/companies/{companyId}/worktemplates/fixed/{id}
2. In id, enter active CDWT ID: e1a64e28-ecd6-49b5-9155-fd30a11d9e8d
3. In Request body, paste: {"shortCode": "HACKCODE"}
4. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `PATCH`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{activeTemplateId}`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "shortCode": "HACKCODE"
}
```

### EXPECTED RESULT:
- HTTP 400 Cit.Attendance:1107 ("shortCode is locked and cannot be modified")

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `400`
- **Col N (Actual Notes):** shortCode immutability strictly locked (Cit.Attendance:1107).

---

## CDWT-DTO-43: Attempt to Reassign Entity to Another Company via PATCH

- **Category:** 6. PATCH & Immutability
- **Priority:** P0 (Blocker)
- **Method & Route:** `PATCH /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{activeTemplateId}`

### OPTION 1 (Swagger UI Steps):
1. Expand PATCH /api/companies/{companyId}/worktemplates/fixed/{id}
2. In Request body, paste the JSON payload below
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `PATCH`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{activeTemplateId}`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "companyId": "3a247435-e31d-ef15-8cc9-62c587f4eb3f"
}
```

### EXPECTED RESULT:
- Cross-company reassignment ignored or rejected with HTTP 400

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `400 / 200 (ignored)`
- **Col N (Actual Notes):** Cross-company transfer locked.

---

## CDWT-DTO-44: Attempt to Spoof tenantName via PATCH

- **Category:** 6. PATCH & Immutability
- **Priority:** P2 (Design Gap)
- **Method & Route:** `PATCH /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{activeTemplateId}`

### OPTION 1 (Swagger UI Steps):
1. Expand PATCH /api/companies/{companyId}/worktemplates/fixed/{id}
2. In Request body, paste the JSON payload below
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `PATCH`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{activeTemplateId}`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "tenantName": {
    "en": "SpoofedTenantName"
  }
}
```

### EXPECTED RESULT:
- Server should ignore or reject client tenantName (DEFECT-20261026-04)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Failed`
- **Col M (Actual HTTP Code):** `200`
- **Col N (Actual Notes):** DEFECT-20261026-04: tenantName accepted in PATCH body.

---

## CDWT-DTO-45: Attempt to Edit an Archived / Superseded Version ID

- **Category:** 6. PATCH & Immutability
- **Priority:** P1 (Must Work)
- **Method & Route:** `PATCH /api/companies/3a247436-8669-844a-7d2f-1a209af02d8e/worktemplates/flexi/a31a2f5e-bc53-4221-b2d2-ff8c5ed54dbb`

### OPTION 1 (Swagger UI Steps):
1. Target Company 4 archived v1.0 ID: a31a2f5e-bc53-4221-b2d2-ff8c5ed54dbb
2. Expand PATCH /api/companies/{companyId}/worktemplates/flexi/{id}
3. In Request body, paste the JSON payload below
4. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `PATCH`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247436-8669-844a-7d2f-1a209af02d8e/worktemplates/flexi/a31a2f5e-bc53-4221-b2d2-ff8c5ed54dbb`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Attempt Edit Archived Version v1.0"
  }
}
```

### EXPECTED RESULT:
- HTTP 400 Cit.Attendance:1107 ("Archived template cannot be edited")

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `400`
- **Col N (Actual Notes):** Archived versions protected from edits (Cit.Attendance:1107).

---

## CDWT-DTO-46: Attempt to Edit a Non-Existent Template GUID

- **Category:** 6. PATCH & Immutability
- **Priority:** P1 (Must Work)
- **Method & Route:** `PATCH /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/ffffffff-ffff-ffff-ffff-ffffffffffff`

### OPTION 1 (Swagger UI Steps):
1. In id, enter fake GUID: ffffffff-ffff-ffff-ffff-ffffffffffff
2. Expand PATCH /api/companies/{companyId}/worktemplates/fixed/{id}
3. In Request body, paste the JSON payload below
4. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `PATCH`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/ffffffff-ffff-ffff-ffff-ffffffffffff`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Edit Non Existent Entity"
  }
}
```

### EXPECTED RESULT:
- HTTP 400 Cit.Attendance:1101 ("Template not found")

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `400`
- **Col N (Actual Notes):** Non-existent template returns Cit.Attendance:1101.

---

## CDWT-DTO-47: Valid In-Place Timing Shift on Thursday

- **Category:** 6. PATCH & Immutability
- **Priority:** P0 (Blocker)
- **Method & Route:** `PATCH /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{activeTemplateId}`

### OPTION 1 (Swagger UI Steps):
1. In id, enter active Fixed CDWT ID
2. In Request body, paste the JSON payload below (Thursday shift changed to 09:00-17:00)
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `PATCH`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{activeTemplateId}`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Shift Timing Updated to 09:00 Thursday"
  },
  "totalWorkDurationInMinutes": 2880,
  "totalWorkingDays": 6,
  "totalDaysOff": 1,
  "fixedTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "09:00",
          "endTime": "17:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "16:00",
          "workDurationInMinutes": 480
        }
      ]
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```

### EXPECTED RESULT:
- HTTP 200 OK (Creates active v2.0, archives v1.0)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `200`
- **Col N (Actual Notes):** In-place edit creates next version and archives previous.

---

## CDWT-DTO-48: Migrate Company Default from Fixed to Flexible Daily

- **Category:** 6. PATCH & Immutability
- **Priority:** P0 (Blocker)
- **Method & Route:** `PATCH /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{activeFixedId}`

### OPTION 1 (Swagger UI Steps):
1. In id, enter active Fixed CDWT ID
2. In Request body, paste the Flexible Daily migration JSON below
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `PATCH`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{activeFixedId}`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Migrated to Flexible Daily CDWT"
  },
  "flexibleType": 1,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    }
  ]
}
```

### EXPECTED RESULT:
- HTTP 200 OK (Creates active v2.0 Flexi CDWT)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `200`
- **Col N (Actual Notes):** Fixed to Flexi migration accepted.

---

## CDWT-DTO-49: Migrate Company Default from Fixed to Split Shift

- **Category:** 6. PATCH & Immutability
- **Priority:** P0 (Blocker)
- **Method & Route:** `PATCH /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{activeFixedId}`

### OPTION 1 (Swagger UI Steps):
1. In id, enter active Fixed CDWT ID
2. In Request body, paste the Split Shift migration JSON below
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `PATCH`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{activeFixedId}`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Migrated to Split Shift CDWT"
  },
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "splitTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00",
          "endTime": "12:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "16:00",
          "endTime": "20:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```

### EXPECTED RESULT:
- HTTP 200 OK (Creates active v2.0 Split CDWT)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `200`
- **Col N (Actual Notes):** Fixed to Split migration accepted.

---

## CDWT-DTO-50: Attempt to Migrate Company Default to Roster / Rotation

- **Category:** 6. PATCH & Immutability
- **Priority:** P1 (Must Work)
- **Method & Route:** `PATCH /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{activeFixedId}`

### OPTION 1 (Swagger UI Steps):
1. In id, enter active Fixed CDWT ID
2. In Request body, paste the JSON payload below
3. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `PATCH`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed/{activeFixedId}`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Attempt Migrate to Roster CDWT"
  },
  "templateType": "Roster",
  "rosterSlots": [
    {
      "cycleDays": 14,
      "shifts": []
    }
  ]
}
```

### EXPECTED RESULT:
- HTTP 400 Bad Request (CDWT is restricted to Fixed, Flexi, Split)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Pass`
- **Col M (Actual HTTP Code):** `400`
- **Col N (Actual Notes):** CDWT restricted to Fixed, Flexi, Split.

---

## CDWT-DTO-51: Attempt to Archive Active Company Default Work Template

- **Category:** 6. PATCH & Immutability
- **Priority:** P1 (Must Work)
- **Method & Route:** `PATCH /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/{activeTemplateId}/archive`

### OPTION 1 (Swagger UI Steps):
1. Expand PATCH /api/companies/{companyId}/worktemplates/{activeId}/archive
2. In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3
3. In activeId, enter active CDWT ID: e1a64e28-ecd6-49b5-9155-fd30a11d9e8d
4. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `PATCH`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/{activeTemplateId}/archive`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
  `None (Query / Route Parameter only)`

### EXPECTED RESULT:
- Expected: HTTP 400 Cit.Attendance:1202 | Actual DEV Bug: Server returns HTTP 200 OK without guard (DEFECT-20261028-03)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Failed`
- **Col M (Actual HTTP Code):** `200`
- **Col N (Actual Notes):** DEFECT-20261028-03: Active default archived without guard.

---

## CDWT-DTO-52: Attempt to Soft-Delete Active Company Default Work Template

- **Category:** 6. PATCH & Immutability
- **Priority:** P1 (Must Work)
- **Method & Route:** `PATCH /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/{activeTemplateId}/delete`

### OPTION 1 (Swagger UI Steps):
1. Expand PATCH /api/companies/{companyId}/worktemplates/{activeId}/delete
2. In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3
3. In activeId, enter active CDWT ID: e1a64e28-ecd6-49b5-9155-fd30a11d9e8d
4. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `PATCH`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/{activeTemplateId}/delete`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
  `None (Query / Route Parameter only)`

### EXPECTED RESULT:
- Expected: HTTP 400 Cit.Attendance:1202 | Actual DEV Bug: Server returns HTTP 200 OK without guard (DEFECT-20261028-03)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Failed`
- **Col M (Actual HTTP Code):** `200`
- **Col N (Actual Notes):** DEFECT-20261028-03: Active default soft-deleted without guard.

---

================================================================================
# END OF PLAYBOOK — ALL 53 TEST CASES WITH FULL REQUEST BODY PAYLOADS
================================================================================
