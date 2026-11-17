import re

files = [
    "Defects/Attendance2_Master_Defect_Log.md",
    "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"
]

defects = [
    "DEFECT-20261105-01",
    "DEFECT-20261105-02",
    "DEFECT-20261105-03",
    "DEFECT-20261105-04",
    "DEFECT-20261106-01",
    "DEFECT-20261106-02",
    "DEFECT-20261106-03",
    "DEFECT-20261106-04",
    "DEFECT-20261106-05",
    "DEFECT-20261106-06",
    "DEFECT-20261106-07"
]

for fpath in files:
    print("=" * 60)
    print("FILE:", fpath)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    for d in defects:
        count = content.count(d)
        print(f"  {d}: occurrences = {count}")
