import sys

sys.stdout.reconfigure(encoding='utf-8')

file1 = "Defects/Attendance2_Master_Defect_Log.md"
file2 = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

# -------------------------------------------------------------------------
# 1. Update Defects/Attendance2_Master_Defect_Log.md
# -------------------------------------------------------------------------
with open(file1, "r", encoding="utf-8") as f:
    text1 = f.read()

text1 = text1.replace("**Date:** **07 November 2026**", "**Date:** **10 November 2026**")
text1 = text1.replace("(All 68 Defects)", "(All 69 Defects)")

# Quick Reference Table: Add DEFECT-20261110-01 above DEFECT-20261107-02
target_tbl = "| [`DEFECT-20261107-02`](#defect-20261107-02) |"
new_tbl_row = """| [`DEFECT-20261110-01`](#defect-20261110-01) | 🟠 P1 | Work Template / Auto-Provisioning & Localization | Auto-Seeded Location Default Work Template Created With Missing / Blank Arabic Name (`WorkTemplateName.ar: ""`) in MongoDB Upon CDWT Creation | ``POST /worktemplates/fixed`` (CDWT Seeding) | [Evidence 51](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_51_location_default_worktemplate_ar_name_empty_compass.png) |
| [`DEFECT-20261107-02`](#defect-20261107-02) |"""

if target_tbl in text1:
    text1 = text1.replace(target_tbl, new_tbl_row)
    print("Added DEFECT-20261110-01 to Quick Reference Table in Master Defect Log.")
else:
    print("Warning: target_tbl not found in Master Defect Log.")

# Detailed section: Add DEFECT-20261110-01 before DEFECT-20261107-02
target_detail = '### <a id="defect-20261107-02"></a>🟡 DEFECT-20261107-02:'

detail_1001 = """### <a id="defect-20261110-01"></a>🔴 DEFECT-20261110-01: Auto-Seeded Location Default Work Template Created With Missing / Blank Arabic Name (`WorkTemplateName.ar: ""`) in MongoDB Upon CDWT Creation

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-01` |
| **Severity** | 🟠 **P1 Critical** (Data Integrity, Multilingual Invariant Breach & Auto-Provisioning Seeding Gap) |
| **Module / Sub-Feature** | Module 2: Work Template & Location Cascade / Shift & Rotation Template Provisioning |
| **API Endpoints** | `POST /api/companies/{companyId}/worktemplates/fixed` (CDWT Creation Triggering Location Seeding) |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Target Location Tested** | Location1 (`3a24d629-0d56-a428-baa1-98493a77e614`) |
| **Visual Evidence** | [Evidence 51 (Seeded Location Work Template Missing Arabic Name in MongoDB)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_51_location_default_worktemplate_ar_name_empty_compass.png)<br>*(User Verification Screenshot: [evidence_51_user_location_default_ar_name_empty.jpg](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_51_user_location_default_ar_name_empty.jpg))* |
| **Status** | **OPEN / CONFIRMED ON DEV ENVIRONMENT** |

#### 1. Issue Description & Live Evidence
During live MongoDB Compass verification on Company **Attendance 8** (`3a249871-7a8d-dec5-2d72-47795dd2662d`):
1. **Background Provisioning / Seeding Trigger:**
   When a Company Default Work Template (CDWT) is created, `SP.AttendanceSvc` background provisioning worker automatically creates (seeds) location-level default templates for all company locations (with `IsCompanyLinked = true` and `IsDefault = false`).
2. **Missing Arabic Name in Seeded Template:**
   Direct inspection of target document in collection `Sahab.ERP.Attendance.WorkTemplates` for Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`) reveals:
   ```json
   {
     "CompanyId": UUID("3a249871-7a8d-dec5-2d72-47795dd2662d"),
     "CompanyName": {
       "en": "Attendance 8",
       "ar": "الحضور 8"
     },
     "LocationId": UUID("3a24d629-0d56-a428-baa1-98493a77e614"),
     "LocationName": {
       "en": "Location1",
       "ar": "الموقع 1"
     },
     "WorkTemplateName": {
       "en": "Location Default",
       "ar": ""   <--- CRITICAL DEFECT: ARABIC NAME IS AN EMPTY STRING ""!
     },
     "IsCompanyLinked": true,
     "IsDefault": false,
     "TemplateType": 1
   }
   ```
3. **Multilingual Architecture Violation:**
   - While `LocationName` is properly multilingual (`en: "Location1"`, `ar: "الموقع 1"`), the auto-seeded `WorkTemplateName` has only the English string `"Location Default"` while `ar` is persisted as an empty string `""`.
   - In the Arabic UI (`ar-SA`), the location template renders with blank title text, breaking shift rotation assignments, roster scheduling, and employee work plan mapping.

#### 2. Photographic Proof & Evidence
| Evidence Image Preview | Live Verification Reference |
| :---: | :--- |
| ![DEFECT-20261110-01](../defect_evidence/evidence_51_location_default_worktemplate_ar_name_empty_compass.png) | **File:** `evidence_51_location_default_worktemplate_ar_name_empty_compass.png`<br><br>[🔍 Click to Open Full-Resolution Image](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_51_location_default_worktemplate_ar_name_empty_compass.png)<br><br>*Evidence 51: MongoDB Compass inspection of Sahab.ERP.Attendance.WorkTemplates on Attendance 8. Highlighted in red: WorkTemplateName.ar: "" (empty string) on auto-seeded location template.* |

#### 3. Developer Remediation (.NET 9 C#)
In `WorkTemplateProvisioningService.cs` (or `SeedLocationWorkTemplatesHandler.cs`):
```csharp
// Ensure auto-seeded location template receives valid Arabic localization
template.WorkTemplateName = new MultilingualString
{
    En = !string.IsNullOrWhiteSpace(companyDefault.TemplateName?.En) 
        ? companyDefault.TemplateName.En 
        : "Location Default",
    Ar = !string.IsNullOrWhiteSpace(companyDefault.TemplateName?.Ar) 
        ? companyDefault.TemplateName.Ar 
        : "الدوام الافتراضي للموقع"
};
```
Execute database data-repair update in MongoDB DEV:
```javascript
db.getSiblingDB("Sahab").getCollection("ERP.Attendance.WorkTemplates").updateMany(
    { "WorkTemplateName.ar": "" },
    { $set: { "WorkTemplateName.ar": "الدوام الافتراضي للموقع" } }
);
```

---

"""

