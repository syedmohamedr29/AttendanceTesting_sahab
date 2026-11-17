with open("Defects/Attendance2_Master_Defect_Log.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    for d in ["DEFECT-20261106-04", "DEFECT-20261106-05"]:
        if f'### <a id="{d.lower()}"></a>' in line or f'### 🔴 {d}' in line:
            # find preceding section header ## or #
            sec_header = ""
            for prev_idx in range(idx, -1, -1):
                if lines[prev_idx].startswith("## ") or lines[prev_idx].startswith("# "):
                    sec_header = lines[prev_idx].strip()
                    break
            print(f"{d} at line {idx+1}: Under section '{sec_header}'")
