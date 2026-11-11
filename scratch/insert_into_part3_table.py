import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

target_line = '| **`DEFECT-20261028-07`**<br>(`USER-134`, `USER-135`) | **P1 (Boundary)** | `POST /attpolicies/grace`<br>`POST /attpolicies/break` | Negative values (`-15` grace minutes, `-60` break minutes) accepted with **HTTP 200 OK** | Reject with HTTP 400 (`GracePeriod >= 0`, `BreakDuration > 0`) | 🔴 **FAIL / OPEN**<br>*(Verified on DEV)* |\n'

new_rows = target_line + """| **`DEFECT-20261029-01`**<br>*(Added 29-Oct)* | **P0 (Critical Security)** | All Auth APIs (`/api/companies/*`) | **Critical JWT Validation Bypass:** Server accepts expired tokens (10d past exp) and forged signatures (`AAAA...`), returning **HTTP 200 OK** | Reject with HTTP 401 (`ValidateLifetime=true`, `ValidateIssuerSigningKey=true`) | 🚨 **CRITICAL OPEN** |
| **`DEFECT-20261029-02`**<br>*(Added 29-Oct)* | **P1 (High Architecture / DX)** | Swagger UI (`/swagger/index.html`) | **Swagger Missing OAuth2 (`authorizationCode`) Flow:** Unlike `SP.CompanySvc` using `WebGateway_Swagger`, Attendance Swagger only has raw `Bearer`, causing auth failures | Implement OAuth2 Authorization Code flow in `Program.cs` SwaggerGen | ❌ **OPEN (DEV PATCH PROVIDED)** |
"""

if target_line in text:
    text = text.replace(target_line, new_rows)
    print("Added 29-Oct defects to Part 3 table successfully!")
else:
    print("Error: target_line not matched!")

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("SUCCESS: Updated report!")

