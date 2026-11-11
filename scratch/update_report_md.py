import sys

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update TOC (around line 30)
target_toc = "* [**✅ Part 5: Actionable Developer Checklist (Date-Wise)**](#-part-5-actionable-developer-checklist-date-wise) — *Consolidated Engineering Action Items for Khalid's Team*"
new_toc = """* [**🏢 Part 3G: Defects Discovered on 05 November 2026 (WORK TEMPLATE MODULE: EMPTY COMPANYNAME IN MONGO)**](#-part-3g-defects-identified-on-05-november-2026--work-template-module-live-mongodb-compass-verification) — *Live MongoDB Compass Evidence: CompanyName persists as Object (empty) {} upon CDWT creation (DEFECT-20261105-01)*
* [**✅ Part 5: Actionable Developer Checklist (Date-Wise)**](#-part-5-actionable-developer-checklist-date-wise) — *Consolidated Engineering Action Items for Khalid's Team*"""

assert target_toc in content, "target_toc not found"
content = content.replace(target_toc, new_toc, 1)

# 2. Add Critical Defect Logged Today (05 November 2026) banner right above line 34 (## 🚨 Critical & High-Priority Defects Logged Today (03 November 2026))
target_banner = "## 🚨 Critical & High-Priority Defects Logged Today (03 November 2026)"
new_banner = """## 🚨 Critical Defect Logged Today (05 November 2026): DEFECT-20261105-01

> [!WARNING]
> On **05 November 2026**, direct live verification in MongoDB Compass (`DEV > Sahab > ERP.Attendance.WorkTemplates`) for newly onboarded company **Attendance 9** (`3a249872-2d69-f931-41f6-d8db086b09b8`) uncovered photographic proof of a critical master data persistence defect:
> **`CompanyName` Persists as Empty Object (`DEFECT-20261105-01`):** Document `d5abe5c4-d51f-4287-9baf-38e2e4f547c8` shows `CompanyId: UUID('3a249872-2d69-f931-41f6-d8db086b09b8')`, but `CompanyName: Object (empty)` `{}`! The localized company name (`{"en": "Attendance 9", "ar": "الحضور 9"}`) is never resolved from `SP.CompanySvc`, leaving all created templates company-nameless in MongoDB and API responses.
> Full details and Compass screenshot are documented in [**Part 3G**](#-part-3g-defects-identified-on-05-november-2026--work-template-module-live-mongodb-compass-verification).

| Defect ID | Severity / Priority | Layer | Collection / Endpoint | Defect Description | Live Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **`DEFECT-20261105-01`** | **P1 (Master Data Integrity)** | **Work Template Module**<br>(Master Data) | `ERP.Attendance.WorkTemplates`<br>(`POST /worktemplates/*`) | **Work Template: `CompanyName` Persists as `Object (empty)` `{}` in MongoDB:** Creating a CDWT saves `CompanyId`, but `CompanyName` remains empty `{}` in Mongo and API response. Missing metadata resolution from `SP.CompanySvc`. | ❌ **FAIL (COMPASS PROOF)** |

---

## 🚨 Critical & High-Priority Defects Logged on 03 November 2026"""

assert target_banner in content, "target_banner not found"
content = content.replace(target_banner, new_banner, 1)

# 3. Add Evidence 39 to Gallery around line 135
target_gallery = """| `evidence_37`: MongoDB Compass — `ERP.Attendance.WorkTemplates` with Only 4 Documents (Delhi Missing) | `evidence_38`: Web UI — 4 Locations Configured (Chennai, Bangalore, Hyderabad, Delhi) |
| :---: | :---: |
| ![Compass 4 WT Documents](defect_evidence/evidence_37_cdwt_compass_only_4_templates_missing_delhi.jpg) | ![UI 4 Locations](defect_evidence/evidence_38_company_locations_ui_4_locations_including_delhi.png) |
| [🔍 View Evidence 37 (Compass)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_37_cdwt_compass_only_4_templates_missing_delhi.jpg) | [🔍 View Evidence 38 (UI)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_38_company_locations_ui_4_locations_including_delhi.png) |"""

