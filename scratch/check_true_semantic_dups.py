import sys
import openpyxl
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

# Let's check for true duplicates: same sheet, identical scenario AND identical input/preconditions!
true_dups = []

for sheet in wb.sheetnames:
    if sheet == 'INDEX':
        continue
    ws = wb[sheet]
    seen = {}
    for r in range(2, ws.max_row+1):
        tc_id = str(ws.cell(r, 1).value or '').strip()
        sec = str(ws.cell(r, 2).value or '').strip()
        scen = str(ws.cell(r, 3).value or '').strip()
        inp = str(ws.cell(r, 4).value or '').strip()
        exp = str(ws.cell(r, 5).value or '').strip()
        
        # Key combining scenario and input
        key = (scen.lower(), inp.lower())
        if scen and inp:
            if key in seen:
                prev_r, prev_tc, prev_sec = seen[key]
                true_dups.append({
                    'sheet': sheet,
                    'row1': prev_r,
                    'tc1': prev_tc,
                    'sec1': prev_sec,
                    'row2': r,
                    'tc2': tc_id,
                    'sec2': sec,
                    'scen': scen,
                    'input': inp
                })
            else:
                seen[key] = (r, tc_id, sec)

print(f"Total True Semantic Duplicates found (Identical Scenario + Identical Input within same sheet): {len(true_dups)}")
for d in true_dups:
    print(f"[{d['sheet']}] Row {d['row1']} ({d['tc1']}) vs Row {d['row2']} ({d['tc2']}):")
    print(f"   Scenario: {d['scen'][:80]}")
    print(f"   Input: {d['input'][:80]}")
    print("-" * 60)

