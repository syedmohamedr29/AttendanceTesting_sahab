import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['Work Assignments']
doc_count = sum(1 for r in ws.iter_rows(min_row=2, values_only=True) if r[0] and str(r[0]).startswith('DOC-'))
root_count = sum(1 for r in ws.iter_rows(min_row=2, values_only=True) if r[0] and str(r[0]).startswith('ROOT-'))
wa_flow_count = sum(1 for r in ws.iter_rows(min_row=2, values_only=True) if r[0] and str(r[0]).startswith('WA-FLOW-'))
wa_emp_count = sum(1 for r in ws.iter_rows(min_row=2, values_only=True) if r[0] and str(r[0]).startswith('WA-EMP-'))

print(f"DOC: {doc_count}")
print(f"ROOT: {root_count}")
print(f"WA-FLOW: {wa_flow_count}")
print(f"WA-EMP: {wa_emp_count}")
print(f"Total: {doc_count + root_count + wa_flow_count + wa_emp_count}")
