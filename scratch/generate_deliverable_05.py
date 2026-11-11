import json, os, sys

sys.stdout.reconfigure(encoding='utf-8')

master_suite = json.load(open('scratch/full_master_suite_results.json', encoding='utf-8'))
split_tests = [t for t in master_suite if t.get('suite') == 'Split']

out_path = r"reports/SPLIT_WORK_TEMPLATE_TEST_CASES.md"

md = []
md.append("# Sahab ERP Attendance – Split Work Template Test Suite Specification & Execution Log")
md.append("\n**Document Version:** `1.0`  ")
md.append("**Execution Date:** `2026-11-10`  ")
md.append("**Module:** Split Work Template (`TemplateType: 3`)  ")
md.append("**Target Location:** Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`)  ")
md.append(f"**Total Scenarios:** `{len(split_tests)}` | **Passed:** `{sum(1 for t in split_tests if t.get('passed'))}` | **Failed:** `{sum(1 for t in split_tests if not t.get('passed'))}`  ")
md.append("**Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`  ")
md.append("**Visual Evidence:** [Evidence 56 (Flexible & Split Template Validation Bypasses & Transitions)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)  ")
md.append("\n---\n")

md.append("## 1. Module Overview & Technical Architecture")
md.append("\nA **Split Work Template** (`TemplateType: 3`) accommodates shifts structured into multiple active work sessions separated by mandatory non-working break windows (e.g., Morning Shift: 08:00–12:00, Break: 12:00–14:00, Afternoon Shift: 14:00–18:00).")
md.append("\n### Key Domain Properties:")
md.append("- `templateType`: Integer `3` (Split).")
md.append("- `splitTimeSlots`: Array of 7 weekday rows.")
md.append("- `timeSlots`: Array of interval objects embedded within each working day slot. Each interval contains `startTime`, `endTime`, and `workDurationInMinutes`.")
md.append("- **Mathematical Invariant:** `slot.workDurationInMinutes` must equal the sum of durations of all child intervals inside `timeSlots`.")
md.append("- **Interval Invariant:** Intervals on the same day cannot overlap and must be strictly chronological.")

md.append("\n---\n")
md.append("## 2. Test Execution Breakdown by Category")

categories = [
    ("Positive POST (Creation of Multi-Interval Split Shifts)", lambda t: t.get('category') == "Positive POST"),
    ("Negative POST (Interval Overlap, Inversion & Sum Guardrails)", lambda t: t.get('category') == "Negative POST"),
    ("Positive PATCH (In-Place Location Mutation)", lambda t: t.get('category') == "Positive PATCH"),
    ("Negative PATCH (Immutability & Validation Gaps)", lambda t: t.get('category') == "Negative PATCH"),
]

for cat_title, filter_fn in categories:
    cat_tests = [t for t in split_tests if filter_fn(t)]
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
            if tid in ["SPL-NEG-10", "SPL-PAT-07"]:
                defect_tag = " **[DEFECT-20261110-13]**"
            elif tid == "SPL-PAT-06":
                defect_tag = " **[DEFECT-20261110-14]**"
        
        md.append(f"| `{tid}` | {notes} | `{method} /worktemplates/split` | `{status}` | {badge} | {notes}{defect_tag} |")

md.append("\n---\n")
md.append("## 3. Detailed Payload & Database Verification Log")

for t in split_tests:
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
