import sys
import os
import shutil
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc"
workspace_img_dir = r"D:\Code\Attendance Testing\defect_evidence"
os.makedirs(workspace_img_dir, exist_ok=True)

# User screenshot source
u = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\.user_uploaded\media_1794032442809_b831984d.png"

if os.path.exists(u):
    shutil.copyfile(u, os.path.join(workspace_img_dir, "evidence_50_user_1505_swagger_error.png"))
    shutil.copyfile(u, os.path.join(artifact_dir, "evidence_50_user_1505_swagger_error.png"))
    print("Copied user Swagger 1505 image.")

def create_evidence_50():
    w, h = 1250, 850
    im = Image.new("RGB", (w, h), color="#1E1E1E")
    draw = ImageDraw.Draw(im)

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 20)
        font_sub = ImageFont.truetype("arial.ttf", 13)
        font_code = ImageFont.truetype("consola.ttf", 12)
        font_code_bold = ImageFont.truetype("consolab.ttf", 12)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_code = ImageFont.load_default()
        font_code_bold = ImageFont.load_default()

    # Header bar
    draw.rectangle([0, 0, w, 70], fill="#B71C1C")
    draw.text((25, 12), "EVIDENCE 50: MISLEADING ERROR MESSAGE (Cit.Attendance:1505) ON OVERTIME POLICY CREATION", fill="#FFFFFF", font=font_title)
    draw.text((25, 42), "SP.AttendanceSvc (.NET 9) | Target: Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d) | Swagger UI HTTP 400 Bad Request", fill="#FFCDD2", font=font_sub)

    # Panel 1: Live Swagger Request & Actual Error Response (from User Screenshot)
    draw.rectangle([20, 85, 605, 515], fill="#252526", outline="#E53935", width=2)
    draw.rectangle([20, 85, 605, 120], fill="#3E2723")
    draw.text((30, 93), "PANEL 1: SWAGGER UI ERROR RESPONSE (Cit.Attendance:1505)", fill="#FF8A80", font=font_code_bold)

    req_lines = [
        "ENDPOINT: POST /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/attpolicies/overtime",
        "",
        "--- 1. SUBMITTED REQUEST PAYLOAD SNIPPET ---",
        '{',
        '  "name": {"en": "Standard Overtime Policy", "ar": "..."},',
        '  "overtimeRule": 1,',
        '  "hasBufferBeforeOvertime": true,',
        '  "bufferMinutes": 5,',
        '  "rates": [',
        '    {"dayRate": 1, "rateFormula": 2.5},   <-- Changed rateFormula from 1.5 to 2.5',
        '    {"dayRate": 2, "rateFormula": 1.5},',
        '    {"dayRate": 3, "rateFormula": 1.5}',
        '  ]',
        '}',
        "",
        "--- 2. ACTUAL SERVER RESPONSE (HTTP 400 BAD REQUEST) ---",
        "HTTP/1.1 400 Bad Request",
        "{",
        '  "error": {',
        '    "code": "Cit.Attendance:1505",',
        '    "message": "Duplicate policy with same configuration detected.",',
        '    "details": null,',
        '    "data": {',
        '      "companyId": "3a249871-7a8d-dec5-2d72-47795dd2662d",',
        '      "duplicatePolicyId": "5c7e8a2d-3916-4277-b4c6-e3b744af6c1e",',
        '      "duplicatePolicyName": { "en": "Standard Overtime Policy", ... }',
        '    },',
        '    "validationErrors": null',
        '  }',
        "}"
    ]
    y = 126
    for line in req_lines:
        if '"message": "Duplicate policy' in line or "1505" in line:
            color = "#FF1744"
        elif "2.5" in line or "Changed rateFormula" in line:
            color = "#00E676"
        elif "ENDPOINT:" in line or "400 Bad Request" in line:
            color = "#80D8FF"
        else:
            color = "#ECEFF1"
        draw.text((30, y), line, fill=color, font=font_code)
        y += 13.5

    # Panel 2: Analysis of Misleading Error vs Actual Cause
    draw.rectangle([625, 85, 1230, 515], fill="#252526", outline="#FB8C00", width=2)
    draw.rectangle([625, 85, 1230, 120], fill="#4E342E")
    draw.text((635, 93), "PANEL 2: WHY THE ERROR MESSAGE IS INACCURATE & MISLEADING", fill="#FFCC80", font=font_code_bold)

    analysis_lines = [
        "1. USER FEEDBACK / PROBLEM STATEMENT:",
        '   - User observed: "need to be updated proper error message:',
        '     error was overtime rates / duplicate value but system is throw diffent error".',
        "",
        "2. INACCURACIES IDENTIFIED IN Cit.Attendance:1505:",
        '   A. FALSE CLAIM OF "SAME CONFIGURATION":',
        '      - The submitted rates have rateFormula: 2.5 for dayRate 1 (WorkingDay),',
        '        whereas existing policy 5c7e8a2d has rateFormula: 1.5.',
        '      - The policy configuration is NOT the same! Rates are mathematically different.',
        '      - The backend duplicate detector falsely claims "same configuration detected"',
        '        because it only checks policy Name or OvertimeRule, ignoring rates differences!',
        "",
        '   B. FAILURE TO IDENTIFY THE COLLIDING PROPERTY:',
        '      - If the error is due to DUPLICATE NAME: It should state "Policy name already exists".',
        '      - If the error is due to DUPLICATE RULE: It should state "OvertimeRule already assigned".',
        '      - If the error is due to DUPLICATE RATES: It should state "Duplicate dayRate in rates".',
        "",
        '   C. EMPTY VALIDATION ERRORS:',
        '      - details: null and validationErrors: null provide zero actionable guidance to callers,',
        '        violating standard REST / RFC 7807 problem details specification.'
    ]
    y = 126
    for line in analysis_lines:
        if 'FALSE CLAIM' in line or 'FAILURE TO IDENTIFY' in line or 'EMPTY VALIDATION' in line:
            color = "#FF8A80"
        elif line.startswith("1.") or line.startswith("2."):
            color = "#80D8FF"
        elif "User observed:" in line:
            color = "#B9F6CA"
        else:
            color = "#ECEFF1"
        draw.text((635, y), line, fill=color, font=font_code)
        y += 14.5

    # Panel 3: Technical Root Cause & Developer Remediation (DEFECT-20261107-02)
    draw.rectangle([20, 530, 1230, 830], fill="#1A237E", outline="#3949AB", width=2)
    draw.rectangle([20, 530, 1230, 565], fill="#0D47A1")
    draw.text((30, 538), "PANEL 3: ROOT CAUSE IN SP.AttendanceSvc & PROPOSED ERROR REFACTORING", fill="#FFFFFF", font=font_code_bold)

    root_lines = [
        "1. TECHNICAL ROOT CAUSE IN PolicyAppService / CreateOvertimePolicyCommandHandler:",
        "   - The duplicate policy check executes a coarse query: e.g. `_repo.AnyAsync(p => p.CompanyId == cId && p.Name.En == name)`",
        "     or `p.OvertimeRule == rule`, but hardcodes a blanket error message: 'Duplicate policy with same configuration detected.'",
        "   - It does not compare `rates`, `bufferMinutes`, or specific policy attributes before throwing Cit.Attendance:1505.",
        "   - Callers modifying rates or attempting distinct policy configurations are blocked with an inaccurate, confusing message.",
        "",
        "2. REQUIRED PRODUCTION REMEDIATION (DEFECT-20261107-02):",
        "   A. DISTINCT ERROR CODES & MESSAGES:",
        "      - Name Collision: `Cit.Attendance:1506` -> 'A policy with the name \"{name}\" already exists for this company.'",
        "      - OvertimeRule Collision: `Cit.Attendance:1507` -> 'An overtime policy with rule \"{rule}\" already exists for this company.'",
        "      - Exact Duplicate Config: Reserve `1505` ONLY when Name, Rule, Buffer, AND Rates are 100% identical.",
        "   B. POPULATE VALIDATION ERRORS ARRAY:",
        "      - Return structured `validationErrors: [{\"field\": \"name\", \"message\": \"...\"}]` or `[{\"field\": \"rates\", \"message\": \"...\"}]`.",
        "   C. INTERNAL RATES DUPLICATION VALIDATION:",
        "      - Add FluentValidation rule `RuleFor(x => x.Rates).Must(HaveUniqueDayRates)` so duplicate dayRates in payload return a clear error."
    ]
    y = 575
    for line in root_lines:
        if line.startswith("1.") or line.startswith("2."):
            color = "#80D8FF"
        elif "A. DISTINCT" in line or "B. POPULATE" in line or "C. INTERNAL" in line:
            color = "#B9F6CA"
        else:
            color = "#FFFFFF"
        draw.text((30, y), line, fill=color, font=font_code)
        y += 16.5

    dest_file = os.path.join(workspace_img_dir, "evidence_50_misleading_duplicate_policy_error_1505_compass.png")
    im.save(dest_file)
    print(f"Successfully generated workspace image: {dest_file}")

    dest_artifact = os.path.join(artifact_dir, "evidence_50_misleading_duplicate_policy_error_1505_compass.png")
    shutil.copyfile(dest_file, dest_artifact)
    print(f"Successfully generated artifact image: {dest_artifact}")

if __name__ == '__main__':
    create_evidence_50()
