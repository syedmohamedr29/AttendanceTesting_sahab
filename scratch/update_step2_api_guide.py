import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'r', encoding='utf-8') as f:
    text = f.read()

start_str = '### Step 2: Company Default Work Template (CDWT)'
end_str = '### Step 3: Company Holiday Calendar'

start_idx = text.find(start_str)
end_idx = text.find(end_str)

if start_idx == -1 or end_idx == -1:
    print("Error: Could not find markers!")
    sys.exit(1)

new_step2 = """### Step 2: Company Default Work Template (CDWT) & Lifecycle Evolution
* **Goal:** Define the company-wide standard working schedule. Trigger automatic creation of location default templates and default plans (`LOCWOPL`). Support multi-version lifecycle across Fixed, Flexible Daily, Flexible Weekly, and Split shifts.
* **Microservice:** **`SP.AttendanceSvc`** (`attendance2.dev.zoolwork.com`)

| Step | Method | Service (`svc`) | Full Endpoint URL | Query / Route Params | Request Body / Payload | Expected Response & HTTP Code | MongoDB Collection |
|---|:---:|---|---|---|---|---|---|
| **2.1** | `POST` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/fixed` | *(No `locationId`)* | `templateName: {"en":"Attendance 1"}`<br>`shortCode: "ATTEDQA"`<br>`fixedTimeSlots: [...]` | **HTTP 201**: CDWT created (`Version: "1.0"`, `IsDefault: true`). **Auto-provisions** Location Default WT and Default Plan (`LOCWOPL`) for each location. | `ERP.Attendance.WorkTemplates`<br>`ERP.Attendance.WorkPlans`<br>*(Cross-Svc: `CompanyMaster`)* |
| **2.2** | `POST` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/flexi` | *(Alternative: Flexi Initial)* | `flexibleType: "Daily"` (or `"Weekly"`)<br>`totalWorkDurationInMinutes: 3240` | **HTTP 201**: Creates Flexi Company Default directly as Version 1.0. | `ERP.Attendance.WorkTemplates` |
| **2.3** | `POST` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/split` | *(Alternative: Split Initial)* | `splitTimeSlots: [...]` | **HTTP 201**: Creates Split Company Default directly as Version 1.0. | `ERP.Attendance.WorkTemplates` |

> [!WARNING] Critical Rule: First-Time Setup Lockout (POST vs. PATCH)
> - **`POST` is EXCLUSIVELY for first-time setup** when no default template exists for the company.
> - Once a default work template exists (`IsDefault: true`), calling `POST /fixed`, `POST /flexi`, or `POST /split` will immediately throw **`HTTP 409 Conflict`** (*"A default work template already exists for this company. Please use PATCH to update or switch template types."*).
> - **To switch template types or update timings, ALWAYS use `PATCH`!**

> [!WARNING] Critical Cross-Service Integration & Known Defect (`USER-01`)
> * **Expected Behavior:** Upon successful creation of the Company Default Work Schedule, Attendance Service must notify **Company Service** (`SP.CompanySvc`), which must update the company master profile:  
>   `CompanyMaster` collection $\\rightarrow$ `CompanyChecklist.WorkSchedulesCreated = true`.
> * **Current Defect Status (Reported by QA):** `CompanyChecklist.WorkSchedulesCreated` remains `false`. The checklist flag is not updated, causing onboarding/setup validation to report incomplete work schedule setup.

#### Subsequent Edits, Shift Type Switching & Version Progression:

| Step | Method | Service (`svc`) | Full Endpoint URL | Query / Route Params | Request Body / Payload | Expected Response & HTTP Code | MongoDB Collection |
|---|:---:|---|---|---|---|---|---|
| **2.4** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/flexi/{id}` | `{id}` *(No `locationId`)* | `flexibleType: "Daily"`<br>`totalWorkDurationInMinutes: 3240`<br>`flexiTimeSlots: [9h per day]` | **HTTP 200**: Staged edit creates **Version 2.0** (`_id: 23791f16-...`). Marks v1.0 `IsSuperseded: true`. Sets `ChangeLog` (`Fixed -> Flexible`, `6h -> 54h`). Sets `HasPendingLocSync = true`. | `ERP.Attendance.WorkTemplates` |
| **2.5** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/flexi/{id}` | `{id}` *(No `locationId`)* | `flexibleType: "Weekly"`<br>`totalWorkDurationInMinutes: 3240`<br>`flexiTimeSlots: [days only]` | **HTTP 200**: Staged edit creates **Version 3.0** (`_id: 718b74a7-...`). Marks v2.0 `IsSuperseded: true`. Stores `FlexibleType: 2`. Sets `ChangeLog` (`ChangeType: 8` "Updated"). Sets `HasPendingLocSync = true`. | `ERP.Attendance.WorkTemplates` |
| **2.6** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/split/{id}` | `{id}` *(No `locationId`)* | `splitTimeSlots: [...]` | **HTTP 200**: Staged edit creates **Version 4.0** with Split shift configuration. | `ERP.Attendance.WorkTemplates` |
| **2.7** | `GET` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/company-default/sync-status` | None | None | **HTTP 200**: Returns `{ hasPendingLocSync: true }` when CDWT has unsynced major versions. | `ERP.Attendance.WorkTemplates` |
| **2.8** | `POST` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/apply-sync` | None | None | **HTTP 200**: Pushes active version down to all inheriting location templates. Sets `HasPendingLocSync = false`. | `ERP.Attendance.WorkTemplates` |
| **2.9** | `GET` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/company-default/versions` | None | None | **HTTP 200**: Returns full version chain descending: `[v3.0 (isCurrent: true), v2.0 (isCurrent: false), v1.0 (isCurrent: false)]`. | `ERP.Attendance.WorkTemplates` |

> [!IMPORTANT] Architectural Distinction: Immutable Versioning vs. In-Place Mutation
> - **Company Default (`LocationId == 000...000`):** Always uses **Immutable Versioning**. Every PATCH creates a brand new MongoDB document with an incremented major version number (`1.0` $\\rightarrow$ `2.0` $\\rightarrow$ `3.0`), archives the prior document, and tracks all delta messages in `ChangeLog`.
> - **Location Work Template (`LocationId != 000...000`):** Always modifies the **exact same MongoDB document in-place**. The `_id` is retained, no new documents are created, and `Version` remains `1.0`.

---

"""

updated_text = text[:start_idx] + new_step2 + text[end_idx:]

with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'w', encoding='utf-8') as f:
    f.write(updated_text)

print("Successfully updated Step 2 in Attendance_API_Endpoints_and_Testing_Guide.md!")

