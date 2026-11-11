import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

insert_idx = -1
for i in range(1250, 1275):
    if lines[i].strip() == '```' and 'DEFECT-20261028-03' in lines[i+4]:
        insert_idx = i + 1
        break

print("insert_idx:", insert_idx)

if insert_idx != -1:
    reverif_text = [
        "* **Status:** 🟢 **RESOLVED / VERIFIED FIXED LIVE (05-Nov-2026)**\n",
        "* **Live Re-Verification Proof (Attendance 4 Execution — `USER-22` & `USER-37`):**\n",
        "  - **Empty PATCH Body (`USER-22`):** Calling `PATCH /worktemplates/flexi/53470658-5f9b-47b4-b254-f96b9501401c` with `{}` now cleanly returns **HTTP 400 Bad Request** with `Cit.Attendance:Validation` (\"An English template name is required. All 7 days of the week must be defined, each day once.\"), completely eliminating the HTTP 500 crash.\n",
        "  - **Invalid DayEnum 8 (`USER-37`):** Calling `POST /worktemplates/flexi` with invalid DayEnum `8` now cleanly returns **HTTP 400 Bad Request** with `Cit.Attendance:Validation` (\"All 7 days of the week must be defined, each day once.\"), eliminating the HTTP 500 crash.\n",
        "  - **Split Shift Interval Overlaps (`USER-137`):** Calling `POST /worktemplates/split` with overlapping shift intervals now cleanly returns **HTTP 400 Bad Request** with `Cit.Attendance:Validation` (\"Shift time slot cannot overlap with other slot.\").\n",
        "  - **Days Sum Invariant (`USER-138`):** Calling `POST /worktemplates/fixed` with `6 + 2 = 8` days now cleanly returns **HTTP 400 Bad Request** with `Cit.Attendance:Validation` (\"Total working days and total days off must equal 7 days.\").\n"
    ]
    new_lines = lines[:insert_idx] + reverif_text + lines[insert_idx:]
    with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("Successfully inserted live re-verification block!")
else:
    print("Could not find insert_idx")

