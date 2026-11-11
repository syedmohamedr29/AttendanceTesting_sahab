import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
sheet = wb['Holiday Calendar - Test Cases']

sections = {}

for r in range(2, sheet.max_row + 1):
    sec = sheet.cell(r, 2).value
    st = sheet.cell(r, 9).value
    if sec:
        if sec not in sections:
            sections[sec] = {'total': 0, 'pass': 0, 'fail': 0}
        sections[sec]['total'] += 1
        if st and ('pass' in str(st).lower()):
            sections[sec]['pass'] += 1
        elif st and ('fail' in str(st).lower()):
            sections[sec]['fail'] += 1

print(f"Total sections: {len(sections)}")
tot_all = 0
tot_pass = 0
tot_fail = 0
for s, d in sections.items():
    rate = (d['pass'] / d['total'] * 100) if d['total'] > 0 else 0
    print(f"| **{s}** | {d['total']} | {d['pass']} | {d['fail']} | {rate:.1f}% |")
    tot_all += d['total']
    tot_pass += d['pass']
    tot_fail += d['fail']

print(f"TOTAL: {tot_all} | Passed: {tot_pass} | Failed: {tot_fail} | Rate: {tot_pass/tot_all*100:.1f}%")

