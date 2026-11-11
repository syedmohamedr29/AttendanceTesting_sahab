import sys

md_path = 'Attendance_API_Endpoints_and_Testing_Guide.md'

with open(md_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Step 2 Note
step2_target = """| **2.1** | `POST` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/fixed` | *(No `locationId`)* | `templateName: {"en":"Std"}`<br>`shortCode: "COSTD01"`<br>`fixedTimeSlots: [...]` | **HTTP 200**: CDWT created (`IsDefault: true`). **Auto-provisions** Location Default WT and Default Plan (`LOCWOPL`) for each location. | `ERP.Attendance.WorkTemplates`<br>`ERP.Attendance.WorkPlans` |"""

step2_replacement = """| **2.1** | `POST` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/fixed` | *(No `locationId`)* | `templateName: {"en":"Std"}`<br>`shortCode: "COSTD01"`<br>`fixedTimeSlots: [...]` | **HTTP 200**: CDWT created (`IsDefault: true`). **Auto-provisions** Location Default WT and Default Plan (`LOCWOPL`) for each location. | `ERP.Attendance.WorkTemplates`<br>`ERP.Attendance.WorkPlans`<br>*(Cross-Svc: `CompanyMaster`)* |

> [!WARNING] Critical Cross-Service Integration & Known Defect (`USER-01`)
> * **Expected Behavior:** Upon successful creation of the Company Default Work Schedule, Attendance Service must notify **Company Service** (`SP.CompanySvc`), which must update the company master profile:  
>   `CompanyMaster` collection $\rightarrow$ `CompanyChecklist.WorkSchedulesCreated = true`.
> * **Current Defect Status (Reported by QA):** `CompanyChecklist.WorkSchedulesCreated` remains `false`. The checklist flag is not updated, causing onboarding/setup validation to report incomplete work schedule setup."""

if step2_target in text:
    text = text.replace(step2_target, step2_replacement)
    print("Step 2 callout updated successfully!")
else:
    print("Step 2 target not found!")

# 2. Update External Integrated Services Matrix
ext_target = """| **Company Service** | `https://company8.dev.zoolwork.com` | Master company profiles, location lists, holiday types | `GET /api/company/worklocations/companyWorkLocationList`<br>`GET /api/company/{companyId}/holidaytypes` |"""

ext_replacement = """| **Company Service** | `https://company8.dev.zoolwork.com` | Master company profiles, location lists, onboarding checklist (`CompanyMaster`) | `GET /api/company/worklocations/companyWorkLocationList`<br>`GET /api/company/{companyId}/holidaytypes`<br>`CompanyMaster` collection (`CompanyChecklist.WorkSchedulesCreated`) |"""

if ext_target in text:
    text = text.replace(ext_target, ext_replacement)
    print("External Integrated Services Matrix updated successfully!")
else:
    print("External target not found!")

# 3. Add to Part 4 under Master Data Collections
part4_target = """### Master Data Collections Detail

#### 1. `ERP.Attendance.WorkTemplates`"""

part4_replacement = """### Master Data Collections Detail

#### Cross-Service Impact: `CompanyMaster` (Company Service DB)
> **Owner Service:** `SP.CompanySvc` (Company Service)  
> **Collection:** `CompanyMaster` (or `Companies`)  
> **Key Object / Field:** `CompanyChecklist.WorkSchedulesCreated` (`Boolean`)  
> 
> **Integration Contract:**  
> When the initial Company Default Work Schedule is provisioned in Attendance 2 (`POST /worktemplates/{type}`), an integration event or internal API call must trigger an update in Company Service to mark `CompanyChecklist.WorkSchedulesCreated: true`.  
> 
> **QA Defect Alert (`USER-01`):**  
> In current DEV builds, `CompanyChecklist.WorkSchedulesCreated` is **NOT updated to true** and remains **`false`**. This is a confirmed integration defect tracked under test case `USER-01`.

#### 1. `ERP.Attendance.WorkTemplates`"""

if part4_target in text:
    text = text.replace(part4_target, part4_replacement)
    print("Part 4 cross-service impact added successfully!")
else:
    print("Part 4 target not found!")

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated Attendance_API_Endpoints_and_Testing_Guide.md!")

