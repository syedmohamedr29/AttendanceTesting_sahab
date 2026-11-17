with open("Defects/Attendance2_Master_Defect_Log.md", "r", encoding="utf-8") as f:
    text = f.read()

part3g_new = """### 📊 Part 3G: Defects Identified on 05 November 2026 (Live Compass Verification: Work Template Empty CompanyName) — Re-Verification Audit

> **Execution Date:** 16 November 2026 | **Suite:** Part 3G Work Template Master Data Resolution (`DEFECT-20261105-01`)  
> **Target Environment:** DEV (`https://attendance2.dev.zoolwork.com` / `https://company8.dev.zoolwork.com`) | **DB:** MongoDB `Sahab` on `10.1.0.4:27018`  
> **Confluence Sync:** Consolidated under Confluence Page **`Bug Fixes Testing`** (Page ID `1567653890`) under folder **`Attendance company testing`** as **Row 7** (Merged with WT - Company Default to eliminate duplicate entries).  
> **Suite Status:** **1 Core Defect Re-audited | 1 NOT FIXED (100% Failed / Open)**

#### Summary of Re-Verification Status:
- **❌ Confirmed STILL NOT FIXED / FAILED (Consolidated into Confluence Row 7):**
  - **`CompanyName` Persists as `Object (empty)` `{}` (`DEFECT-20261105-01`):** Retested against `Sahab.ERP.Attendance.WorkTemplates` on Company `Attendance 9` (`3a249872-2d69-f931-41f6-d8db086b09b8`), document `d5abe5c4-d51f-4287-9baf-38e2e4f547c8`. `SP.AttendanceSvc` saves `CompanyId: UUID('3a249872-2d69-f931-41f6-d8db086b09b8')`, but leaves `CompanyName: Object (empty) {}`. The service never invokes `SP.CompanySvc` to resolve `{"en": "Attendance 9", "ar": "الحضور 9"}`. Consolidated under **Row 7** on Confluence to maintain a clean 1:1 mapping.

---

"""

pos = text.find("### 📊 Part 3G:")
if pos != -1:
    pos_end = text.find("### 📊 Part 3H:", pos)
    text = text[:pos] + part3g_new + text[pos_end:]
    with open("Defects/Attendance2_Master_Defect_Log.md", "w", encoding="utf-8") as f:
        f.write(text)
    print("Successfully replaced Part 3G in Master Defect Log!")
else:
    print("Error: Could not find Part 3G header in Master Defect Log")
