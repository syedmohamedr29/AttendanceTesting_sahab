import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

for path in ["Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md", "Defects/Attendance2_Master_Defect_Log.md"]:
    print(f"=== {path} ===")
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    for line in text.splitlines():
        if any(w in line for w in ["Total Defects", "Total Tracked", "Active Open", "Active Defects", "Critical", "Closed Defects"]):
            print(line)
