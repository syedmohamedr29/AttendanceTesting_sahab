import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = 'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_block = """* **Live Tampering & Proof of Bug:**
  1. **Client Tenant Spoofing:** In `PATCH /worktemplates/fixed/{id}`, sending `"tenantName": {"en": "Spoofed Tenant In Body"}` returned `HTTP 200 OK` and saved the spoofed string into MongoDB!
  2. **Empty Object Bug:** When the client omits `tenantName` (as the frontend should), MongoDB persists `TenantName: Object (empty)` `{}` (confirmed in MongoDB Compass).
  3. **Dead Contract Parameter:** `shortCode` is declared in all 5 `Update*WorkTemplateDto` models, but modifying it throws `Cit.Attendance:1107 ("A work template's short code cannot be changed after it is created")`."""

new_block = """* **Live Tampering & Proof of Bug (Comprehensive 6-Endpoint Audit on 2026-11-04):**
  A live verification test was executed on 2026-11-04 across all 6 Work Template creation and update endpoints:

  | # | Operation | Endpoint | Body DTO Schema | Client Payload Injected | HTTP Status | MongoDB Template ID | Stored `TenantName` | Verdict |
  |:---:|---|---|---|---|:---:|---|---|:---:|
  | 1 | **POST Fixed** | `/api/companies/{cId}/worktemplates/fixed` | `FixedWorkTemplateDto` | `{"tenantName": {"en": "Spoofed Tenant In POST Fixed"}}` | **200 OK** | `0dfe6de8-0784-4871-876e-c6d5ea85c91d` | `{'en': 'Spoofed Tenant In POST Fixed'}` | ❌ **FAIL** |
  | 2 | **POST Flexi** | `/api/companies/{cId}/worktemplates/flexi` | `FlexiWorkTemplateDto` | `{"tenantName": {"en": "Spoofed Injected Tenant POST Flexi"}}` | **200 OK** | `7c9673df-5c85-405f-a8fd-5de6b4ef4959` | `{'en': 'Spoofed Injected Tenant POST Flexi'}` | ❌ **FAIL** |
  | 3 | **POST Split** | `/api/companies/{cId}/worktemplates/split` | `SplitWorkTemplateDto` | `{"tenantName": {"en": "Spoofed Injected Tenant POST Split"}}` | **200 OK** | `2fb70114-cafc-4e21-bff1-80603c9c84a8` | `{'en': 'Spoofed Injected Tenant POST Split'}` | ❌ **FAIL** |
  | 4 | **PATCH Fixed** | `/api/companies/{cId}/worktemplates/fixed/{id}` | `UpdateFixedWorkTemplateDto` | `{"tenantName": {"en": "Spoofed Tenant In PATCH Fixed v2.0"}}` | **200 OK** | `bd3c48cb-0881-4eb7-9802-6d45a020e929` | `{'en': 'Spoofed Tenant In PATCH Fixed v2.0'}` | ❌ **FAIL** |
  | 5 | **PATCH Flexi** | `/api/companies/{cId}/worktemplates/flexi/{id}` | `UpdateFlexiWorkTemplateDto` | `{"tenantName": {"en": "Spoofed Tenant In PATCH Flexi v2.0"}}` | **200 OK** | `f6081d7e-b61a-4260-aae1-9bae5a001793` | `{'en': 'Spoofed Tenant In PATCH Flexi v2.0'}` | ❌ **FAIL** |
  | 6 | **PATCH Split** | `/api/companies/{cId}/worktemplates/split/{id}` | `UpdateSplitWorkTemplateDto` | `{"tenantName": {"en": "Spoofed Tenant In PATCH Split v2.0"}}` | **200 OK** | `54c65fdc-6fc3-40f2-b4ed-fb13273b627f` | `{'en': 'Spoofed Tenant In PATCH Split v2.0'}` | ❌ **FAIL** |

  1. **Client Tenant Spoofing Persists Everywhere:** All 6 endpoints accept client-spoofed `tenantName` with HTTP 200 OK and overwrite MongoDB `TenantName`!
  2. **Empty Object Bug:** When the client omits `tenantName` (as the frontend should), MongoDB persists `TenantName: Object (empty)` `{}` (confirmed in MongoDB Compass on Attendance 8 v1.0 and Attendance 3 v1.0).
  3. **Dead Contract Parameter:** `shortCode` is declared in all 5 `Update*WorkTemplateDto` models, but modifying it throws `Cit.Attendance:1107 ("A work template's short code cannot be changed after it is created")`."""

if old_block in content:
    content = content.replace(old_block, new_block)
    print("Replaced old_block successfully.")
else:
    print("Could not find old_block in content!")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Updated {file_path} successfully.")

