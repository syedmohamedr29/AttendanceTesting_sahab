import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook(r'document (Enum and db collection)\AttendanceTestCases.xlsx', data_only=True)
ws = wb['Work Template - Location']

print("=== Work Template - Location Test Cases ===")
for r in ws.iter_rows(values_only=True):
    if not r or not r[0]: continue
    line = ' | '.join(str(c) for c in r if c is not None)
    lower = line.lower()
    if any(k in lower for k in ['create', 'first', 'company default', 'already', 'cascade', 'linked', 'locationid', 'header', 'cap', 'limit']):
        print(f"[{r[0]}] {r[1]} | {r[2]} | {str(r[3])[:40]} -> {str(r[4])[:70]}")

