import json, os, sys

sys.stdout.reconfigure(encoding='utf-8')

v1_fixed = json.load(open('scratch/fixed_wt_location_validation_results.json', encoding='utf-8'))
master_suite = json.load(open('scratch/full_master_suite_results.json', encoding='utf-8'))

out_path = r"reports/WORK_TEMPLATE_TEST_EXECUTION.md"

md = []
md.append("# Sahab ERP Attendance – Master Work Template Test Execution Matrix")
md.append("\n**Document Version:** `1.0`  ")
md.append("**Execution Date:** `2026-11-10`  ")
md.append("**Test Environment:** `DEV (attendance2.dev.zoolwork.com)`  ")
md.append("**Target Company:** `Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)`  ")
md.append("**Target Locations:**  ")
md.append("- Location 1: `3a24d629-0d56-a428-baa1-98493a77e614` (Fixed Work Template Suite & Quota Boundary)  ")
md.append("- Location 2: `3a24d646-b3cf-b1d4-61bb-1adf094b52fc` (Flexible, Split & Cross-Type Transition Matrix)  ")
md.append("- Location 3: `3a24d667-0dcc-e3d1-74a3-cbee98168772`  ")
md.append("**Target Database:** MongoDB `10.1.0.4:27018` | Database: `Sahab` | Collection: `ERP.Attendance.WorkTemplates`  ")
md.append("**Visual Evidence Artifacts:**  ")
md.append("- [Evidence 54: Regular Shift Location POST/PATCH Audit Wipeout & Swagger](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png)  ")
md.append("- [Evidence 55: Fixed Work Template Location PATCH Validation Bypasses & DB Results](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)  ")
md.append("- [Evidence 56: Flexible & Split Template Validation Bypasses & Transitions](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)  ")
md.append("\n---\n")

md.append("## 1. Executive Summary & Test Metrics")
md.append("\nThis master test execution suite represents complete end-to-end automated verification of the **Sahab ERP Attendance Work Template API and MongoDB persistence engine**. Testing encompasses all three supported shift template architectures:")
md.append("1. **Fixed Work Template (`TemplateType: 1`)** — Uniform recurring schedules with fixed start/end times and daily durations.")
md.append("2. **Flexible Work Template (`TemplateType: 2`)** — Target work hour quotas evaluated on Daily (`FlexibleType: 1`) or Weekly (`FlexibleType: 2`) recurrence.")
md.append("3. **Split Work Template (`TemplateType: 3`)** — Multiple distinct work intervals separated by mandatory breaks per working day.")
md.append("\n### High-Level Metrics Summary")
md.append("| Suite / Category | Total Scenarios | Passed / Expected | Failed / Defect Caught | Pass Rate | Primary Architectural Invariant / Finding |")
md.append("| :--- | :---: | :---: | :---: | :---: | :--- |")
md.append("| **Fixed: Positive POST** | 9 | 8 | 1 | 88.9% | Hits 20-template quota limit (`Cit.Attendance:1203`) at P09 |")
md.append("| **Fixed: Negative POST** | 23 | 23 | 0 | 100.0% | Strict FluentValidation on missing fields, shortCode format, DTO schema |")
md.append("| **Fixed: Boundary Value Analysis** | 26 | 23 | 3 | 88.5% | Validation gap on recurrence `[0]`, `[6]`, and 10,080 min duration |")
md.append("| **Fixed: Positive PATCH** | 8 | 8 | 0 | 100.0% | In-place location update preserves `_id` & `Version: \"1.0\"` |")
md.append("| **Fixed: Negative PATCH** | 12 | 9 | 3 | 75.0% | Validation bypass on recurrence `[6]`, duration mismatch, invalid timezone |")
md.append("| **Flexible: Positive POST** | 5 | 5 | 0 | 100.0% | Daily and Weekly flexi templates create with `TemplateType: 2` |")
md.append("| **Flexible: Negative POST** | 10 | 8 | 2 | 80.0% | Bypasses recurrence `[6]` and duration sum mismatch |")
md.append("| **Flexible: Positive PATCH** | 3 | 3 | 0 | 100.0% | In-place flexi mutation preserves `_id` & updates `FlexibleType` |")
md.append("| **Flexible: Negative PATCH** | 4 | 1 | 3 | 25.0% | Bypasses recurrence `[6]`, duration mismatch, and invalid timezone |")
md.append("| **Split: Positive POST** | 5 | 5 | 0 | 100.0% | Multiple split intervals persist under `splitTimeSlots[].timeSlots` |")
md.append("| **Split: Negative POST** | 10 | 9 | 1 | 90.0% | Catches interval overlap, inversion, zero gap; bypasses total duration |")
md.append("| **Split: Positive PATCH** | 3 | 3 | 0 | 100.0% | In-place split interval reconfiguration succeeds with HTTP 200 OK |")
md.append("| **Split: Negative PATCH** | 4 | 2 | 2 | 50.0% | Locks `shortCode`, catches overlap; bypasses recurrence `[6]` & duration |")
md.append("| **Cross-Type Transitions** | 6 | 6 | 0 | 100.0% | Full polymorphic mutation supported across Fixed $\\leftrightarrow$ Flexi $\\leftrightarrow$ Split |")
md.append("| **GRAND TOTAL** | **128** | **113** | **15** | **88.3%** | **14 New Defect Lifecycles Tracked (`DEFECT-20261110-01` to `14`)** |")

