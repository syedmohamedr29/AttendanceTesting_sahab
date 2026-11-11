import openpyxl
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['WT - Company Default']

print(f"Sheet '{ws.title}' has {ws.max_row} rows (including header).")

sections = {}
rows_data = []

for r in range(2, ws.max_row + 1):
    tc_id = ws.cell(r, 1).value
    sec = ws.cell(r, 2).value
    scen = ws.cell(r, 3).value
    inp = ws.cell(r, 4).value
    exp = ws.cell(r, 5).value
    pri = ws.cell(r, 6).value
    t_type = ws.cell(r, 7).value
    status = ws.cell(r, 9).value
    
    sections[sec] = sections.get(sec, 0) + 1
    rows_data.append({
        "row": r,
        "id": tc_id,
        "section": sec,
        "scenario": scen,
        "input": inp,
        "expected": exp,
        "pri": pri,
        "type": t_type,
        "status": status
    })

print(f"\nSections breakdown ({len(sections)} sections):")
for sec, cnt in sections.items():
    print(f"  - {sec}: {cnt} test cases")

with open('scratch/cdwt_all_rows.json', 'w', encoding='utf-8') as f:
    json.dump(rows_data, f, indent=2, ensure_ascii=False)

print(f"\nSaved all {len(rows_data)} test cases to scratch/cdwt_all_rows.json")

