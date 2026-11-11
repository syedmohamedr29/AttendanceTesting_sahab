import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'r', encoding='utf-8') as f:
    text = f.read()

target = '| **2.6** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/split/{id}` | `{id}` *(No `locationId`)* | `splitTimeSlots: [...]` | **HTTP 200**: Staged edit creates **Version 4.0** with Split shift configuration. | `ERP.Attendance.WorkTemplates` |'

replacement = '| **2.6** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/split/{id}` | `{id}` *(No `locationId`)* | `splitTimeSlots: [2 intervals/day]`<br>`totalWorkDurationInMinutes: 2880` | **HTTP 200**: Staged edit creates **Version 4.0** (`_id: 6bc32276-...`). Marks v3.0 `IsSuperseded: true`. Stores `TemplateType: 3` (Split). Captures ChangeLog: [Work Type: Flexible → Split, Timings Changed, Weekly hours: 54h → 48h]. Sets `HasPendingLocSync = true`. | `ERP.Attendance.WorkTemplates` |'

if target in text:
    updated = text.replace(target, replacement, 1)
    with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'w', encoding='utf-8') as f:
        f.write(updated)
    print("Successfully enhanced Step 2.6 in API Guide!")
else:
    print("Target not found!")

