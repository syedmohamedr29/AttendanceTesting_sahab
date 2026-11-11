import openpyxl, sys, re
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

print("Sheet names:", wb.sheetnames)

post_patch_tcs = []

# Scan all sheets except INDEX
for sname in wb.sheetnames:
    if sname in ['INDEX', 'User Scenarios (Add Here)']:
        continue
    ws = wb[sname]
    header = [str(c) for c in next(ws.iter_rows(values_only=True))]
    
    for row_idx, r in enumerate(ws.iter_rows(values_only=True), 2):
        if not r or not r[0]:
            continue
        tc_id = str(r[0])
        section = str(r[1]) if len(r) > 1 and r[1] is not None else ""
        scenario = str(r[2]) if len(r) > 2 and r[2] is not None else ""
        precond = str(r[3]) if len(r) > 3 and r[3] is not None else ""
        expected = str(r[4]) if len(r) > 4 and r[4] is not None else ""
        tc_type = str(r[6]) if len(r) > 6 and r[6] is not None else ""
        
        full_text = f"{section} {scenario} {precond} {expected}".lower()
        
        # Check if it relates to POST / PUT / PATCH / Create / Update / Edit / Validation
        is_mutation = any(m in full_text for m in ['post', 'put', 'patch', 'create', 'update', 'edit', 'delete', 'restore', 'apply'])
        is_validation = any(v in full_text for v in ['validation', 'validat', 'required', '400', 'sbp:validation', 'missing', 'invalid', 'empty', 'format', 'null', 'bad request', 'dto'])
        
        post_patch_tcs.append({
            'sheet': sname,
            'tc_id': tc_id,
            'section': section,
            'scenario': scenario,
            'precond': precond,
            'expected': expected,
            'is_mutation': is_mutation,
            'is_validation': is_validation,
            'type': tc_type
        })

print(f"Total test cases scanned: {len(post_patch_tcs)}")
validation_tcs = [tc for tc in post_patch_tcs if tc['is_validation']]
print(f"Total validation test cases found: {len(validation_tcs)}")

