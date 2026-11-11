import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

defect_log_path = "Defects/Attendance2_Master_Defect_Log.md"
report_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

with open(defect_log_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add Evidence 44 row to Evidence table
evidence_row = """| ![DEFECT-20261106-01-ATT7](../defect_evidence/evidence_44_attendance7_reverification_defects_compass.png) | **File:** `evidence_44_attendance7_reverification_defects_compass.png`<br>**Defects:** [`DEFECT-20261105-03`](#defect-20261105-03), [`DEFECT-20261105-04`](#defect-20261105-04), [`DEFECT-20261106-01`](#defect-20261106-01)<br>**Description:** Comprehensive live re-verification on Company Attendance 7 (`3a249870-c8ae-b3dc-1b8d-c44efad14f89`). Confirms reproduction of negative Overtime rateFormula (-1.5) HTTP 200, duplicate client-dictated ID HTTP 500 crash, and empty `TenantName: {}` in MongoDB Compass. |
"""

target_ev = "| ![DEFECT-20261106-01]"
if target_ev in content:
    content = content.replace(target_ev, evidence_row + target_ev)

with open(defect_log_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated Defects/Attendance2_Master_Defect_Log.md with Evidence 44!")

# Update report too
with open(report_path, "r", encoding="utf-8") as f:
    rep = f.read()

# Add note about Attendance 7 in report
if "Attendance 7" not in rep:
    rep_insert = "\n> [!NOTE]\n> **Attendance 7 Live Re-Verification Completed (06 November 2026):** Confirmed full reproduction of `DEFECT-20261105-03`, `DEFECT-20261105-04`, and `DEFECT-20261106-01` against Company Attendance 7 (`3a249870-c8ae-b3dc-1b8d-c44efad14f89`). Evidence saved to [Evidence 44](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_44_attendance7_reverification_defects_compass.png).\n"
    marker = "## 1. Executive Summary"
    if marker in rep:
        rep = rep.replace(marker, marker + rep_insert)

with open(report_path, "w", encoding="utf-8") as f:
    f.write(rep)
print("Updated Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md with Attendance 7 note!")

