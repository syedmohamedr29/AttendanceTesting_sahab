import json
from collections import Counter

with open("scratch/all_user_scenarios_dump.json") as f:
    tcs = json.load(f)

print(f"Total TCs: {len(tcs)}")
status_counts = Counter(tc["status"] for tc in tcs)
print("Status breakdown in sheet:")
for st, count in status_counts.items():
    print(f"  '{st}': {count}")

# Check sections for Not-Run
not_run_sections = Counter(tc["section"] for tc in tcs if tc["status"] not in ["Pass", "Fail"])
print(f"\nSections with Not-Run cases ({sum(not_run_sections.values())} total):")
for sec, count in not_run_sections.items():
    print(f"  {sec}: {count}")

