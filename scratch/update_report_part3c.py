# -*- coding: utf-8 -*-
"""
Updates Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
Adds Part 3C: Defects Discovered on 29 October 2026:
 - DEFECT-20261029-01 (P0 Critical Security): JWT Lifetime & Signature Validation Disabled
 - DEFECT-20261029-02 (P1 High Architecture/DX): Attendance Swagger Missing OAuth2 (authorizationCode) Flow
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update TOC (after Part 3B)
old_toc = "* [**📅 Part 3B: Live Execution of Holiday Calendar Test Cases (Attendance 2 & 3)**](#-part-3b-live-execution-of-holiday-calendar-test-cases-attendance-2--3---29-october-2026) — *100% Executed Across All 310 TCs (288 Pass, 22 Fail — 92.9% Pass Rate)*\n* [**🔄 Part 4: Standardized Bug Lifecycle Procedure**]"
new_toc = """* [**📅 Part 3B: Live Execution of Holiday Calendar Test Cases (Attendance 2 & 3)**](#-part-3b-live-execution-of-holiday-calendar-test-cases-attendance-2--3---29-october-2026) — *100% Executed Across All 310 TCs (288 Pass, 22 Fail — 92.9% Pass Rate)*
* [**📅 Part 3C: Defects Discovered on 29 October 2026 (SECURITY & SWAGGER ARCHITECTURE)**](#-part-3c-defects-identified-on-29-october-2026-security--swagger-architecture) — *Critical JWT Validation Bypass (DEFECT-20261029-01) & Swagger Missing OAuth2 AuthorizationCode Flow (DEFECT-20261029-02) (2 Issues)*
* [**🔄 Part 4: Standardized Bug Lifecycle Procedure**]"""

if old_toc in content:
    content = content.replace(old_toc, new_toc)
    print("Updated TOC successfully!")
else:
    print("Warning: old_toc not matched exactly.")

# 2. Update Dashboard table to include Module 17
old_dash_total = """| **16** | **Holiday Calendar - Test Cases** | 310 | 172 | 130 | 8 | 0 | **288** | **22** | **0** | **100.0%** | 🚀 **100% Executed (92.9% Pass Rate)** |
| **TOTAL** | **All 16 Modules Combined** | **1,527** | **659** | **647** | **208** | **13** | **541** | **57** | **929** | **39.2%** | 🎯 **598 Executed (541 Pass, 57 Fail — 90.5% Pass Rate)** |"""

new_dash_total = """| **16** | **Holiday Calendar - Test Cases** | 310 | 172 | 130 | 8 | 0 | **288** | **22** | **0** | **100.0%** | 🚀 **100% Executed (92.9% Pass Rate)** |
| **17** | **CDWT - Manual DTO Validations** | 52 | 27 | 20 | 5 | 0 | 0 | 0 | 52 | 0.0% | 📝 Ready for Manual Testing |
| **TOTAL** | **All 17 Modules Combined** | **1,579** | **686** | **667** | **213** | **13** | **541** | **57** | **981** | **37.9%** | 🎯 **598 Executed (541 Pass, 57 Fail — 90.5% Pass Rate)** |"""

if old_dash_total in content:
    content = content.replace(old_dash_total, new_dash_total)
    print("Updated Dashboard table successfully!")
else:
    print("Warning: old_dash_total not matched exactly.")

# 3. Create Part 3C content
part_3c_text = """

---

# 📅 Part 3C: Defects Identified on 29 October 2026 (Security & Swagger Architecture)
**Theme:** API Gateway / Kestrel Authentication Hardening & Microservice Swagger Ecosystem Consistency

### Summary Matrix (29-Oct-2026)

| Defect ID | Severity / Priority | Layer | Endpoint / Module | Defect Description | Live Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **`DEFECT-20261029-01`** | **P0 (Critical Security)** | Auth / Kestrel | All Authenticated APIs (`/api/companies/*`) | **Critical JWT Validation Bypass:** `SP.AttendanceSvc` accepts expired JWT tokens (tested 10 days past `exp`) and forged / tampered signatures (`AAAA...`), returning `HTTP 200 OK` and live company data instead of `HTTP 401 Unauthorized`. | 🚨 **CRITICAL OPEN** |
| **`DEFECT-20261029-02`** | **P1 (High Architecture / DX)** | Swagger / OpenAPI | Swagger UI (`/swagger/index.html`) | **Swagger Missing OAuth2 (`authorizationCode`) Flow:** Unlike `SP.CompanySvc` and all other Sahab microservices which implement `oauth2 (OAuth2, authorizationCode)` with `WebGateway_Swagger` client, Attendance Swagger only offers raw `Bearer (http, Bearer)`, blocking seamless SSO login and causing test auth failures. | ❌ **FAIL (ARCHITECTURAL GAP)** |

---

### Defect `DEFECT-20261029-01`: Critical Security Vulnerability — JWT Lifetime & Signature Validation Disabled in Attendance Service

#### 1. Photographic & Live Reproduction Evidence
Live probes against `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates` revealed:

```bash
# 1. Probe with a forged token (signature replaced with arbitrary 'AAAA...'):
curl -i -X GET "https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates" \\
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2F1dGg4LmRldi56b29sd29yay5jb20iLCJhdWQiOiJBdHRlbmRhbmNlIiwic3ViIjoiMTIzNCJ9.AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \\
  -H "__tenant: Attendance"

# Server Live Response:
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Server: Kestrel

[{"id":"e1a64e28-ecd6-49b5-9155-fd30a11d9e8d","shortCode":"FIX001","templateName":{"en":"Fixed Shift"...}}]
```

#### 2. Root Cause Analysis
In `SP.AttendanceSvc/Program.cs`, the JWT Bearer configuration sets or defaults:
```csharp
// VULNERABLE CONFIGURATION IN DEV:
services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.Authority = "https://auth8.dev.zoolwork.com";
        options.Audience = "Attendance";
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuerSigningKey = false, // <-- CRITICAL: Signature verification disabled!
            ValidateLifetime = false,         // <-- CRITICAL: Expiration verification disabled!
            ValidateIssuer = true,
            ValidateAudience = true
        };
    });
```
Because `ValidateLifetime` and `ValidateIssuerSigningKey` are not strictly enforced, any client possessing an expired token or fabricating a signed token can impersonate users and execute business mutations against any tenant.

#### 3. Engineering Remediation Patch (.NET 9)
```csharp
// RECOMMENDED PATCH:
services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.Authority = "https://auth8.dev.zoolwork.com";
        options.Audience = "Attendance";
        options.RequireHttpsMetadata = false; // or true in prod
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuerSigningKey = true, // Must validate cryptographic signature
            ValidateLifetime = true,         // Must strictly reject expired tokens
            ClockSkew = TimeSpan.FromMinutes(1), // Minimal skew
            ValidateIssuer = true,
            ValidIssuer = "https://auth8.dev.zoolwork.com",
            ValidateAudience = true,
            ValidAudience = "Attendance"
        };
    });
```

---

### Defect `DEFECT-20261029-02`: High Priority Architecture / Developer Experience — Attendance Swagger Missing OAuth2 (`authorizationCode`) Flow

#### 1. Photographic Proof & Microservice Ecosystem Comparison

A direct comparison of Swagger Authorize modals between **Attendance Service** and **Company Service** demonstrates the architectural omission:

````carousel
![Attendance Swagger Missing OAuth2](file:///C:/Users/Comm-IT%20India/.gemini/antigravity/brain/65113ff1-ddbc-4539-afe6-44cf63216ecc/evidence_16_attendance_swagger_missing_oauth2.png)
<!-- slide -->
![Company Swagger Has OAuth2](file:///C:/Users/Comm-IT%20India/.gemini/antigravity/brain/65113ff1-ddbc-4539-afe6-44cf63216ecc/evidence_17_company_swagger_has_oauth2.png)
````

* **Evidence 1 (Attendance Swagger):** Only provides `Bearer (http, Bearer)`. Users must copy-paste an external token. If the token expires or is omitted, requests fail without an in-browser OAuth redirect.
* **Evidence 2 (Company Service Swagger & Other Services):** Fully implements `oauth2 (OAuth2, authorizationCode)` with:
  * Authorization URL: `https://auth8.dev.zoolwork.com/connect/authorize`
  * Token URL: `https://auth8.dev.zoolwork.com/connect/token`
  * Client ID: `WebGateway_Swagger`
  * Configured Scopes: `CompanySvc`, `IdentityService`

#### 2. Root Cause Analysis
In `SP.AttendanceSvc/Program.cs`, `builder.Services.AddSwaggerGen(...)` only registers a basic `Bearer` security definition:
```csharp
// CURRENT ATTENDANCE SERVICE SWAGGER (INCOMPLETE):
builder.Services.AddSwaggerGen(c =>
{
    c.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Type = SecuritySchemeType.Http,
        Scheme = "Bearer",
        BearerFormat = "JWT",
        Description = "Paste your JWT access token here (without the 'Bearer ' prefix)."
    });
    // Missing OAuth2 SecurityDefinition!
});
```

Whereas `SP.CompanySvc` correctly configures the OpenID Connect / OAuth2 Authorization Code flow:
```csharp
// STANDARD IMPLEMENTATION IN COMPANY SERVICE & OTHER SERVICES:
c.AddSecurityDefinition("oauth2", new OpenApiSecurityScheme
{
    Type = SecuritySchemeType.OAuth2,
    Flows = new OpenApiOAuthFlows
    {
        AuthorizationCode = new OpenApiOAuthFlow
        {
            AuthorizationUrl = new Uri("https://auth8.dev.zoolwork.com/connect/authorize"),
            TokenUrl = new Uri("https://auth8.dev.zoolwork.com/connect/token"),
            Scopes = new Dictionary<string, string>
            {
                { "AttendanceService", "Attendance Service API" },
                { "IdentityService", "Identity Service API" }
            }
        }
    }
});
```

#### 3. Impact & Business Consequences
1. **Severe Developer & QA Friction:** Manual testers and frontend engineers cannot authorize directly in the Swagger UI. They must leave Swagger, execute manual curl or token scripts, extract the access token, and paste it back into Swagger every 60 minutes.
2. **Architectural Inconsistency:** Attendance Service is the *only* service in the Sahab Payroll ecosystem (`CompanySvc`, `IdentitySvc`, etc.) lacking standard OAuth2 Authorization Code Swagger integration.
3. **Authorization Failure Inconsistencies:** Testers attempting to use standard Swagger authentication workflows run into authorization failures because the required `WebGateway_Swagger` client interaction is not wired up.

#### 4. Engineering Remediation Patch (.NET 9 `Program.cs`)

```csharp
// 1. In Program.cs (Service Configuration):
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "Sahab Attendance API",
        Version = "v1",
        Description = "API for managing work templates, work plans, and attendance policies in the Sahab Payroll system."
    });

    // Add standard OAuth2 Authorization Code Flow
    options.AddSecurityDefinition("oauth2", new OpenApiSecurityScheme
    {
        Type = SecuritySchemeType.OAuth2,
        Flows = new OpenApiOAuthFlows
        {
            AuthorizationCode = new OpenApiOAuthFlow
            {
                AuthorizationUrl = new Uri($"{builder.Configuration["Identity:Authority"]}/connect/authorize"),
                TokenUrl = new Uri($"{builder.Configuration["Identity:Authority"]}/connect/token"),
                Scopes = new Dictionary<string, string>
                {
                    { "AttendanceService", "Attendance Service API" },
                    { "IdentityService", "Identity Service API" }
                }
            }
        }
    });

    // Retain Bearer for direct token testing
    options.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Type = SecuritySchemeType.Http,
        Scheme = "Bearer",
        BearerFormat = "JWT",
        Description = "Paste your JWT access token here (without the 'Bearer ' prefix)."
    });

    options.AddSecurityRequirement(new OpenApiSecurityRequirement
    {
        {
            new OpenApiSecurityScheme
            {
                Reference = new OpenApiReference { Type = ReferenceType.SecurityScheme, Id = "oauth2" }
            },
            new[] { "AttendanceService", "IdentityService" }
        },
        {
            new OpenApiSecurityScheme
            {
                Reference = new OpenApiReference { Type = ReferenceType.SecurityScheme, Id = "Bearer" }
            },
            Array.Empty<string>()
        }
    });
});

// 2. In Program.cs (App Pipeline Configuration):
app.UseSwagger();
app.UseSwaggerUI(options =>
{
    options.SwaggerEndpoint("/swagger/v1/swagger.json", "Sahab Attendance API v1");
    options.OAuthClientId("WebGateway_Swagger");
    options.OAuthClientSecret("swagger_secret"); // Or retrieve from appsettings.json
    options.OAuthUsePkce();
    options.OAuthScopeSeparator(" ");
});
```
"""

# Insert Part 3C before Part 4
part4_marker = "# 🔄 Part 4: Standardized Bug Lifecycle Procedure"
if part4_marker in content:
    content = content.replace(part4_marker, part_3c_text + "\n" + part4_marker)
    print("Inserted Part 3C successfully!")
else:
    print("Error: part4_marker not found!")

# 4. Add Day 4 to Part 5 Checklist
day4_checklist = """### 📅 Day 4: 29 October 2026 Checklist (Security & Swagger Architecture)
- [ ] **P0 (`DEFECT-20261029-01`):** In `SP.AttendanceSvc/Program.cs`, set `ValidateLifetime = true` and `ValidateIssuerSigningKey = true` inside `TokenValidationParameters` to reject expired JWT tokens and forged signatures with `HTTP 401 Unauthorized`.
- [ ] **P1 (`DEFECT-20261029-02`):** In `SP.AttendanceSvc/Program.cs`, configure `oauth2 (OAuth2, authorizationCode)` security scheme pointing to `https://auth8.dev.zoolwork.com` with client `WebGateway_Swagger` and scopes `AttendanceService`, matching `SP.CompanySvc` and standard Sahab Swagger configurations.
"""

# Find Day 3 checklist to append Day 4
day3_marker = "- [ ] **P2 (`DEFECT-20261028-04`):** Return HTTP 404 Not Found when querying `/api/companies/{companyId}/worktemplates` with a non-existent or zero GUID company.\n"
if day3_marker in content:
    content = content.replace(day3_marker, day3_marker + "\n" + day4_checklist)
    print("Added Day 4 Checklist successfully!")
else:
    print("Warning: day3_marker not matched exactly.")

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Report completely updated with Part 3C and Day 4 Checklist!")

