import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

# Search document (Enum and db collection)/AttendanceTestCases.xlsx
wb_doc = openpyxl.load_workbook('document (Enum and db collection)/AttendanceTestCases.xlsx', data_only=True)
print("=== Searching document (Enum and db collection) ===")
for sheet in wb_doc.sheetnames:
    ws = wb_doc[sheet]
    for r in range(1, ws.max_row+1):
        row_str = " | ".join([str(ws.cell(r, c).value) for c in range(1, min(ws.max_column+1, 8)) if ws.cell(r, c).value is not None])
        for kw in ['short code cannot', '1107', 'companylinked', 'templatename', 'shortcode change', 'companyid']:
            if kw in row_str.lower():
                print(f"[{sheet}] R{r}: {row_str[:140]}")
                break

# Search root AttendanceTestCases.xlsx
wb_root = openpyxl.load_workbook('AttendanceTestCases.xlsx', data_only=True)
print("\n=== Searching root AttendanceTestCases.xlsx ===")
for sheet in wb_root.sheetnames:
    ws = wb_root[sheet]
    for r in range(1, ws.max_row+1):
        row_str = " | ".join([str(ws.cell(r, c).value) for c in range(1, min(ws.max_column+1, 8)) if ws.cell(r, c).value is not None])
        for kw in ['short code cannot', '1107', 'companylinked', 'shortcode change']:
            if kw in row_str.lower():
                print(f"[{sheet}] R{r}: {row_str[:140]}")
                break