md.append("\n---\n")
md.append("## 2. Master Execution Results Catalog")

# 1. Fixed Suite
md.append("\n### 2.1 Fixed Work Template Suite (Location 1: `3a24d629-0d56-a428-baa1-98493a77e614`)")
md.append("| Test ID | Category | Method & Endpoint | Payload Highlights | Status Code | Result | Key Observations & Defect Link |")
md.append("| :--- | :--- | :--- | :--- | :---: | :---: | :--- |")
for t in v1_fixed:
    tid = t.get('test_id')
    cat = t.get('category')
    method = t.get('method', 'POST')
    status = t.get('status_code')
    passed = t.get('passed')
    res_badge = "✅ PASS" if passed else "❌ FAIL"
    notes = t.get('notes', '')
    payload_str = json.dumps(t.get('payload', {}))[:60] + "..."
    defect_link = ""
    if not passed:
        if tid == "POST-P09":
            defect_link = "<br>[DEFECT-20261110-09](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#defect-20261110-09)"
        elif tid in ["BVA16", "BVA17"]:
            defect_link = "<br>[DEFECT-20261110-07](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#defect-20261110-07)"
        elif tid == "BVA26":
            defect_link = "<br>[DEFECT-20261110-08](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#defect-20261110-08)"
        elif tid == "PATCH-N06":
            defect_link = "<br>[DEFECT-20261110-04](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#defect-20261110-04)"
        elif tid == "PATCH-N07":
            defect_link = "<br>[DEFECT-20261110-05](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#defect-20261110-05)"
        elif tid == "PATCH-N08":
            defect_link = "<br>[DEFECT-20261110-06](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#defect-20261110-06)"
    md.append(f"| `{tid}` | {cat} | `{method} /worktemplates/fixed` | `{payload_str}` | `{status}` | {res_badge} | {notes}{defect_link} |")

# 2. Flexible Suite
md.append("\n### 2.2 Flexible Work Template Suite (Location 2: `3a24d646-b3cf-b1d4-61bb-1adf094b52fc`)")
md.append("| Test ID | Category | Method & Endpoint | Payload Highlights | Status Code | Result | Key Observations & Defect Link |")
md.append("| :--- | :--- | :--- | :--- | :---: | :---: | :--- |")
for t in master_suite:
    if t.get('suite') == 'Flexible':
        tid = t.get('test_id')
        cat = t.get('category')
        method = t.get('method')
        status = t.get('status_code')
        passed = t.get('passed')
        res_badge = "✅ PASS" if passed else "❌ FAIL"
        notes = t.get('notes', '')
        payload_str = json.dumps(t.get('payload', {}))[:60] + "..."
        defect_link = ""
        if not passed:
            if tid in ["FLX-NEG-09", "FLX-PAT-05"]:
                defect_link = "<br>[DEFECT-20261110-10](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#defect-20261110-10)"
            elif tid in ["FLX-NEG-10", "FLX-PAT-06"]:
                defect_link = "<br>[DEFECT-20261110-11](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#defect-20261110-11)"
            elif tid == "FLX-PAT-07":
                defect_link = "<br>[DEFECT-20261110-12](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#defect-20261110-12)"
        md.append(f"| `{tid}` | {cat} | `{method} /worktemplates/flexi` | `{payload_str}` | `{status}` | {res_badge} | {notes}{defect_link} |")

# 3. Split Suite
md.append("\n### 2.3 Split Work Template Suite (Location 2: `3a24d646-b3cf-b1d4-61bb-1adf094b52fc`)")
md.append("| Test ID | Category | Method & Endpoint | Payload Highlights | Status Code | Result | Key Observations & Defect Link |")
md.append("| :--- | :--- | :--- | :--- | :---: | :---: | :--- |")
for t in master_suite:
    if t.get('suite') == 'Split':
        tid = t.get('test_id')
        cat = t.get('category')
        method = t.get('method')
        status = t.get('status_code')
        passed = t.get('passed')
        res_badge = "✅ PASS" if passed else "❌ FAIL"
        notes = t.get('notes', '')
        payload_str = json.dumps(t.get('payload', {}))[:60] + "..."
        defect_link = ""
        if not passed:
            if tid in ["SPL-NEG-10", "SPL-PAT-07"]:
                defect_link = "<br>[DEFECT-20261110-13](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#defect-20261110-13)"
            elif tid == "SPL-PAT-06":
                defect_link = "<br>[DEFECT-20261110-14](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#defect-20261110-14)"
        md.append(f"| `{tid}` | {cat} | `{method} /worktemplates/split` | `{payload_str}` | `{status}` | {res_badge} | {notes}{defect_link} |")

