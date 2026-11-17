import re
from collections import defaultdict

files = [
    "Defects/Attendance2_Master_Defect_Log.md",
    "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"
]

header_pattern = re.compile(r"### (?:<a id=\"([^\"]+)\"></a>)?.*?(DEFECT-\d{8}-\d{2})")

for fpath in files:
    print("=" * 60)
    print(f"Checking duplicate headers in: {fpath}")
    with open(fpath, "r", encoding="utf-8") as f:
        text = f.read()
    
    header_counts = defaultdict(list)
    for idx, line in enumerate(text.splitlines(), start=1):
        if line.startswith("### "):
            m = re.search(r"DEFECT-\d{8}-\d{2}", line)
            if m:
                header_counts[m.group(0)].append((idx, line.strip()[:80]))
                
    dup_found = False
    for did, occurrences in sorted(header_counts.items()):
        if len(occurrences) > 1:
            dup_found = True
            print(f"\nDefect {did} has {len(occurrences)} '### ' headers:")
            for occ in occurrences:
                print(f"  Line {occ[0]}: {occ[1]}")
    if not dup_found:
        print("No duplicate '### ' defect headers found!")
