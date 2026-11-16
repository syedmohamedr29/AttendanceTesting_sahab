import re
from collections import Counter

with open('reports/WORK_ASSIGNMENT_TEST_CASES.md', 'r', encoding='utf-8') as f:
    text = f.read()

wa_tcs = re.findall(r'`(WA-[A-Z0-9\-]+)`', text)
print(f"Total `WA-*` test case references in markdown: {len(wa_tcs)}")
unique_wa = list(dict.fromkeys(wa_tcs))
print(f"Unique `WA-*` test cases in markdown: {len(unique_wa)}")

sections = Counter()
for tc in unique_wa:
    prefix = '-'.join(tc.split('-')[:2])
    sections[prefix] += 1

print("\nBreakdown of unique TCs in WORK_ASSIGNMENT_TEST_CASES.md:")
for s, count in sorted(sections.items()):
    print(f"  {s}: {count} TCs")
