import re

files = [
    "Defects/Attendance2_Master_Defect_Log.md",
    "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"
]

pattern = re.compile(r"DEFECT-20261029-\d+")

for fpath in files:
    with open(fpath, "r", encoding="utf-8") as f:
        text = f.read()
    matches = sorted(list(set(pattern.findall(text))))
    print("=" * 60)
    print(f"File: {fpath}")
    print(f"Total matching 29-Oct defects: {len(matches)}")
    for m in matches:
        pos = text.find(m)
        line_start = text.rfind("\n", 0, pos) + 1
        line_end = text.find("\n", pos)
        print(f"  {m}: {text[line_start:line_end].strip()[:90]}")
