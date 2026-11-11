with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('DEFECT-20261026-02: `TenantName`', 'DEFECT-20261026-02 (DEFECT-20261028-05): `TenantName`')
text = text.replace('DEFECT-20261026-04: `tenantName`', 'DEFECT-20261026-04 (DEFECT-20261028-06): `tenantName`')

with open('Defects/Attendance2_Master_Defect_Log.md', 'w', encoding='utf-8') as f:
    f.write(text)
print('Updated defect log with aliases!')

