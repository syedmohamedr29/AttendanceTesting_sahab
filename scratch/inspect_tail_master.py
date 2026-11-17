with open("Defects/Attendance2_Master_Defect_Log.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx in range(5700, len(lines)):
    line = lines[idx]
    if line.startswith("### ") or line.startswith("## ") or line.startswith("# "):
        print(f"Line {idx+1}: {line.strip()[:80]}")