# 4. Cross-Type Transitions
md.append("\n### 2.4 Cross-Type Transition Matrix (Location 2 Polymorphic Mutation)")
md.append("| Transition ID | Source Type | Target Type | Method & Endpoint | HTTP Status | Mutation Integrity | Mongo Discriminator (`_t`) Proof |")
md.append("| :--- | :--- | :--- | :--- | :---: | :---: | :--- |")
md.append("| `TRANS-01` | Fixed (`1`) | Flexible (`2`) | `PATCH /worktemplates/flexi/{id}` | `200 OK` | ✅ Preserves `_id`, Version `1.0` | `['WorkTemplate', 'FlexiWorkTemplate']` |")
md.append("| `TRANS-02` | Fixed (`1`) | Split (`3`) | `PATCH /worktemplates/split/{id}` | `200 OK` | ✅ Preserves `_id`, Version `1.0` | `['WorkTemplate', 'SplitWorkTemplate']` |")
md.append("| `TRANS-03` | Flexible (`2`) | Fixed (`1`) | `PATCH /worktemplates/fixed/{id}` | `200 OK` | ✅ Preserves `_id`, Version `1.0` | `['WorkTemplate', 'FixedWorkTemplate']` (Doc `7ecfbe95`) |")
md.append("| `TRANS-04` | Flexible (`2`) | Split (`3`) | `PATCH /worktemplates/split/{id}` | `200 OK` | ✅ Preserves `_id`, Version `1.0` | `['WorkTemplate', 'SplitWorkTemplate']` (Doc `68dab14c`) |")
md.append("| `TRANS-05` | Split (`3`) | Fixed (`1`) | `PATCH /worktemplates/fixed/{id}` | `200 OK` | ✅ Preserves `_id`, Version `1.0` | `['WorkTemplate', 'FixedWorkTemplate']` (Doc `ab6bb972`) |")
md.append("| `TRANS-06` | Split (`3`) | Flexible (`2`) | `PATCH /worktemplates/flexi/{id}` | `200 OK` | ✅ Preserves `_id`, Version `1.0` | `['WorkTemplate', 'FlexiWorkTemplate']` (Doc `5766c9f3`) |")

md.append("\n---\n")
md.append("## 3. Key Architectural Invariants & Production Findings")
md.append("\n### 3.1 ShortCode Immutability and Exact Length Constraint")
md.append("- **Format Enforcement:** `shortCode` must be exactly 7 alphanumeric characters (`^[a-zA-Z0-9]{7}$`). Values shorter or longer fail with `Cit.Attendance:Validation ShortCode must be exactly 7 letters or digits.`")
md.append("- **Post-Creation Lockout:** Once created, `shortCode` cannot be altered. Any attempt to update `shortCode` in PATCH triggers `Cit.Attendance:1107 A work template's short code cannot be changed after it is created.`")
md.append("- **Scope Uniqueness:** Uniqueness is enforced at the company scope across all locations. Duplicate shortcodes fail with `Cit.Attendance:1106 This short code is already used by another work template in this company.`")

md.append("\n### 3.2 Location Work Template Quota Hard Cap (`Cit.Attendance:1203`)")
md.append("- Each company location is hard-capped at exactly **20 work templates**.")
md.append("- Attempting to add a 21st template (`POST-P09`) returns `HTTP 400 Bad Request` with `Cit.Attendance:1203 Location maximum limit reached.`")
md.append("- No quota visibility is currently surfaced in Swagger or the UI dashboard (`DEFECT-20261110-09`).")

md.append("\n### 3.3 In-Place Location Mutation vs Company-Default Versioning")
md.append("- **Company Default Work Template (CDWT):** Modifying CDWT creates a brand-new immutable MongoDB document with `Version: \"2.0\"`, a new `_id`, and marks the old document as `IsSuperseded: true`.")
md.append("- **Location Work Template:** Editing a location template mutates the existing document **in place** (retains `_id` and `Version: \"1.0\"`). However, this triggers `DEFECT-20261110-03` where `CreatedAt` is wiped out to `0001-01-01T00:00:00.000Z` and `CreatedBy` is reset to `null`.")

md.append("\n### 3.4 Cross-Module Validation Discrepancies")
md.append("- Total work duration declared in the request header (`totalWorkDurationInMinutes`) is not validated against the actual sum of working slot durations during PATCH operations across all three template types (`DEFECT-20261110-05`, `DEFECT-20261110-11`, `DEFECT-20261110-13`).")
md.append("- Monthly recurrence arrays accept out-of-range values `[0]` and `[6]` across Fixed, Flexible, and Split templates (`DEFECT-20261110-04`, `DEFECT-20261110-07`, `DEFECT-20261110-10`, `DEFECT-20261110-14`).")

with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print(f"Generated {out_path} successfully. Total lines: {len(md)}")