if target_detail in text1:
    text1 = text1.replace(target_detail, detail_1001 + target_detail)
    print("Inserted DEFECT-20261110-01 detail into Master Defect Log.")
else:
    print("Warning: target_detail not found in Master Defect Log.")

with open(file1, "w", encoding="utf-8") as f:
    f.write(text1)
print(f"Saved {file1} successfully.")

# -------------------------------------------------------------------------
# 2. Update Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
# -------------------------------------------------------------------------
with open(file2, "r", encoding="utf-8") as f:
    text2 = f.read()

text2 = text2.replace("**Report Last Updated:** **07 November 2026**", "**Report Last Updated:** **10 November 2026**")

# Dashboard table: Add DEFECT-20261110-01 above DEFECT-20261107-02
target_rep_dash = "| **`DEFECT-20261107-02`** |"
new_rep_dash = """| **`DEFECT-20261110-01`** | **🟠 P1 (Localization & Seeding)** | **Work Template Module**<br>(Location Auto-Provisioning) | `ERP.Attendance.WorkTemplates`<br>(`CDWT Auto-Seeding`) | **Auto-Seeded Location Work Template Has Empty Arabic Name (`WorkTemplateName.ar: ""`):** Upon CDWT creation, auto-provisioned location templates set English `"Location Default"` but leave Arabic empty `""` in MongoDB. Breaks Arabic UI shift/roster selectors. | ❌ **FAIL ([Evidence 51](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_51_location_default_worktemplate_ar_name_empty_compass.png))** |
| **`DEFECT-20261107-02`** |"""

if target_rep_dash in text2:
    text2 = text2.replace(target_rep_dash, new_rep_dash, 1)
    print("Added DEFECT-20261110-01 to Dashboard in Report.")
else:
    print("Warning: target_rep_dash not found in Report.")

# Part 3H / Detailed Section in Report
target_rep_detail = "#### Defect `DEFECT-20261107-02`:"
new_rep_detail = """#### Defect `DEFECT-20261110-01`: Auto-Seeded Location Default Work Template Created With Missing / Blank Arabic Name (`WorkTemplateName.ar: ""`) in MongoDB Upon CDWT Creation

- **Severity:** 🟠 **P1 Critical** (Data Integrity, Multilingual Invariant Breach & Auto-Provisioning Seeding Gap)
- **Module / Feature:** Module 2: Work Template & Location Cascade / Shift & Rotation Template Auto-Provisioning
- **Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) | **Target Location:** Location1 (`3a24d629-0d56-a428-baa1-98493a77e614`)
- **Visual Evidence:** [Evidence 51 (Seeded Location Work Template Missing Arabic Name in MongoDB)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_51_location_default_worktemplate_ar_name_empty_compass.png)<br>*(User Verification Screenshot: [evidence_51_user_location_default_ar_name_empty.jpg](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_51_user_location_default_ar_name_empty.jpg))*

##### 1. Problem Description & Direct Evidence Analysis
1. **Auto-Seeding Trigger:** When the Company Default Work Template is created, the system seeds location-level default templates for each company location.
2. **Missing Arabic Name:** MongoDB Compass query `{ CompanyId: UUID("3a249871-7a8d-dec5-2d72-47795dd2662d") }` shows `WorkTemplateName: { en: "Location Default", ar: "" }`. While `LocationName` has `ar: "الموقع 1"`, `WorkTemplateName.ar` is empty string `""`.
3. **Impact:** In the Arabic UI (`ar-SA`), location work template titles display as blank, breaking shift assignment and rotation configuration.

##### 2. Developer Action & Remediation
- In `WorkTemplateProvisioningService.cs`, set `template.WorkTemplateName.Ar` from parent CDWT Arabic name or fallback to `"الدوام الافتراضي للموقع"`.
- Run MongoDB repair script: `db.getCollection("ERP.Attendance.WorkTemplates").updateMany({ "WorkTemplateName.ar": "" }, { $set: { "WorkTemplateName.ar": "الدوام الافتراضي للموقع" } })`.

---

#### Defect `DEFECT-20261107-02`:`"""

if target_rep_detail in text2:
    text2 = text2.replace(target_rep_detail, new_rep_detail)
    print("Added DEFECT-20261110-01 deep-dive to Report.")
else:
    print("Warning: target_rep_detail not found in Report.")

with open(file2, "w", encoding="utf-8") as f:
    f.write(text2)
print("Saved Report successfully.")
