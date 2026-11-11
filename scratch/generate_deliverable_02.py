import os, sys

sys.stdout.reconfigure(encoding='utf-8')

out_path = r"defects/WORK_TEMPLATE_DEFECTS.md"
os.makedirs(os.path.dirname(out_path), exist_ok=True)

defects = [
    {
        "id": "DEFECT-20261110-01",
        "severity": "🟠 P1 Critical",
        "title": "Default Work Template Seeding Leaves Arabic Name Blank (`WorkTemplateName.ar: \"\"`) in Seeded Location Documents",
        "endpoint": "POST /api/companies/{companyId}/worktemplates/company-default",
        "method": "POST",
        "db": "Sahab.ERP.Attendance.WorkTemplates",
        "summary": "When creating the Company Default Work Template (CDWT), background seeding automatically replicates the template into company locations. However, while the English name is populated as 'Location Default', the Arabic name `WorkTemplateName.ar` is initialized as empty string `\"\"` instead of inheriting the CDWT Arabic name or using the localized Arabic equivalent.",
        "payload": "{\n  \"templateName\": { \"en\": \"Company Default Shift\", \"ar\": \"الوردية الافتراضية للشركة\" },\n  \"shortCode\": \"CDWT001\",\n  \"templateType\": 1,\n  \"isDefault\": true\n}",
        "response": "HTTP 200 OK | CDWT created, but seeded location document 0ba519c8... has WorkTemplateName.ar: \"\".",
        "impact": "Breaks Arabic UI localization for non-CDWT location templates and violates bilingual data integrity mandates in KSA.",
        "remediation": "In WorkTemplateSeeder.cs, copy both localized properties:\n`locationTemplate.WorkTemplateName = new LocalizedString(cdwt.WorkTemplateName.En, cdwt.WorkTemplateName.Ar ?? cdwt.WorkTemplateName.En);`",
        "evidence": "Evidence 51 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_51_location_default_worktemplate_ar_name_empty_compass.png)"
    },
    {
        "id": "DEFECT-20261110-02",
        "severity": "🟠 P1 Critical",
        "title": "Editing Company Default Work Template Leaves Location Templates Unsynchronized (`HasPendingLocSync: true`)",
        "endpoint": "PATCH /api/companies/{companyId}/worktemplates/company-default/{id}",
        "method": "PATCH",
        "db": "Sahab.ERP.Attendance.WorkTemplates",
        "summary": "Editing CDWT saves a new version (Version 2.0). Locations linked to CDWT are marked with HasPendingLocSync: true, but the background cascade worker fails to propagate the schedule updates down to the location templates, leaving them stuck with HasPendingLocSync: true indefinitely.",
        "payload": "{\n  \"templateName\": { \"en\": \"Updated CDWT\", \"ar\": \"الوردية المحدثة\" },\n  \"totalWorkDurationInMinutes\": 2160,\n  \"totalWorkingDays\": 4,\n  \"totalDaysOff\": 3\n}",
        "response": "HTTP 200 OK | New CDWT version created with HasPendingLocSync: true; Location template remains un-updated.",
        "impact": "Location schedules diverge from corporate default shift definitions silently without administrator notification.",
        "remediation": "In CascadeWorkTemplateUpdateJob.cs, ensure background consumer processes LocationSyncQueue messages and updates linked location documents.",
        "evidence": "Evidence 52 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_52_cdwt_edit_cascade_failure_haspendinglocsync_true_compass.png)"
    },
    {
        "id": "DEFECT-20261110-03",
        "severity": "🟠 P1 Critical",
        "title": "In-Place Location Work Template PATCH Wipes Out Creation Audit Metadata (`CreatedAt: 0001-01-01T00:00:00.000Z`, `CreatedBy: null`)",
        "endpoint": "PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}",
        "method": "PATCH",
        "db": "Sahab.ERP.Attendance.WorkTemplates",
        "summary": "When editing a location-level work template in-place via PATCH, the update pipeline instantiates a fresh entity or maps without preserving existing audit fields, overwriting CreatedAt with DateTime.MinValue (0001-01-01T00:00:00.000Z) and CreatedBy with null in MongoDB.",
        "payload": "{\n  \"shortCode\": \"LOC0001\",\n  \"templateType\": 1,\n  \"totalWorkDurationInMinutes\": 2695,\n  \"fixedTimeSlots\": [...]\n}",
        "response": "HTTP 200 OK | Document 0ba519c8... in MongoDB now shows CreatedAt: '0001-01-01T00:00:00.000Z' and CreatedBy: null.",
        "impact": "Irreversible audit trail corruption. Violates enterprise compliance and auditability invariants.",
        "remediation": "In WorkTemplateRepository.UpdateAsync, use MongoDB `$set` operator for mutable fields only, preserving CreatedAt and CreatedBy.",
        "evidence": "Evidence 54 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png)"
    },
    {
        "id": "DEFECT-20261110-04",
        "severity": "🟠 P1 Critical",
        "title": "Fixed Work Template PATCH Validation Bypass — Accepts Out-of-Range Monthly Recurrence Index 6 (`recurrenceOfMonth: [6]`) with HTTP 200 OK",
        "endpoint": "PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}",
        "method": "PATCH",
        "db": "Sahab.ERP.Attendance.WorkTemplates",
        "summary": "Monthly recurrence is bounded to values 1 to 5. PATCH /worktemplates/fixed accepts recurrenceOfMonth: [6] and updates MongoDB document c9e00652... with [6] without validation error.",
        "payload": "{\n  \"shortCode\": \"FXL0101\",\n  \"fixedTimeSlots\": [ { \"recurrenceOfMonth\": [6], \"dayEnum\": 1, \"isWorkingDay\": true, ... } ]\n}",
        "response": "HTTP 200 OK | MongoDB document c9e00652... updated with RecurrenceOfMonth: [6].",
        "impact": "Breaks schedule evaluation engine since no calendar month has a 6th occurrence of any day.",
        "remediation": "In UpdateFixedWorkTemplateValidator, add RuleForEach on recurrenceOfMonth with InclusiveBetween(1, 5).",
        "evidence": "Evidence 55 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)"
    },
    {
        "id": "DEFECT-20261110-05",
        "severity": "🟠 P1 Critical",
        "title": "Fixed Work Template PATCH Validation Bypass — Accepts Mismatched Total Work Duration (3000m vs 2700m Slot Sum) with HTTP 200 OK",
        "endpoint": "PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}",
        "method": "PATCH",
        "db": "Sahab.ERP.Attendance.WorkTemplates",
        "summary": "PATCH payload declared totalWorkDurationInMinutes: 3000 against a slot sum of 2,700m (5 days * 540m). PATCH succeeded with HTTP 200 OK and overwrote MongoDB with TotalWorkDurationInMinutes: 3000.0.",
        "payload": "{\n  \"totalWorkDurationInMinutes\": 3000,\n  \"fixedTimeSlots\": [ 5 working days * 540 min = 2700 min ]\n}",
        "response": "HTTP 200 OK | Declared 3000 persisted into MongoDB despite mathematical contradiction.",
        "impact": "Corrupts payroll calculations, shift duration totals, and weekly attendance threshold evaluations.",
        "remediation": "In UpdateFixedWorkTemplateValidator, enforce TotalWorkDurationInMinutes == sum of working slot durations.",
        "evidence": "Evidence 55 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)"
    },
    {
        "id": "DEFECT-20261110-06",
        "severity": "🟠 P1 Critical",
        "title": "Fixed Work Template PATCH Validation Bypass — Accepts Arbitrary / Invalid Timezone String ('Invalid/Timezone') with HTTP 200 OK",
        "endpoint": "PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}",
        "method": "PATCH",
        "db": "Sahab.ERP.Attendance.WorkTemplates",
        "summary": "Submitting timeZoneId: 'Invalid/Timezone' via PATCH /worktemplates/fixed returned HTTP 200 OK and updated MongoDB document c9e00652... with the bogus timezone string.",
        "payload": "{\n  \"shortCode\": \"FXL0101\",\n  \"timeZoneId\": \"Invalid/Timezone\",\n  \"fixedTimeSlots\": [...]\n}",
        "response": "HTTP 200 OK | Saved TimeZoneId: 'Invalid/Timezone' directly into MongoDB.",
        "impact": "Causes unhandled TimeZoneNotFoundException in attendance punch calculation workers.",
        "remediation": "In UpdateFixedWorkTemplateValidator, validate TimeZoneId with TimeZoneInfo.TryFindSystemTimeZoneById.",
        "evidence": "Evidence 55 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)"
    },
    {
        "id": "DEFECT-20261110-07",
        "severity": "🟠 P1 Critical",
        "title": "Fixed Work Template POST Boundary Validation Gap — Accepts Out-of-Range Recurrence Values [0] and [6] on Working Days with HTTP 200 OK",
        "endpoint": "POST /api/companies/{companyId}/worktemplates/fixed?locationId={locationId}",
        "method": "POST",
        "db": "Sahab.ERP.Attendance.WorkTemplates",
        "summary": "POST /worktemplates/fixed accepts boundary invalid recurrence values [0] (BVA16) and [6] (BVA17) on working days with HTTP 200 OK and creates permanent documents 9605711d... and 6382798d... in MongoDB.",
        "payload": "{\n  \"shortCode\": \"BVBVA16\",\n  \"fixedTimeSlots\": [ { \"recurrenceOfMonth\": [0], ... } ]\n}",
        "response": "HTTP 200 OK | Documents created in MongoDB with corrupt recurrence arrays.",
        "impact": "Corrupts work plan generation. Month recurrence values outside 1..5 break schedule calculation.",
        "remediation": "In CreateFixedWorkTemplateValidator, add RuleForEach on RecurrenceOfMonth to be InclusiveBetween(1, 5).",
        "evidence": "Evidence 55 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)"
    },
    {
        "id": "DEFECT-20261110-08",
        "severity": "🟡 P2 Major",
        "title": "Fixed Work Template POST Boundary Validation Gap — Accepts Continuous Work Duration of 10,080 Minutes (Full Week Continuous Working) with HTTP 200 OK",
        "endpoint": "POST /api/companies/{companyId}/worktemplates/fixed?locationId={locationId}",
        "method": "POST",
        "db": "Sahab.ERP.Attendance.WorkTemplates",
        "summary": "In test case BVA26, a 168-hour continuous weekly schedule (totalWorkDurationInMinutes: 10080) was submitted. The POST endpoint returned HTTP 200 OK and created document 40ac02d3... in MongoDB without sanity check.",
        "payload": "{\n  \"shortCode\": \"BVBVA26\",\n  \"totalWorkDurationInMinutes\": 10080,\n  \"fixedTimeSlots\": [ 7 working days * 1440 min = 10080 min ]\n}",
        "response": "HTTP 200 OK | Created document in MongoDB with 10,080 minutes duration.",
        "impact": "Violates Saudi Labour Law maximum weekly hour caps (Art. 98) and common sense human limits.",
        "remediation": "Add upper boundary rule: RuleFor(x => x.TotalWorkDurationInMinutes).LessThanOrEqualTo(3600).",
        "evidence": "Evidence 55 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)"
    },
    {
        "id": "DEFECT-20261110-09",
        "severity": "🟡 P2 Major",
        "title": "Location Work Template Hard Quota Enforced at 20 Templates with `Cit.Attendance:1203 Location maximum limit reached.`",
        "endpoint": "POST /api/companies/{companyId}/worktemplates/fixed?locationId={locationId}",
        "method": "POST",
        "db": "Sahab.ERP.Attendance.WorkTemplates",
        "summary": "When creating the 21st work template for Location 1, the API blocked creation with HTTP 400 Bad Request and error Cit.Attendance:1203. No quota information is available via GET worktemplates or in the Web UI.",
        "payload": "POST /worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614 (Attempt 21)",
        "response": "HTTP 400 Bad Request | {\"error\": {\"code\": \"Cit.Attendance:1203\", \"message\": \"Location maximum limit reached.\"}}",
        "impact": "Blocks enterprise operational scaling. Administrators cannot anticipate when a location is full.",
        "remediation": "Expose quota capacity metadata in GET worktemplates and show capacity warnings in Web UI.",
        "evidence": "Evidence 55 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)"
    },
    {
        "id": "DEFECT-20261110-10",
        "severity": "🟠 P1 Critical",
        "title": "Flexible Work Template POST & PATCH Validation Bypass — Accepts Out-of-Range Monthly Recurrence Index 6 (`recurrenceOfMonth: [6]`) with HTTP 200 OK",
        "endpoint": "POST & PATCH /api/companies/{companyId}/worktemplates/flexi",
        "method": "POST & PATCH",
        "db": "Sahab.ERP.Attendance.WorkTemplates",
        "summary": "Both POST /worktemplates/flexi (FLX-NEG-09) and PATCH /worktemplates/flexi/{id} (FLX-PAT-05) accept recurrenceOfMonth: [6] on working days and return HTTP 200 OK, persisting [6] in documents 0ee23f7d... and 7ecfbe95... in MongoDB.",
        "payload": "{\n  \"shortCode\": \"FXDNEG9\",\n  \"flexiTimeSlots\": [ { \"recurrenceOfMonth\": [6], \"workDurationInMinutes\": 480, ... } ]\n}",
        "response": "HTTP 200 OK | Documents persisted in MongoDB with RecurrenceOfMonth: [6].",
        "impact": "Roster generation fails for the 6th occurrence because no 6th weekday exists in any month.",
        "remediation": "In CreateFlexiWorkTemplateValidator and UpdateFlexiWorkTemplateValidator, enforce recurrence index between 1 and 5.",
        "evidence": "Evidence 56 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)"
    },
    {
        "id": "DEFECT-20261110-11",
        "severity": "🟠 P1 Critical",
        "title": "Flexible Work Template POST & PATCH Validation Bypass — Accepts Mismatched Total Work Duration with HTTP 200 OK",
        "endpoint": "POST & PATCH /api/companies/{companyId}/worktemplates/flexi",
        "method": "POST & PATCH",
        "db": "Sahab.ERP.Attendance.WorkTemplates",
        "summary": "POST declared 3000m against 2400m slot sum (FLX-NEG-10), and PATCH declared 3500m against 2700m slot sum (FLX-PAT-06). Both returned HTTP 200 OK and saved corrupt totals in MongoDB.",
        "payload": "{\n  \"totalWorkDurationInMinutes\": 3000,\n  \"flexiTimeSlots\": [ 5 working days * 480 min = 2400 min ]\n}",
        "response": "HTTP 200 OK | Overrode database with TotalWorkDurationInMinutes: 3000.0.",
        "impact": "Breaks timesheet reconciliation and creates inaccurate payroll overtime/shortage amounts.",
        "remediation": "In CreateFlexiWorkTemplateValidator and UpdateFlexiWorkTemplateValidator, enforce TotalWorkDurationInMinutes equals sum of slot durations.",
        "evidence": "Evidence 56 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)"
    },
    {
        "id": "DEFECT-20261110-12",
        "severity": "🟠 P1 Critical",
        "title": "Flexible Work Template PATCH Validation Bypass — Accepts Arbitrary / Invalid Timezone String ('Invalid/Timezone') with HTTP 200 OK",
        "endpoint": "PATCH /api/companies/{companyId}/worktemplates/flexi/{id}?locationId={locationId}",
        "method": "PATCH",
        "db": "Sahab.ERP.Attendance.WorkTemplates",
        "summary": "Submitting timeZoneId: 'Invalid/Timezone' via PATCH /worktemplates/flexi/{id} returned HTTP 200 OK and persisted TimeZoneId: 'Invalid/Timezone' into document 7ecfbe95... in MongoDB.",
        "payload": "{\n  \"shortCode\": \"FXD0001\",\n  \"timeZoneId\": \"Invalid/Timezone\",\n  \"flexiTimeSlots\": [...]\n}",
        "response": "HTTP 200 OK | Saved unvalidated string directly into MongoDB.",
        "impact": "Punch processing workers crash with TimeZoneNotFoundException.",
        "remediation": "In UpdateFlexiWorkTemplateValidator, validate TimeZoneId with TimeZoneInfo.TryFindSystemTimeZoneById.",
        "evidence": "Evidence 56 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)"
    },
    {
        "id": "DEFECT-20261110-13",
        "severity": "🟠 P1 Critical",
        "title": "Split Work Template POST & PATCH Validation Bypass — Accepts Mismatched Total Work Duration with HTTP 200 OK",
        "endpoint": "POST & PATCH /api/companies/{companyId}/worktemplates/split",
        "method": "POST & PATCH",
        "db": "Sahab.ERP.Attendance.WorkTemplates",
        "summary": "POST declared 3000m against 2400m interval sum (SPL-NEG-10), and PATCH declared 3200m against 2400m interval sum (SPL-PAT-07). Both succeeded with HTTP 200 OK without interval sum validation.",
        "payload": "{\n  \"totalWorkDurationInMinutes\": 3000,\n  \"splitTimeSlots\": [ 5 working days * 2 intervals of 240m = 2400m ]\n}",
        "response": "HTTP 200 OK | Persisted 3000.0 into MongoDB despite mathematical contradiction.",
        "impact": "Corrupts shift interval balancing and breaks weekly payroll aggregation.",
        "remediation": "In CreateSplitWorkTemplateValidator and UpdateSplitWorkTemplateValidator, enforce TotalWorkDurationInMinutes equals sum of split interval durations.",
        "evidence": "Evidence 56 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)"
    },
    {
        "id": "DEFECT-20261110-14",
        "severity": "🟠 P1 Critical",
        "title": "Split Work Template PATCH Validation Bypass — Accepts Out-of-Range Monthly Recurrence Index 6 (`recurrenceOfMonth: [6]`) with HTTP 200 OK",
        "endpoint": "PATCH /api/companies/{companyId}/worktemplates/split/{id}?locationId={locationId}",
        "method": "PATCH",
        "db": "Sahab.ERP.Attendance.WorkTemplates",
        "summary": "Submitting recurrenceOfMonth: [6] in PATCH /worktemplates/split/{id} (SPL-PAT-06) returned HTTP 200 OK and mutated document ab6bb972... in MongoDB with RecurrenceOfMonth: [6].",
        "payload": "{\n  \"shortCode\": \"SPD0001\",\n  \"splitTimeSlots\": [ { \"recurrenceOfMonth\": [6], \"timeSlots\": [...] } ]\n}",
        "response": "HTTP 200 OK | Saved RecurrenceOfMonth: [6] directly into MongoDB.",
        "impact": "Causes downstream scheduling failure due to impossible 6th recurrence in a calendar month.",
        "remediation": "In UpdateSplitWorkTemplateValidator, enforce recurrence index between 1 and 5.",
        "evidence": "Evidence 56 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)"
    }
]

