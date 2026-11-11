import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    content = f.read()

target_start = "### Summary Matrix: Attendance 4 Live Execution (13 Scenarios)"
target_end = "# 📅 Part 3: Defects Identified on 28 October 2026 (LIVE EXECUTION & USER SCENARIOS)"

idx_start = content.find(target_start)
idx_end = content.find(target_end)

print(f"Start index: {idx_start}, End index: {idx_end}")
print("Found target region length:", idx_end - idx_start)

