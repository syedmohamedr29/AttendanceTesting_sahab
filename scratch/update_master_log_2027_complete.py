import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

log_path = 'Defects/Attendance2_Master_Defect_Log.md'

with open(log_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Matrix rows for DEFECT-20261027-01, 02, 05
matrix_updates = [
    (
        r'\| \[`DEFECT-20261027-01`\]\(#defect-20261027-01\) \| 🟠 P1 \| Work Plans \| Missing `locationId` in `POST /workplans` throws unhandled HTTP 500 crash instead of clean 400 \| ``POST /workplans`` \| .*? \|',
        r'| [`DEFECT-20261027-01`](#defect-20261027-01) | 🟢 P1 | Work Plans | **[FIXED]** Missing `locationId` query param: HTTP 500 crash resolved; cleanly rejected with HTTP 400 | ``POST /workplans`` | 🟢 Verified Fixed (HTTP 400) |'
    ),
    (
        r'\| \[`DEFECT-20261027-02`\]\(#defect-20261027-02\) \| 🟡 P2 \| Work Plans \| Redundant DTO validation on audit field `CreatedBy` forces client to submit user identity in body \| ``POST /workplans`` \| Audit DTO Contract \|',
        r'| [`DEFECT-20261027-02`](#defect-20261027-02) | 🟢 P2 | Policies / Work Plans | **[FIXED]** Redundant `CreatedBy` removed from body DTOs; assigned server-side from JWT | ``POST /attpolicies/*`` | 🟢 Verified Fixed |'
    ),
    (
        r'\| \[`DEFECT-20261027-05`\]\(#defect-20261027-05\) \| 🟠 P1 \| Work Template \| Header `Location` model binding trap during CDWT setup causes ASP.NET Core binding collision \| ``POST /worktemplates`` \| Controller Binding \|',
        r'| [`DEFECT-20261027-05`](#defect-20261027-05) | 🟢 P1 | Work Template | **[FIXED]** Header `Location` model binding trap decoupled; CDWT setup creates default shift without collision | ``POST /worktemplates`` | 🟢 Verified Fixed |'
    )
]

for pat, repl in matrix_updates:
    new_c, n = re.subn(pat, repl, content)
    if n > 0:
        content = new_c
        print(f"Matrix updated for {pat[:35]}")
    else:
        print(f"WARNING: Matrix pattern not matched: {pat[:35]}")

# 2. Update DEFECT-20261027-01 Heading, Status, and Historical vs Live Re-Verification section
old_h1 = '### <a id="defect-20261027-01"></a>🔴 DEFECT-20261027-01:'
new_h1 = '### <a id="defect-20261027-01"></a>🟢 DEFECT-20261027-01:'
if old_h1 in content:
    content = content.replace(old_h1, new_h1)
    print("Heading DEFECT-20261027-01 updated to 🟢")

pat_stat1 = r'(### <a id="defect-20261027-01"></a>.*?-\s*\*\*Status:\*\*)\s*❌\s*\*\*Open / Verified with Evidence\*\*'
repl_stat1 = r'\1 🟢 **RESOLVED / VERIFIED FIXED LIVE**'
content, n_stat = re.subn(pat_stat1, repl_stat1, content, flags=re.DOTALL)
print(f"Status for DEFECT-20261027-01 updated: {n_stat}")

# Check if Historical vs Live Re-Verification block exists for 01
idx_01 = content.find('id="defect-20261027-01"')
if idx_01 != -1:
    idx_next = content.find('### <a id="defect-', idx_01 + 20)
    block_01 = content[idx_01:idx_next]
    if "Historical vs Live Re-Verification" not in block_01:
        idx_ev = block_01.find('#### 5. Photographic Proof')
        if idx_ev != -1:
            ins_pos = idx_01 + idx_ev
            rev_text = """#### 4. Historical vs Live Re-Verification Server Response
* **Historical Baseline (27-Oct-2026):** `HTTP 500 Internal Server Error` (Unhandled `NullReferenceException` / `SimpleException`).
* **Live Re-Verification (04/05-Nov-2026):** 🟢 **`HTTP 400 Bad Request`**.
  ```json
  {
    "error": {
      "code": "Cit.Attendance:Validation",
      "message": "LocationId is required. A work plan can only be created for a location. Work Plan name is required. Description is required. Minimum 10 characters",
      "details": null,
      "data": null,
      "validationErrors": [
        {
          "errorCode": "Cit.Attendance:Validation",
          "errorMessage": "LocationId is required. A work plan can only be created for a location.",
          "propertyName": "LocationId",
          "severity": 0
        }
      ]
    }
  }
  ```

"""
            content = content[:ins_pos] + rev_text + content[ins_pos:]
            print("Added Historical vs Live Re-Verification section to DEFECT-20261027-01")

# 3. Update Checklist items in Master Defect Log
checklists = [
    (
        r'- \[ \] \*\*P1 \(`DEFECT-20261027-01`\):\*\* Require `locationId` in `POST /workplans` with clean HTTP 400 instead of HTTP 500 crash\.',
        r'- [x] **P1 (`DEFECT-20261027-01`):** Require `locationId` in `POST /workplans` with clean HTTP 400 instead of HTTP 500 crash. *(Verified Fixed Live: HTTP 400 Cit.Attendance:Validation)*'
    ),
    (
        r'- \[ \] \*\*P2 \(`DEFECT-20261027-02`\):\*\* Remove redundant `CreatedBy` field from `POST /workplans` request body\.',
        r'- [x] **P2 (`DEFECT-20261027-02`):** Remove redundant `CreatedBy` field from policy/work plan request body. *(Verified Fixed Live)*'
    )
]

for pat, repl in checklists:
    new_c, n = re.subn(pat, repl, content)
    if n > 0:
        content = new_c
        print(f"Checklist item updated for {pat[:35]}")
    else:
        print(f"WARNING: Checklist pattern not matched: {pat[:35]}")

with open(log_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Defects/Attendance2_Master_Defect_Log.md successfully updated!")