new_gallery = target_gallery + """

| `evidence_39`: MongoDB Compass — `ERP.Attendance.WorkTemplates` Document with `CompanyName: Object (empty)` `{}` |
| :---: |
| ![Compass CompanyName Empty](defect_evidence/evidence_39_companyname_empty_object_compass.jpg) |
| [🔍 View Evidence 39 (Compass)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_39_companyname_empty_object_compass.jpg) |"""

assert target_gallery in content, "target_gallery not found"
content = content.replace(target_gallery, new_gallery, 1)

# 4. Insert Part 3G right before Part 4 (around line 3950)
target_part4 = "# 🔄 Part 4: Standardized Bug Lifecycle Procedure"

part3g_content = """# 🏢 Part 3G: Defects Identified on 05 November 2026 — Work Template Module (Live MongoDB Compass Verification)

> [!IMPORTANT]
> On **05 November 2026**, during fresh company onboarding and Company Default Work Template creation on company **Attendance 9** (`3a249872-2d69-f931-41f6-d8db086b09b8`), direct inspection of document `d5abe5c4-d51f-4287-9baf-38e2e4f547c8` in MongoDB Compass (`ERP.Attendance.WorkTemplates`) provided photographic proof of a critical master data persistence defect.

### Defect `DEFECT-20261105-01`: `CompanyName` Persists as `Object (empty)` `{}` in MongoDB Upon Work Template Creation (Missing Company Metadata Resolution from `SP.CompanySvc`)
- **Severity:** 🟠 **P1 (Critical / Data Integrity & Master Data)**
- **Affected Endpoints:** `POST /api/companies/{companyId}/worktemplates/{fixed|flexi|split}`, `GET /api/companies/{companyId}/worktemplates`
- **Database Target:** `Sahab.ERP.Attendance.WorkTemplates`
- **Live Status:** ❌ **FAIL / OPEN (Verified via MongoDB Compass Evidence 39)**

#### 1. Problem Description
When a Company Default Work Template is created for a company (e.g. `Attendance 9`, `3a249872-2d69-f931-41f6-d8db086b09b8`), `SP.AttendanceSvc` saves `CompanyId: UUID('3a249872-2d69-f931-41f6-d8db086b09b8')`, but leaves `CompanyName` as an unpopulated empty object (`CompanyName: Object (empty)` `{}`).
In addition, the server's HTTP 200 response for `POST /worktemplates/fixed` and `GET /worktemplates/{id}` returns `"companyName": {}`.
Because `SP.AttendanceSvc` never calls `SP.CompanySvc` to fetch the company's English and Arabic names (`{"en": "Attendance 9", "ar": "الحضور 9"}`), the document is stored without human-readable company names, causing broken UI cards and missing company metadata across reports.

#### 2. Photographic Proof from MongoDB Compass (05-Nov-2026)
| MongoDB Compass Visual Evidence | Description |
| :--- | :--- |
| ![DEFECT-20261105-01](defect_evidence/evidence_39_companyname_empty_object_compass.jpg) | **Evidence 39:** Live MongoDB Compass inspection of document `d5abe5c4-d51f-4287-9baf-38e2e4f547c8` on Company `Attendance 9` (`3a249872-2d69-f931-41f6-d8db086b09b8`). Highlighted in red: `CompanyName: Object (empty)`.<br><br>[🔍 Click to Open Full-Resolution Image](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_39_companyname_empty_object_compass.jpg) |

#### 3. Exact Reproduction Request & Response Payload
**Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249872-2d69-f931-41f6-d8db086b09b8/worktemplates/fixed`  
**Request Body:**
```json
{
  "templateName": {
    "en": "Attendance 9 Fixed Template",
    "ar": "قالب الحضور 9 الثابت"
  },
  "shortCode": "ATT9FIX",
  "templateType": 1,
  "totalWorkDurationInMinutes": 480,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "fixedTimeSlots": [
    { "dayEnum": 1, "isWorkingDay": true, "workDurationInMinutes": 480, "startTime": "08:00:00", "endTime": "16:00:00", "recurrenceOfMonth": [1, 2, 3, 4, 5] },
    { "dayEnum": 2, "isWorkingDay": true, "workDurationInMinutes": 480, "startTime": "08:00:00", "endTime": "16:00:00", "recurrenceOfMonth": [1, 2, 3, 4, 5] },
    { "dayEnum": 3, "isWorkingDay": true, "workDurationInMinutes": 480, "startTime": "08:00:00", "endTime": "16:00:00", "recurrenceOfMonth": [1, 2, 3, 4, 5] },
    { "dayEnum": 4, "isWorkingDay": true, "workDurationInMinutes": 480, "startTime": "08:00:00", "endTime": "16:00:00", "recurrenceOfMonth": [1, 2, 3, 4, 5] },
    { "dayEnum": 5, "isWorkingDay": true, "workDurationInMinutes": 480, "startTime": "08:00:00", "endTime": "16:00:00", "recurrenceOfMonth": [1, 2, 3, 4, 5] },
    { "dayEnum": 6, "isWorkingDay": false, "workDurationInMinutes": 0, "startTime": "00:00:00", "endTime": "00:00:00", "recurrenceOfMonth": [1, 2, 3, 4, 5] },
    { "dayEnum": 7, "isWorkingDay": false, "workDurationInMinutes": 0, "startTime": "00:00:00", "endTime": "00:00:00", "recurrenceOfMonth": [1, 2, 3, 4, 5] }
  ]
}
```

**Actual Response Received (HTTP 200 OK):**
```json
{
  "message": "Fixed work template created",
  "template": {
    "id": "d5abe5c4-d51f-4287-9baf-38e2e4f547c8",
    "tenantId": "3a24741e-2667-1223-f12e-62a69fab3838",
    "companyId": "3a249872-2d69-f931-41f6-d8db086b09b8",
    "companyName": {},
    "locationId": "00000000-0000-0000-0000-000000000000",
    "locationName": {},
    "workTemplateName": {
      "en": "Attendance 9 Fixed Template",
      "ar": "قالب الحضور 9 الثابت"
    },
    "shortCode": "ATT9FIX",
    "templateType": "Fixed",
    "status": "Active",
    "version": "1.0",
    "isDefault": true
  }
}
```

#### 4. Technical Root Cause & Architecture Analysis
In `SP.AttendanceSvc` command handlers (`CreateFixedWorkTemplateCommandHandler.cs`, `CreateFlexiWorkTemplateCommandHandler.cs`, `CreateSplitWorkTemplateCommandHandler.cs`):
1. The route `companyId` is bound into the command, but `CompanyName` is never retrieved from `SP.CompanySvc`.
2. The domain entity `WorkTemplate` initialises `CompanyName` as empty or null, resulting in MongoDB serializing an empty BSON document `CompanyName: {}`.
3. In parallel, `TenantName` suffers from the identical issue (`DEFECT-20261026-02` / `DEFECT-20261103-02`).
4. This breaks multi-tenant reporting, cross-service UI aggregations, and data exports.

#### 5. Developer Remediation & C# Code Fix
In `SP.AttendanceSvc`:
1. Use `ICompanyServiceClient` to fetch company localized metadata during template creation:
   ```csharp
   var company = await _companyServiceClient.GetCompanyByIdAsync(request.CompanyId, cancellationToken);
   if (company != null)
   {
       template.CompanyName = new MultilingualString
       {
           En = company.Name?.En ?? string.Empty,
           Ar = company.Name?.Ar ?? string.Empty
       };
   }
   ```
2. Ensure `WorkTemplateDto` projects `CompanyName` to the response DTO.

---

"""

assert target_part4 in content, "target_part4 not found"
content = content.replace(target_part4, part3g_content + target_part4, 1)

# 5. Add checklist item in Part 5 Developer Checklist
target_part5_item = "- [ ] **P1 (`DEFECT-20261103-16`):** In `SP.AttendanceSvc`,"
new_part5_item = """- [ ] **P1 (`DEFECT-20261105-01`):** In `SP.AttendanceSvc`, resolve and populate `CompanyName` (`MultilingualString { En, Ar }`) from `SP.CompanySvc` when creating/updating Work Templates so MongoDB `ERP.Attendance.WorkTemplates` and API responses do not persist `CompanyName: Object (empty)` `{}`.
- [ ] **P1 (`DEFECT-20261103-16`):** In `SP.AttendanceSvc`,"""

assert target_part5_item in content, "target_part5_item not found"
content = content.replace(target_part5_item, new_part5_item, 1)

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md updated successfully!")

