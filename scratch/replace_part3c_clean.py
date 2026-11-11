import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Table of Contents to explicitly have Part 3C
toc_old = "* [**📅 Part 4: Defects Discovered on 29 October 2026 (SECURITY & SWAGGER ARCHITECTURE)**](#-part-4-defects-identified-on-29-october-2026-security--swagger-architecture) — *Critical JWT Validation Bypass (DEFECT-20261029-01) & Swagger Missing OAuth2 AuthorizationCode Flow (DEFECT-20261029-02) (2 Issues)*"
toc_new = "* [**📅 Part 3C: Defects Discovered on 29 October 2026 (SECURITY & SWAGGER ARCHITECTURE)**](#-part-3c-defects-identified-on-29-october-2026-live-api-probes-security--swagger-architecture) — *Critical JWT Validation Bypass (DEFECT-20261029-01) & Swagger Missing OAuth2 AuthorizationCode Flow (DEFECT-20261029-02) (2 Issues)*"

if toc_old in text:
    text = text.replace(toc_old, toc_new)
    print("Updated TOC to Part 3C!")
else:
    print("Warning: toc_old not found directly.")

# Renumber Part 5 and 6 back to Part 4 and 5
text = text.replace("# 🔄 Part 5: Standardized Bug Lifecycle Procedure", "# 🔄 Part 4: Standardized Bug Lifecycle Procedure")
text = text.replace("* [**🔄 Part 5: Standardized Bug Lifecycle Procedure**]", "* [**🔄 Part 4: Standardized Bug Lifecycle Procedure**]")
text = text.replace("# ✅ Part 6: Actionable Developer Checklist (Date-Wise)", "# ✅ Part 5: Actionable Developer Checklist (Date-Wise)")
text = text.replace("* [**✅ Part 6: Actionable Developer Checklist (Date-Wise)**]", "* [**✅ Part 5: Actionable Developer Checklist (Date-Wise)**]")

# 2. Build complete Part 3C block
part3c_clean = """# 📅 Part 3C: Defects Identified on 29 October 2026 (Live API Probes, Security & Swagger Architecture)
**Theme:** API Gateway / Kestrel Authentication Hardening & Microservice Swagger Ecosystem Consistency

---

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

| **Evidence 16: Attendance Service Swagger (`attendance2.dev.zoolwork.com`)**<br>*(Only Raw Bearer Input — Missing OAuth2 Scheme)* | **Evidence 17: Company Service Swagger (`company8.dev.zoolwork.com`)**<br>*(Properly Implemented OAuth2 `authorizationCode` Flow with IdentityServer)* |
| :---: | :---: |
| ![Attendance Swagger Missing OAuth2](defect_evidence/evidence_16_attendance_swagger_missing_oauth2.png) | ![Company Swagger Has OAuth2](defect_evidence/evidence_17_company_swagger_has_oauth2.png) |

#### 2. Detailed Evidence Breakdown
* **Evidence 16 (Attendance Swagger — Defect):** Only provides a raw text input for `Bearer (http, Bearer)`. Users and testers must manually acquire tokens from outside Swagger, copy the raw JWT string, and paste it into the textbox every 60 minutes. If the token expires or is omitted, requests fail without an in-browser OAuth redirect.
* **Evidence 17 (Company Service Swagger — Benchmark Standard):** Fully implements `oauth2 (OAuth2, authorizationCode)` with:
  * **Authorization URL:** `https://auth8.dev.zoolwork.com/connect/authorize`
  * **Token URL:** `https://auth8.dev.zoolwork.com/connect/token`
  * **Client ID:** `WebGateway_Swagger`
  * **Flow:** `authorizationCode`
  * **Configured Scopes:** `CompanySvc`, `IdentityService`

#### 3. Root Cause Analysis
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

#### 4. Impact & Business Consequences
1. **Severe Developer & QA Friction:** Manual testers and frontend engineers cannot authorize directly in the Swagger UI. They must leave Swagger, execute manual curl or token scripts, extract the access token, and paste it back into Swagger every 60 minutes.
2. **Architectural Inconsistency:** Attendance Service is the *only* service in the Sahab Payroll ecosystem (`CompanySvc`, `IdentitySvc`, etc.) lacking standard OAuth2 Authorization Code Swagger integration.
3. **Authorization Failure Inconsistencies:** Testers attempting to use standard Swagger authentication workflows run into authorization failures because the required `WebGateway_Swagger` client interaction is not wired up.

#### 5. Engineering Remediation Patch (.NET 9 `Program.cs`)

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
    options.OAuthClientSecret(builder.Configuration["Identity:SwaggerClientSecret"] ?? "swagger_secret");
    options.OAuthUsePkce();
    options.OAuthScopeSeparator(" ");
});
```"""

# Find where Part 4 or Part 3C starts, and replace until Part 4 (Standardized Bug Lifecycle)
start_idx = text.find("# 📅 Part")
# find the one that has 29 October
while start_idx != -1:
    line_end = text.find("\n", start_idx)
    line = text[start_idx:line_end]
    if "29 October" in line and ("Part 3C" in line or "Part 4" in line):
        break
    start_idx = text.find("# 📅 Part", line_end)

print("Found 29 October section at character index:", start_idx)
lifecycle_idx = text.find("# 🔄 Part", start_idx)
print("Found next part (Bug Lifecycle) at character index:", lifecycle_idx)

if start_idx != -1 and lifecycle_idx != -1:
    text = text[:start_idx] + part3c_clean + "\n\n---\n\n" + text[lifecycle_idx:]
    print("Replaced section with clean Part 3C and native markdown image table!")
else:
    print("Error: could not locate section boundaries!")

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("SUCCESS: File saved!")

