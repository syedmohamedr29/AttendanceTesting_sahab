import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

report_path = 'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md'

with open(report_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the progress banner above the table
pat_banner = r'> \*\*Live Execution Progress to Date:\*\* \*\*598 Test Cases Executed\*\* \(.*?\) — \*\*.*?\*\*'
repl_banner = r'> **Live Execution Progress to Date:** **604 Test Cases Executed** (582 Passed, 22 Failed, 981 Not-Run) — **96.4% Pass Rate on Executed Tests**'
content, n1 = re.subn(pat_banner, repl_banner, content)
print(f"Banner updated: {n1}")

# 2. Update Row 16 (Holiday Calendar - Test Cases)
pat_hc_row = r'\| \*\*16\*\* \| \*\*Holiday Calendar - Test Cases\*\* \| \d+ \| \d+ \| \d+ \| \d+ \| \d+ \| \*\*.*?\*\* \| \*\*.*?\*\* \| \*\*.*?\*\* \| \*\*.*?\*\* \| .*? \|'
repl_hc_row = r'| **16** | **Holiday Calendar - Test Cases** | 313 | 172 | 133 | 8 | 0 | **305** | **8** | **0** | **100.0%** | 🟢 **100% Executed (97.4% Pass Rate)** |'
content, n2 = re.subn(pat_hc_row, repl_hc_row, content)
print(f"HC Row updated: {n2}")

# 3. Update TOTAL Row
pat_total_row = r'\| \*\*TOTAL\*\* \| \*\*All 17 Modules Combined\*\* \| \*\*.*?\*\* \| \*\*.*?\*\* \| \*\*.*?\*\* \| \*\*.*?\*\* \| \*\*.*?\*\* \| \*\*.*?\*\* \| \*\*.*?\*\* \| \*\*.*?\*\* \| \*\*.*?\*\* \| .*? \|'
repl_total_row = r'| **TOTAL** | **All 17 Modules Combined** | **1,583** | **686** | **671** | **206** | **13** | **582** | **22** | **981** | **38.2%** | 🎯 **604 Executed (582 Pass, 22 Fail — 96.4% Pass Rate)** |'
content, n3 = re.subn(pat_total_row, repl_total_row, content)
print(f"Total Row updated: {n3}")

# 4. Update Key Execution Findings note under table
pat_note_hc = r'4\. \*\*`Holiday Calendar - Test Cases` \(Module 16\):\*\* 100% completed across all \d+ test cases .*?\n'
repl_note_hc = r'4. **`Holiday Calendar - Test Cases` (Module 16):** 100% completed across all 313 test cases. Live re-verification on 04-Nov-2026 confirmed **305 Passed and 8 Failed (97.4% Pass Rate)** — developer fixes resolved unhandled `ValidationException` crashes, mandatory English name rules, empty array collection invariants, chronological inversion guards, holiday type existence verification, and the today\'s date deadlock (`Cit.Attendance:1706`), reducing remaining defects down to 8 (route 404s, calendarType enum coercion, publish defense-in-depth, and CompanyChecklist event sync).\n'
content, n4 = re.subn(pat_note_hc, repl_note_hc, content)
print(f"Note HC updated: {n4}")

with open(report_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Dashboard table in report successfully updated!")

