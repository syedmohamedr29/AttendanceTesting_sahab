import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook(r'document (Enum and db collection)\AttendanceTestCases.xlsx', data_only=True)

# 1. Inspect Work Template - Company
ws_wt = wb['Work Template - Company']
print("=== Work Template - Company ===")
for r in ws_wt.iter_rows(values_only=True):
    if not r or not r[0]: continue
    line = ' | '.join(str(c) for c in r if c is not None)
    lower = line.lower()
    if any(k in lower for k in ['0 work locations', 'no work locations', 'second company default', 'already exists', '1010', 'location added after', 'new location', 'change type', 'flexi']):
        print(f"[{r[0]}] {r[1]} | {r[2]} | {str(r[3])[:40]} -> {str(r[4])[:70]}")

# 2. Inspect Holiday Calendar - Company
ws_hc = wb['Holiday Calendar - Company']
print("\n=== Holiday Calendar - Company ===")
for r in ws_hc.iter_rows(values_only=True):
    if not r or not r[0]: continue
    line = ' | '.join(str(c) for c in r if c is not None)
    lower = line.lower()
    if any(k in lower for k in ['0 work locations', 'no work locations', 'no location', 'fanout', 'fan-out', 'cascade', 'second company', 'already exists', 'new location', 'location added']):
        print(f"[{r[0]}] {r[1]} | {r[2]} | {str(r[3])[:40]} -> {str(r[4])[:70]}")

