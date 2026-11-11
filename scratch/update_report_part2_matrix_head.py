import sys

sys.stdout.reconfigure(encoding='utf-8')

report_path = 'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md'

with open(report_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update the Summary Matrix title and header for Part 2
old_h = "### Summary Matrix (27-Oct-2026 — Re-Verified Live on 28-Oct-2026)\n\n| Defect ID | Severity | Module & Endpoint | Summary of Defect | Expected Behavior | Live Re-Test Status (28-Oct) |"
new_h = "### Summary Matrix (27-Oct-2026) — *Re-Verified Live 04-Nov-2026: 🟢 ALL 7 DEFECTS FULLY RESOLVED*\n\n| Defect ID | Severity | Module & Endpoint | Summary of Defect | Expected Behavior | Status (Re-Verified Live 04-Nov-2026) |"

if old_h in content:
    content = content.replace(old_h, new_h, 1)
    print("Replaced Summary Matrix header!")
else:
    print("WARNING: Summary Matrix header string not found verbatim!")

with open(report_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Report updated successfully!")

