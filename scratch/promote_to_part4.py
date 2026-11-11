import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Part 3C heading to Part 4
text = text.replace(
    "# 📅 Part 3C: Defects Identified on 29 October 2026 (Security & Swagger Architecture)",
    "# 📅 Part 4: Defects Identified on 29 October 2026 (Security & Swagger Architecture)"
)

# 2. Update TOC references
text = text.replace(
    "* [**📅 Part 3C: Defects Discovered on 29 October 2026 (SECURITY & SWAGGER ARCHITECTURE)**](#-part-3c-defects-identified-on-29-october-2026-security--swagger-architecture)",
    "* [**📅 Part 4: Defects Discovered on 29 October 2026 (SECURITY & SWAGGER ARCHITECTURE)**](#-part-4-defects-identified-on-29-october-2026-security--swagger-architecture)"
)
text = text.replace(
    "# 🔄 Part 4: Standardized Bug Lifecycle Procedure",
    "# 🔄 Part 5: Standardized Bug Lifecycle Procedure"
)
text = text.replace(
    "* [**🔄 Part 4: Standardized Bug Lifecycle Procedure**]",
    "* [**🔄 Part 5: Standardized Bug Lifecycle Procedure**]"
)
text = text.replace(
    "# ✅ Part 5: Actionable Developer Checklist (Date-Wise)",
    "# ✅ Part 6: Actionable Developer Checklist (Date-Wise)"
)
text = text.replace(
    "* [**✅ Part 5: Actionable Developer Checklist (Date-Wise)**]",
    "* [**✅ Part 6: Actionable Developer Checklist (Date-Wise)**]"
)

# 3. Add 29-Oct defects row into Part 3 matrix as well (at line ~900)
part3_matrix_end = "| **`DEFECT-20261028-07`**<br>(`USER-134`, `USER-135`) | **P2 (Major)** | `POST /policies/grace`<br>`POST /policies/break` | Negative Grace (-15m) & Negative Break (-60m) accepted with **HTTP 200 OK** and created in MongoDB | Reject with HTTP 400 (`GraceMinutes >= 0`, `DurationMinutes > 0`) | 🔴 **Open** |"

part3_additions = """| **`DEFECT-20261028-07`**<br>(`USER-134`, `USER-135`) | **P2 (Major)** | `POST /policies/grace`<br>`POST /policies/break` | Negative Grace (-15m) & Negative Break (-60m) accepted with **HTTP 200 OK** and created in MongoDB | Reject with HTTP 400 (`GraceMinutes >= 0`, `DurationMinutes > 0`) | 🔴 **Open** |
| **`DEFECT-20261029-01`**<br>*(Added 29-Oct)* | **P0 (Blocker / Security)** | All Auth Routes (`/api/companies/*`) | **Critical Security Bypass:** Server accepts expired tokens (10d past exp) and forged signatures (`AAAA...`), returning **HTTP 200 OK** | Reject with HTTP 401 (`ValidateLifetime=true`, `ValidateIssuerSigningKey=true`) | 🚨 **CRITICAL OPEN** |
| **`DEFECT-20261029-02`**<br>*(Added 29-Oct)* | **P1 (High Architecture / DX)** | Swagger UI (`/swagger/index.html`) | **Swagger Missing OAuth2 (`authorizationCode`) Flow:** Unlike `SP.CompanySvc` using `WebGateway_Swagger`, Attendance Swagger only has raw `Bearer`, causing auth failures | Implement OAuth2 Authorization Code flow in `Program.cs` SwaggerGen | ❌ **OPEN (DEV PATCH PROVIDED)** |"""

if part3_matrix_end in text:
    text = text.replace(part3_matrix_end, part3_additions)
    print("Added 29-Oct defects into Part 3 matrix successfully!")
else:
    print("Warning: part3_matrix_end not matched.")

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("SUCCESS: Part 4 promoted and synchronized in Report!")

