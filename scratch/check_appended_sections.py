with open("Defects/Attendance2_Master_Defect_Log.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for idx, l in enumerate(lines):
    if l.startswith("### 📊"):
        print(f"Line {idx+1}: {l.strip()}")