md = []
md.append("# Sahab ERP Attendance – Work Template Module Defect Log")
md.append("\n**Document Version:** `1.0`  ")
md.append("**Execution Date:** `2026-11-10`  ")
md.append("**Total Defects Documented:** `14` (12 P1 Critical, 2 P2 Major)  ")
md.append("**Target Environment:** `DEV (attendance2.dev.zoolwork.com)`  ")
md.append("**Target Company:** `Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)`  ")
md.append("**Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`  ")
md.append("\n---\n")

md.append("## 1. Executive Defect Summary Table")
md.append("| Defect ID | Severity | Module / Sub-Feature | Endpoint & Method | Defect Title | Visual Evidence |")
md.append("| :--- | :---: | :--- | :--- | :--- | :--- |")
for d in defects:
    md.append(f"| [`{d['id']}`](#{d['id'].lower()}) | {d['severity']} | Work Templates | `{d['method']} {d['endpoint'].split('?')[0]}` | {d['title']} | [{d['evidence'].split('(')[0].strip()}]({d['evidence'].split('(')[1].rstrip(')')}) |")

md.append("\n---\n")
md.append("## 2. Comprehensive Defect Dossiers")

for d in defects:
    md.append(f"\n### <a id=\"{d['id'].lower()}\"></a>🔴 {d['id']}: {d['title']}")
    md.append(f"\n| Field | Value |")
    md.append(f"| :--- | :--- |")
    md.append(f"| **Defect ID** | `{d['id']}` |")
    md.append(f"| **Severity** | **{d['severity']}** |")
    md.append(f"| **API Endpoint** | `{d['endpoint']}` |")
    md.append(f"| **HTTP Method** | `{d['method']}` |")
    md.append(f"| **Target Collection** | `{d['db']}` |")
    md.append(f"| **Visual Evidence** | [{d['evidence'].split('(')[0].strip()}]({d['evidence'].split('(')[1].rstrip(')')}) |")
    
    md.append("\n#### 1. Detailed Description & Root Cause Analysis")
    md.append(d['summary'])
    
    md.append("\n#### 2. Tested Payload & Live API Response")
    md.append("```json")
    md.append(d['payload'])
    md.append("```")
    md.append(f"**Live API Response:** `{d['response']}`")
    
    md.append("\n#### 3. Business & Data Integrity Impact")
    md.append(d['impact'])
    
    md.append("\n#### 4. Recommended Developer Remediation (.NET 9 C# / FluentValidation)")
    md.append(f"```csharp\n{d['remediation']}\n```")
    md.append("\n---")

with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print(f"Generated {out_path} successfully. Total lines: {len(md)}")
