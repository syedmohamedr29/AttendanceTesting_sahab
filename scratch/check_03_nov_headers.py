with open("Defects/Attendance2_Master_Defect_Log.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(1, 17):
    d = f"DEFECT-20261103-{i:02d}"
    found_lines = []
    for idx, l in enumerate(lines):
        if f"### " in l and d in l:
            found_lines.append((idx+1, l.strip()))
    if found_lines:
        for fl in found_lines:
            print(f"{d} at line {fl[0]}: {fl[1][:80]}")
    else:
        print(f"{d}: No direct '### ' header")
