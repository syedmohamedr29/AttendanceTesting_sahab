import sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. Update Markdown Report
with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace line 10
old_date_line = "> **Report Last Updated:** 28 October 2026"
new_date_line = "> **Report Last Updated:** 29 October 2026 (Updated with Today's P0 Security & P1 Swagger Defects)"

if old_date_line in text:
    text = text.replace(old_date_line, new_date_line)
    print("Updated report date to 29 October 2026!")

# Add Prominent Top Banner right after TOC
toc_end_marker = "* [**✅ Part 5: Actionable Developer Checklist (Date-Wise)**](#-part-5-actionable-developer-checklist-date-wise) — *Consolidated Engineering Action Items for Khalid's Team*\n\n---"

top_banner = """* [**✅ Part 5: Actionable Developer Checklist (Date-Wise)**](#-part-5-actionable-developer-checklist-date-wise) — *Consolidated Engineering Action Items for Khalid's Team*

---

## 🚨 Critical & High-Priority Defects Logged Today (29 October 2026)

> [!WARNING]
> The following high-severity defects were uncovered and cataloged on **29 October 2026**. Full reproduction steps, photographic proofs, root causes, and C# code patches are detailed in [**Part 3C**](#-part-3c-defects-identified-on-29-october-2026-security--swagger-architecture) and [**Part 5 Developer Checklist**](#-part-5-actionable-developer-checklist-date-wise).

| Defect ID | Severity / Priority | Layer | Endpoint / Module | Defect Description | Live Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **`DEFECT-20261029-01`** | **P0 (Critical Security)** | Auth / Kestrel | All Authenticated APIs (`/api/companies/*`) | **Critical JWT Validation Bypass:** `SP.AttendanceSvc` accepts expired JWT tokens (tested 10 days past `exp`) and forged signatures (`AAAA...`), returning `HTTP 200 OK` and company data instead of `HTTP 401 Unauthorized`. | 🚨 **CRITICAL OPEN** |
| **`DEFECT-20261029-02`** | **P1 (High Architecture / DX)** | Swagger / OpenAPI | Swagger UI (`/swagger/index.html`) | **Swagger Missing OAuth2 (`authorizationCode`) Flow:** Unlike `SP.CompanySvc` which uses `WebGateway_Swagger` client with IdentityServer (`https://auth8.dev.zoolwork.com`), Attendance Swagger only offers raw `Bearer (http, Bearer)`, blocking seamless SSO login and causing test auth failures. | ❌ **OPEN (DEV PATCH PROVIDED)** |

📸 **Side-by-Side Photographic Evidence:** See the side-by-side comparison between Attendance Swagger and Company Swagger in [**Section DEFECT-20261029-02**](#defect-defect-20261029-02-high-priority-architecture--developer-experience--attendance-swagger-missing-oauth2-authorizationcode-flow).

---"""

if toc_end_marker in text:
    text = text.replace(toc_end_marker, top_banner)
    print("Added top banner for 29 October 2026 defects!")

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("SUCCESS: Updated Markdown Report!")

