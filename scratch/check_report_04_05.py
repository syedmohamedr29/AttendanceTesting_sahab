with open("Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    for d in ["DEFECT-20261106-04", "DEFECT-20261106-05"]:
        if d in line:
            print(f"{d} at line {idx+1}:")
            print("  ", line.strip())
            # print surrounding lines
            start = max(0, idx - 5)
            end = min(len(lines), idx + 15)
            print("--- Context ---")
            for j in range(start, end):
                print(f"{j+1}: {lines[j].rstrip()}")
            print("-" * 50)
