import openpyxl
from collections import Counter

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['Work Assignments']

sections = Counter()
prefix_counter = Counter()
total = 0

for row in ws.iter_rows(min_row=2, values_only=True):
    if not any(row):
        continue
    tc_id = str(row[0]).strip() if row[0] else ''
    section = str(row[1]).strip() if row[1] else ''
    total += 1
    sections[section] += 1
    prefix = tc_id.split('-')[0] if '-' in tc_id else tc_id
    prefix_counter[prefix] += 1

print(f"Total Test Cases in Excel 'Work Assignments': {total}")
print("\nBreakdown by Section:")
for s, c in sections.items():
    print(f"  {s}: {c} TCs")

print("\nBreakdown by Prefix:")
for p, c in prefix_counter.items():
    print(f"  {p}: {c} TCs")
