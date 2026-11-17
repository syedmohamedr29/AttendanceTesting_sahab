with open("Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(76, 96):
    print(lines[i].rstrip())
