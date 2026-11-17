import re

files = [
    "Defects/Attendance2_Master_Defect_Log.md",
    "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"
]

pattern = re.compile(r"DEFECT-20261110-\d+|Part 3I|10 November 2026", re.IGNORECASE)

for fpath in files:
    print("=" * 60)
    print(f"File: {fpath}")
    with open(fpath, "r", encoding="utf-8") as f:
        text = f.read()
    
    matches = [m.start() for m in pattern.finditer(text)]
    print(f"Matches found: {len(matches)}")
    seen = set()
    for m in matches:
        line_start = text.rfind("\n", 0, m) + 1
        line_end = text.find("\n", m)
        line = text[line_start:line_end].strip()
        if line not in seen:
            seen.add(line)
            if line.startswith("#") or "DEFECT-20261110" in line:
                print(f"  {line[:100]}")
