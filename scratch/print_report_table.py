with open("Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(44, 65):
    print(lines[i].rstrip())
