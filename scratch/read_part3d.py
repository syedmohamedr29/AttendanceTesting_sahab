with open("Defects/Attendance2_Master_Defect_Log.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, l in enumerate(lines):
    if "Part 3D: Defects Identified on 02 November 2026" in l:
        print(f"Starts at line {idx+1}")
        for j in range(idx, min(len(lines), idx + 80)):
            print(lines[j].rstrip())
        break
