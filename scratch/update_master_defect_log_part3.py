import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Update DEFECT-20261028-01 row
old_r01 = '| [`DEFECT-20261028-01`](#defect-20261028-01) | 🟠 P1 | Work Template | Flexi daily work duration exceeding 24 hours (`1441` minutes) accepted with HTTP 200 OK | ``POST /worktemplates/flexi`` | Boundary Invariant |'
new_r01 = '| [`DEFECT-20261028-01`](#defect-20261028-01) | 🟢 P1 | Work Template | **[FIXED 05-Nov]** Flexi daily work duration exceeding 24 hours rejected with HTTP 400 ("A day\'s work duration cannot exceed 23 hours 59 minutes.") | ``POST /worktemplates/flexi`` | 🟢 Verified Fixed (HTTP 400) |'

# Update DEFECT-20261028-03 row
old_r03 = '| [`DEFECT-20261028-03`](#defect-20261028-03) | 🟠 P1 | Work Template | Active Company Default template can be archived or deleted without guard while work plans use it | ``PATCH /worktemplates/{id}/archive`` | Lifecycle Guard |'
new_r03 = '| [`DEFECT-20261028-03`](#defect-20261028-03) | 🟢 P1 | Work Template | **[FIXED 05-Nov]** Active Company Default protected from archive/delete with HTTP 400 Cit.Attendance:1003 ("Company default cannot be deleted.") | ``PATCH /worktemplates/{id}/archive`` | 🟢 Verified Fixed (HTTP 400) |'

# Update DEFECT-20261028-07 row
old_r07 = '| [`DEFECT-20261028-07`](#defect-20261028-07) | 🟠 P1 | Attendance Policies | Negative grace and break durations accepted across Attendance Policies endpoints | ``POST /policies`` | Policy Invariants |'
new_r07 = '| [`DEFECT-20261028-07`](#defect-20261028-07) | 🟢 P1 | Attendance Policies | **[FIXED 05-Nov]** Negative grace and break durations cleanly rejected with HTTP 400 Cit.Attendance:Validation | ``POST /policies`` | 🟢 Verified Fixed (HTTP 400) |'

# Update DEFECT-20261028-03 checklist
old_chk03 = '- [ ] **P1 (`DEFECT-20261028-03`):** Add guard preventing archiving/deleting Company Default Work Template while active Work Plans reference it.'
new_chk03 = '- [x] **P1 (`DEFECT-20261028-03`):** Add guard preventing archiving/deleting Company Default Work Template while active Work Plans reference it. *(Verified Fixed Live 05-Nov-2026: Blocked with HTTP 400 Cit.Attendance:1003)*'

if old_r01 in text:
    text = text.replace(old_r01, new_r01)
    print("Updated DEFECT-20261028-01 row in Master Defect Log!")
else:
    print("Warning: old_r01 not found")

if old_r03 in text:
    text = text.replace(old_r03, new_r03)
    print("Updated DEFECT-20261028-03 row in Master Defect Log!")
else:
    print("Warning: old_r03 not found")

if old_r07 in text:
    text = text.replace(old_r07, new_r07)
    print("Updated DEFECT-20261028-07 row in Master Defect Log!")
else:
    print("Warning: old_r07 not found")

if old_chk03 in text:
    text = text.replace(old_chk03, new_chk03)
    print("Updated DEFECT-20261028-03 checklist in Master Defect Log!")
else:
    print("Warning: old_chk03 not found")

with open('Defects/Attendance2_Master_Defect_Log.md', 'w', encoding='utf-8') as f:
    f.write(text)
print("Finished updating Master Defect Log!")

