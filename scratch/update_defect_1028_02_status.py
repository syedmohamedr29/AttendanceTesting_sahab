import sys

sys.stdout.reconfigure(encoding='utf-8')

# Update Master Defect Log
with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

old_row = '| [`DEFECT-20261028-02`](#defect-20261028-02) | 🟠 P1 | Work Template | FluentValidation `ValidationException` throws unhandled HTTP 500 crash across 13 user scenarios | `ASP.NET Core Middleware` | Exception Filter |'
new_row = '| [`DEFECT-20261028-02`](#defect-20261028-02) | 🟢 P1 | Work Template | **[FIXED 05-Nov]** FluentValidation `ValidationException` HTTP 500 crashes resolved; server returns HTTP 400 Bad Request across all 13 user scenarios | `ASP.NET Core Middleware` | 🟢 Verified Fixed (HTTP 400) |'

old_check = '- [ ] **P1 (`DEFECT-20261028-02`):** Register global exception filter to catch `FluentValidation.ValidationException` and return HTTP 400 ProblemDetails instead of HTTP 500 crashes.'
new_check = '- [x] **P1 (`DEFECT-20261028-02`):** Register global exception filter to catch `FluentValidation.ValidationException` and return HTTP 400 ProblemDetails instead of HTTP 500 crashes. *(Verified Fixed Live 05-Nov-2026: HTTP 500 crashes eliminated; returns HTTP 400 with Cit.Attendance:Validation across all scenarios)*'

if old_row in text:
    text = text.replace(old_row, new_row)
    print("Updated DEFECT-20261028-02 row in Master Defect Log!")
else:
    print("Warning: old_row not found in Master Defect Log")

if old_check in text:
    text = text.replace(old_check, new_check)
    print("Updated DEFECT-20261028-02 checklist item in Master Defect Log!")
else:
    print("Warning: old_check not found in Master Defect Log")

with open('Defects/Attendance2_Master_Defect_Log.md', 'w', encoding='utf-8') as f:
    f.write(text)

# Update main report table row and checklist item
with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    rep_text = f.read()

old_rep_row = '| **`DEFECT-20261028-02`**<br>(`USER-22`, `USER-37`, `USER-60`, `USER-63`, `USER-75`, `USER-85`, `USER-87`, `USER-90`, `USER-96`, `USER-98`, `USER-106`, `USER-137`, `USER-138`) | **P1 (Critical)** | `POST/PATCH /worktemplates/*`<br>`SP.AttendanceSvc` | FluentValidation `ValidationException` throws unhandled **HTTP 500 Server Crash** instead of HTTP 400 across 13 User Scenarios | Catch `ValidationException` in `GlobalExceptionHandlerMiddleware` and return RFC 9110 HTTP 400 | 🔴 **Open** |'
new_rep_row = '| **`DEFECT-20261028-02`**<br>(`USER-22`, `USER-37`, `USER-60`, `USER-63`, `USER-75`, `USER-85`, `USER-87`, `USER-90`, `USER-96`, `USER-98`, `USER-106`, `USER-137`, `USER-138`) | **P1 (Critical)** | `POST/PATCH /worktemplates/*`<br>`SP.AttendanceSvc` | FluentValidation `ValidationException` throws unhandled **HTTP 500 Server Crash** instead of HTTP 400 across 13 User Scenarios | Catch `ValidationException` in `GlobalExceptionHandlerMiddleware` and return RFC 9110 HTTP 400 | **🟢 FIXED** (HTTP 400 with Cit.Attendance:Validation) |'

old_rep_check = '- [ ] **P1 (`DEFECT-20261028-02`):** In global exception middleware (`GlobalExceptionHandlerMiddleware.cs`), catch `FluentValidation.ValidationException` and map it to `StatusCodes.Status400BadRequest` instead of returning HTTP 500.'
new_rep_check = '- [x] **P1 (`DEFECT-20261028-02`):** In global exception middleware (`GlobalExceptionHandlerMiddleware.cs`), catch `FluentValidation.ValidationException` and map it to `StatusCodes.Status400BadRequest` instead of returning HTTP 500. *(Verified Fixed Live 05-Nov-2026: HTTP 500 crashes eliminated; returns HTTP 400 with Cit.Attendance:Validation across all scenarios)*'

if old_rep_row in rep_text:
    rep_text = rep_text.replace(old_rep_row, new_rep_row)
    print("Updated DEFECT-20261028-02 row in Report Part 3 table!")
else:
    print("Warning: old_rep_row not found in Report")

if old_rep_check in rep_text:
    rep_text = rep_text.replace(old_rep_check, new_rep_check)
    print("Updated DEFECT-20261028-02 checklist in Report Part 5!")
else:
    print("Warning: old_rep_check not found in Report")

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(rep_text)

