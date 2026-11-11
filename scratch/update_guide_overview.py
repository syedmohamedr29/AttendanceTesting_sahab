with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'r', encoding='utf-8') as f:
    content = f.read()

target = """### Master Consolidated Workbook Overview
* **Consolidated File:** `AttendanceTestCases_Master_Consolidated.xlsx` (Created clean; existing files remain 100% untouched).
* **Total Tests:** **1,079 test cases** across **16 structured tabs**:
  - `INDEX` Dashboard with auto-counters.
  - `User Scenarios (Add Here)` dedicated custom scenarios tab.
  - 9 Active Master Setup & Scheduling tabs (Blue & Green).
  - 5 Attendance Log processing tabs (Rose, tagged with `(KT)` as deferred)."""

replacement = """### Master Consolidated Workbook Overview
* **Consolidated File:** `AttendanceTestCases_Master_Consolidated.xlsx` (Created clean; existing baseline sheets remain 100% untouched).
* **Total Tests:** **1,492 test cases** across **17 structured tabs**:
  - `INDEX` Dashboard with auto-counters across all 16 modules.
  - `User Scenarios (Add Here)` dedicated custom scenarios tab (127 TCs).
  - 10 Active Master Setup & Scheduling tabs (Blue & Green), including `Holiday Calendar - Test Cases` (286 TCs).
  - 5 Attendance Log processing tabs (Rose, tagged with `(KT)` as deferred).
  - Priority Breakdown: **P0: 640** | **P1: 642** | **P2: 197** | **P3: 13**."""

if target in content:
    content = content.replace(target, replacement)
    with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully updated Overview in guide!")
else:
    # Try normalizing newlines
    content_norm = content.replace('\r\n', '\n')
    target_norm = target.replace('\r\n', '\n')
    replacement_norm = replacement.replace('\r\n', '\n')
    if target_norm in content_norm:
        content_norm = content_norm.replace(target_norm, replacement_norm)
        with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'w', encoding='utf-8', newline='\r\n') as f:
            f.write(content_norm.replace('\n', '\r\n'))
        print("Successfully updated Overview in guide (normalized CRLF)!")
    else:
        print("Target not found!")

