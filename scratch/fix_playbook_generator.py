# -*- coding: utf-8 -*-
import re
import sys

with open('scratch/generate_full_playbook.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the generation loop at the end
old_gen_marker = '# Generate Output Text'
pos = content.find(old_gen_marker)
if pos == -1:
    print("Error: Could not find '# Generate Output Text'")
    sys.exit(1)

cases_def_part = content[:pos]

new_gen_code = '''# Generate Clean, Beautifully Aligned Markdown Playbook (Zero Tables, Real Newlines)
lines = []
lines.append("# Company Default Work Template (CDWT) — Manual Testing Playbook")
lines.append("## Complete Step-by-Step Test Data Guide for All 53 Edge Cases (With Full Request Body Payloads)")
lines.append("")
lines.append("> **Target Microservice:** SP.AttendanceSvc (.NET 9 / ASP.NET Core)  ")
lines.append("> **Base DEV URL:** `https://attendance2.dev.zoolwork.com`  ")
lines.append("> **Auth Server:** `https://auth8.dev.zoolwork.com/connect/token` (tenant: `Attendance`)  ")
lines.append("> **Swagger UI:** `https://attendance2.dev.zoolwork.com/swagger/index.html`  ")
lines.append("> **Excel Workbook:** `CompanyDefault_DTO_Validation_TestCases.xlsx`  ")
lines.append("")
lines.append("### Target Companies for Testing:")
lines.append("- **Company 2 (Attendance 2):** `3a247435-3cea-83ae-6a9f-6dda99f386a3` (Fixed CDWT Active v3.0 `e1a64e28-ecd6-49b5-9155-fd30a11d9e8d`)")
lines.append("- **Company 3 (Attendance 3):** `3a247435-e31d-ef15-8cc9-62c587f4eb3f` (Fixed CDWT Active v2.0 `27aa7562-b833-46f7-9cb7-d65f27171dab`)")
lines.append("- **Company 4 (Attendance 4):** `3a247436-8669-844a-7d2f-1a209af02d8e` (Flexi CDWT Active v2.0 `53470658-5f9b-47b4-b254-f96b9501401c`)")
lines.append("- **Tenant Header:** `__tenant: Attendance`")
lines.append("")

current_cat = None
for c in cases:
    if c["category"] != current_cat:
        current_cat = c["category"]
        lines.append("")
        lines.append(f"# {current_cat.upper()}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(f"## {c['id']}: {c['title']}")
    lines.append("")
    lines.append(f"- **Category:** {c['category']}")
    lines.append(f"- **Priority:** {c['priority']}")
    lines.append(f"- **Method & Route:** `{c['method']} {c['route']}`")
    lines.append("")
    lines.append("### OPTION 1 (Swagger UI Steps):")
    for i, step in enumerate(c["swagger_steps"], 1):
        lines.append(f"{i}. {step}")
    lines.append("")
    lines.append("### OPTION 2 (Postman / Direct Request Steps):")
    lines.append(f"- **Method:** `{c['method']}`")
    lines.append(f"- **Full URL:** `https://attendance2.dev.zoolwork.com{c['route']}`")
    lines.append(f"- **Authorization:** `{c['auth']}`")
    lines.append("- **Headers:**")
    lines.append("  - `Content-Type: application/json`")
    lines.append("  - `__tenant: Attendance`")
    lines.append("- **Request Body (JSON Payload):**")
    if c["payload"] is None:
        lines.append("  `None (Query / Route Parameter only)`")
    else:
        lines.append("```json")
        lines.append(json_str(c["payload"]))
        lines.append("```")
    lines.append("")
    lines.append("### EXPECTED RESULT:")
    lines.append(f"- {c['expected']}")
    lines.append("")
    lines.append("### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):")
    lines.append(f"- **Col L (Manual Status):** `{c['excel'][0]}`")
    lines.append(f"- **Col M (Actual HTTP Code):** `{c['excel'][1]}`")
    lines.append(f"- **Col N (Actual Notes):** {c['excel'][2]}")
    lines.append("")

lines.append("---")
lines.append("")
lines.append("# END OF PLAYBOOK — ALL 53 TEST CASES WITH FULL REQUEST BODY PAYLOADS")
lines.append("")

full_text = "\\n".join(lines)
with open('CDWT_Manual_Testing_Playbook.md', 'w', encoding='utf-8') as f:
    f.write(full_text)

print(f"SUCCESS: Generated CDWT_Manual_Testing_Playbook.md ({len(full_text)} characters, {len(lines)} lines)!")
'''

# Wait! Look closely at the code above: full_text = "\\n".join(lines) in a raw python string inside a python script
# If we put `full_text = "\\n".join(lines)` in python, it writes `full_text = "\n".join(lines)` in the target file!
# Let's verify this!

