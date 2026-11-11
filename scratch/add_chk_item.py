import sys
sys.stdout.reconfigure(encoding='utf-8')

log_path = 'Defects/Attendance2_Master_Defect_Log.md'
with open(log_path, 'r', encoding='utf-8') as f:
    text = f.read()

target = "### Priority 2: Audit & Contract Cleanups\n"
item = "- [ ] **P2 (`DEFECT-20261105-02`):** In `SP.AttendanceSvc`, create dedicated `Create*PolicyDto` and `Update*PolicyDto` removing `id` and `tenantName` from request body schemas. Pre-populate `TenantName` and `TenantId` server-side from `ICurrentTenant` context into MongoDB `ERP.Attendance.Policies`.\n"

if target in text and "DEFECT-20261105-02" not in text[140000:]:
    text = text.replace(target, target + item, 1)
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Added DEFECT-20261105-02 to Section 8 Priority 2 Checklist successfully!")
else:
    print("Already present or target not found.")

