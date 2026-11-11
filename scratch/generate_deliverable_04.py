import json, os, sys

sys.stdout.reconfigure(encoding='utf-8')

master_suite = json.load(open('scratch/full_master_suite_results.json', encoding='utf-8'))
flexi_tests = [t for t in master_suite if t.get('suite') == 'Flexible']

out_path = r"reports/FLEXIBLE_WORK_TEMPLATE_TEST_CASES.md"

md = []
md.append("# Sahab ERP Attendance – Flexible Work Template Test Suite Specification & Execution Log")
md.append("\n**Document Version:** `1.0`  ")
md.append("**Execution Date:** `2026-11-10`  ")
md.append("**Module:** Flexible Work Template (`TemplateType: 2`)  ")
md.append("**Target Location:** Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`)  ")
md.append(f"**Total Scenarios:** `{len(flexi_tests)}` | **Passed:** `{sum(1 for t in flexi_tests if t.get('passed'))}` | **Failed:** `{sum(1 for t in flexi_tests if not t.get('passed'))}`  ")
md.append("**Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`  ")
md.append("**Visual Evidence:** [Evidence 56 (Flexible & Split Template Validation Bypasses & Transitions)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)  ")
md.append("\n---\n")

md.append("## 1. Module Overview & Technical Architecture")
md.append("\nA **Flexible (Flexi) Work Template** (`TemplateType: 2`) eliminates fixed check-in/check-out timestamps and evaluates attendance based on completed duration quotas. Flexible templates operate in two distinct modes:")
md.append("1. **Daily Flexible (`FlexibleType: 1`)** — Enforces a specific daily required work duration (e.g., 480 minutes per working day).")
md.append("2. **Weekly Flexible (`FlexibleType: 2`)** — Enforces a cumulative weekly quota (e.g., 2,400 minutes across the working week) where employees can vary daily hours.")
md.append("\n### Key Domain Properties:")
md.append("- `templateType`: Integer `2` (Flexi).")
md.append("- `flexibleType`: Integer `1` (Daily) or `2` (Weekly).")
md.append("- `flexiTimeSlots`: Array of 7 weekday slots containing `dayEnum`, `isWorkingDay`, `workDurationInMinutes`, and `recurrenceOfMonth`.")
md.append("- Does **not** include `startTime` or `endTime` properties in slots.")

md.append("\n---\n")
md.append("## 2. Test Execution Breakdown by Category")

categories = [
    ("Positive POST (Creation of Daily & Weekly Flexi Shifts)", lambda t: t.get('category') == "Positive POST"),
    ("Negative POST (Schema Guardrails & Bypasses)", lambda t: t.get('category') == "Negative POST"),
    ("Positive PATCH (In-Place Location Mutation)", lambda t: t.get('category') == "Positive PATCH"),
    ("Negative PATCH (Immutability & Validation Gaps)", lambda t: t.get('category') == "Negative PATCH"),
]

for cat_title, filter_fn in categories:
    cat_tests = [t for t in flexi_tests if filter_fn(t)]
    md.append(f"\n### 2.{categories.index((cat_title, filter_fn)) + 1} {cat_title} ({len(cat_tests)} Scenarios)")
    md.append("| Test ID | Description | HTTP Method & Endpoint | Status | Result | Notes / Defect Caught |")
    md.append("| :--- | :--- | :--- | :---: | :---: | :--- |")
    for t in cat_tests:
        tid = t.get('test_id')
        notes = t.get('notes', '')
        method = t.get('method')
        status = t.get('status_code')
        passed = t.get('passed')
        badge = "✅ PASS" if passed else "❌ FAIL"
        
        defect_tag = ""
        if not passed:
            if tid in ["FLX-NEG-09", "FLX-PAT-05"]:
                defect_tag = " **[DEFECT-20261110-10]**"
            elif tid in ["FLX-NEG-10", "FLX-PAT-06"]:
                defect_tag = " **[DEFECT-20261110-11]**"
            elif tid == "FLX-PAT-07":
                defect_tag = " **[DEFECT-20261110-12]**"
        
        md.append(f"| `{tid}` | {notes} | `{method} /worktemplates/flexi` | `{status}` | {badge} | {notes}{defect_tag} |")

md.append("\n---\n")
md.append("## 3. Detailed Payload & Database Verification Log")

for t in flexi_tests:
    tid = t.get('test_id')
    md.append(f"\n#### Scenario `{tid}`: {t.get('notes')}")
    md.append(f"- **Endpoint:** `{t.get('method')} {t.get('url')}`")
    md.append(f"- **Execution Result:** HTTP `{t.get('status_code')}` -> **{'PASS' if t.get('passed') else 'FAIL'}**")
    if t.get('created_id'):
        md.append(f"- **MongoDB `_id`:** `{t.get('created_id')}`")
    if t.get('error_code') or t.get('error_message'):
        md.append(f"- **API Error:** `{t.get('error_code')}` | `{t.get('error_message')}`")
    md.append("\n**Request Payload:**")
    md.append("```json")
    md.append(json.dumps(t.get('payload'), indent=2))
    md.append("```")
    md.append("---")

with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print(f"Generated {out_path} successfully. Total lines: {len(md)}")
