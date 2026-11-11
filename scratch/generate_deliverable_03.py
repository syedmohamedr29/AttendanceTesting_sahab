import json, os, sys

sys.stdout.reconfigure(encoding='utf-8')

fixed_data = json.load(open('scratch/fixed_wt_location_validation_results.json', encoding='utf-8'))

out_path = r"reports/FIXED_WORK_TEMPLATE_TEST_CASES.md"

md = []
md.append("# Sahab ERP Attendance – Fixed Work Template Test Suite Specification & Execution Log")
md.append("\n**Document Version:** `1.0`  ")
md.append("**Execution Date:** `2026-11-10`  ")
md.append("**Module:** Fixed Work Template (`TemplateType: 1`)  ")
md.append("**Target Location:** Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`)  ")
md.append("**Total Scenarios:** `78` | **Passed:** `67` | **Failed / Inconsistencies Caught:** `11`  ")
md.append("**Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`  ")
md.append("**Visual Evidence:** [Evidence 55 (Fixed Work Template Location PATCH Validation Bypasses & DB Results)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)  ")
md.append("\n---\n")

md.append("## 1. Module Overview & Technical Architecture")
md.append("\nA **Fixed Work Template** (`TemplateType: 1`) enforces standardized daily working hours across designated working days with fixed `startTime`, `endTime`, and declared `workDurationInMinutes`. Non-working days have `isWorkingDay: false`, `workDurationInMinutes: 0`, and midnight boundary times (`00:00:00`).")
md.append("\n### Key Domain Properties:")
md.append("- `templateType`: Integer `1` (Fixed).")
md.append("- `fixedTimeSlots`: Array of exactly 7 weekday slots (`dayEnum: 1` [Sunday] to `7` [Saturday]).")
md.append("- `recurrenceOfMonth`: Array of occurrence indices (`[1, 2, 3, 4, 5]`) for active working days; `[]` for off days.")
md.append("- `totalWorkDurationInMinutes`: Total weekly duration (must equal sum of active working slot durations).")
md.append("- `totalWorkingDays` + `totalDaysOff`: Must strictly sum to 7.")

md.append("\n---\n")
md.append("## 2. Test Execution Breakdown by Category")

categories = [
    ("POST Positive (Creation Scenarios)", lambda t: t.get('category') == "POST Positive"),
    ("POST Negative (DTO & Validation Schema Guardrails)", lambda t: t.get('category') == "POST Negative"),
    ("POST Boundary Value Analysis (BVA)", lambda t: "BVA" in t.get('category', '')),
    ("PATCH Positive (In-Place Location Updates)", lambda t: t.get('category') == "PATCH Positive"),
    ("PATCH Negative (In-Place Mutation Guardrails & Bypasses)", lambda t: t.get('category') == "PATCH Negative"),
]

for cat_title, filter_fn in categories:
    cat_tests = [t for t in fixed_data if filter_fn(t)]
    md.append(f"\n### 2.{categories.index((cat_title, filter_fn)) + 1} {cat_title} ({len(cat_tests)} Scenarios)")
    md.append("| Test ID | Description | HTTP Method & URL | Expected | Actual | Result | Notes / Defect |")
    md.append("| :--- | :--- | :--- | :---: | :---: | :---: | :--- |")
    
    for t in cat_tests:
        tid = t.get('test_id')
        notes = t.get('notes', '')
        method = t.get('method', 'POST')
        url = t.get('url', '/api/companies/{companyId}/worktemplates/fixed')
        short_url = url.split('api/companies/')[1] if 'api/companies/' in url else url
        exp = t.get('expected_status', '200')
        act = t.get('status_code')
        passed = t.get('passed')
        badge = "✅ PASS" if passed else "❌ FAIL"
        
        defect_tag = ""
        if not passed:
            if tid == "POST-P09":
                defect_tag = " **[DEFECT-20261110-09]**"
            elif tid in ["BVA16", "BVA17"]:
                defect_tag = " **[DEFECT-20261110-07]**"
            elif tid == "BVA26":
                defect_tag = " **[DEFECT-20261110-08]**"
            elif tid == "PATCH-N06":
                defect_tag = " **[DEFECT-20261110-04]**"
            elif tid == "PATCH-N07":
                defect_tag = " **[DEFECT-20261110-05]**"
            elif tid == "PATCH-N08":
                defect_tag = " **[DEFECT-20261110-06]**"
        
        md.append(f"| `{tid}` | {notes} | `{method} ...{short_url}` | `{exp}` | `{act}` | {badge} | {notes}{defect_tag} |")

md.append("\n---\n")
md.append("## 3. Detailed Payload & Database Verification Log")

# List key interesting tests
key_tests = ["POST-P01", "POST-P09", "N01", "N05", "N10", "BVA16", "BVA17", "BVA26", "PATCH-P01", "PATCH-N06", "PATCH-N07", "PATCH-N08"]
for t in fixed_data:
    if t.get('test_id') in key_tests:
        tid = t.get('test_id')
        md.append(f"\n#### Scenario `{tid}`: {t.get('notes')}")
        md.append(f"- **Endpoint:** `{t.get('method', 'POST')} {t.get('url')}`")
        md.append(f"- **Execution Result:** HTTP `{t.get('status_code')}` (Expected `{t.get('expected_status')}`) -> **{'PASS' if t.get('passed') else 'FAIL'}**")
        if t.get('created_id'):
            md.append(f"- **MongoDB `_id`:** `{t.get('created_id')}`")
        if t.get('error_code') or t.get('error_message'):
            md.append(f"- **API Error Code:** `{t.get('error_code')}` | **Message:** `{t.get('error_message')}`")
        md.append("\n**Request Payload:**")
        md.append("```json")
        md.append(json.dumps(t.get('payload'), indent=2))
        md.append("```")
        md.append("---")

with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print(f"Generated {out_path} successfully. Total lines: {len(md)}")
