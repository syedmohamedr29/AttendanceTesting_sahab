import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['WT - Company Default']

print(f"Sheet: {ws.title} | Rows: {ws.max_row}")

sections = {}
test_cases = []

for r in range(2, ws.max_row + 1):
    tc_id = ws.cell(r, 1).value
    sec = ws.cell(r, 2).value
    scen = ws.cell(r, 3).value
    inp = ws.cell(r, 4).value
    exp = ws.cell(r, 5).value
    pri = ws.cell(r, 6).value
    t_type = ws.cell(r, 7).value
    
    sections[sec] = sections.get(sec, 0) + 1
    test_cases.append({
        "row": r,
        "id": tc_id,
        "section": sec,
        "scenario": scen,
        "input": inp,
        "expected": exp,
        "priority": pri,
        "type": t_type
    })

print(f"\nSections in '{ws.title}':")
for sec, count in sections.items():
    print(f"  {sec}: {count} test cases")

print("\nFirst 10 test cases:")
for tc in test_cases[:10]:
    print(f"  {tc['id']} | {tc['section'][:30]} | {tc['scenario'][:45]} | {tc['priority']}")

