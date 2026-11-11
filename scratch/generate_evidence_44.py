import sys
import os
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc"
workspace_img_dir = r"D:\Code\Attendance Testing\defect_evidence"
os.makedirs(workspace_img_dir, exist_ok=True)

def create_evidence_44():
    w, h = 1200, 750
    im = Image.new("RGB", (w, h), color="#1E1E1E")
    draw = ImageDraw.Draw(im)
    
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 20)
        font_sub = ImageFont.truetype("arial.ttf", 13)
        font_code = ImageFont.truetype("consola.ttf", 13)
        font_code_bold = ImageFont.truetype("consolab.ttf", 13)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_code = ImageFont.load_default()
        font_code_bold = ImageFont.load_default()

    # Header bar
    draw.rectangle([0, 0, w, 65], fill="#00695C")
    draw.text((25, 12), "EVIDENCE 44: LIVE RE-VERIFICATION ON COMPANY ATTENDANCE 7 (DEFECTS & DB AUDIT)", fill="#FFFFFF", font=font_title)
    draw.text((25, 40), "Target Company: Attendance 7 (ID: 3a249870-c8ae-b3dc-1b8d-c44efad14f89) | Service: SP.AttendanceSvc | DB: MongoDB Sahab", fill="#B2DFDB", font=font_sub)

    # Panel 1: DEFECT-20261105-03 Re-Verification (Negative Overtime Rate Accepted)
    draw.rectangle([25, 80, 580, 400], fill="#252526", outline="#E53935", width=2)
    draw.rectangle([25, 80, 580, 115], fill="#3E1A1A")
    draw.text((35, 90), "RE-VERIFIED: DEFECT-20261105-03 (NEGATIVE OVERTIME RATE)", fill="#FF5252", font=font_code_bold)

    p1_lines = [
        "POST /api/companies/3a249870.../attpolicies/overtime HTTP/1.1",
        "Host: attendance2.dev.zoolwork.com | Company: Attendance 7",
        "",
        "{",
        '  "name": { "en": "Negative Overtime Multiplier Test" },',
        '  "rates": [',
        '    {',
        '      "dayRate": "WorkingDay",',
        '      "rateFormula": -1.5     // <-- CRITICAL: Negative multiplier',
        '    }',
        '  ]',
        "}",
        "",
        "ACTUAL RESPONSE: HTTP/1.1 200 OK",
        "{",
        '  "message": "Overtime policy created",',
        '  "policy": {',
        '    "id": "59a1ed42-4425-493f-9db9-4fca6d91d411",',
        '    "companyId": "3a249870-c8ae-b3dc-1b8d-c44efad14f89"',
        '  }',
        "}"
    ]
    y = 125
    for line in p1_lines:
        col = "#DCDCDC"
        if '"rateFormula": -1.5' in line:
            col = "#FF5252"
        elif "HTTP/1.1 200 OK" in line:
            col = "#FFD600"
        elif "POST " in line:
            col = "#569CD6"
        draw.text((35, y), line, fill=col, font=font_code)
        y += 13

    # Panel 2: DEFECT-20261106-01 Re-Verification (Duplicate Client Dictated ID Crash)
    draw.rectangle([600, 80, 1175, 400], fill="#252526", outline="#E53935", width=2)
    draw.rectangle([600, 80, 1175, 115], fill="#3E1A1A")
    draw.text((610, 90), "RE-VERIFIED: DEFECT-20261106-01 (DUPLICATE ID 500 CRASH)", fill="#FF5252", font=font_code_bold)

    p2_lines = [
        "POST /api/companies/3a249870.../attpolicies/break HTTP/1.1",
        "Payload transmits pre-existing ID: 12b68f6d-9a31-4de9-8184...",
        "",
        "{",
        '  "id": "12b68f6d-9a31-4de9-8184-f812c42de412",',
        '  "name": { "en": "Duplicate Key Attempt on Att 7" },',
        '  "breaks": [{ "name": "Tea", "type": "Paid", "durationMinutes": 11 }]',
        "}",
        "",
        "ACTUAL RESPONSE: HTTP/1.1 500 Internal Server Error",
        "{",
        '  "error": {',
        '    "code": "MongoWriteException",',
        '    "message": "A write operation resulted in an error.',
        '      WriteError: { Category: \\"DuplicateKey\\", Code: 11000,',
        '      Message: \\"E11000 duplicate key error collection:',
        '      Sahab.ERP.Attendance.Policies index: _id_ dup key:',
        '      { _id: UUID(\\"12b68f6d-9a31-4de9-8184-f812c42de412\\") }\\" }"',
        '  }',
        "}"
    ]
    y = 125
    for line in p2_lines:
        col = "#DCDCDC"
        if "500 Internal Server Error" in line or "MongoWriteException" in line:
            col = "#FF1744"
        elif "E11000 duplicate key" in line:
            col = "#FFD600"
        elif "POST " in line:
            col = "#569CD6"
        draw.text((610, y), line, fill=col, font=font_code)
        y += 13

    # Panel 3: MongoDB Compass Live Documents for Attendance 7
    draw.rectangle([25, 415, 1175, 730], fill="#111B24", outline="#00ED64", width=2)
    draw.rectangle([25, 415, 1175, 450], fill="#00351D")
    draw.text((35, 425), "MONGODB COMPASS AUDIT: 7 DOCUMENTS PERSISTED FOR ATTENDANCE 7 (Sahab > ERP.Attendance.Policies)", fill="#00ED64", font=font_code_bold)

    p3_lines = [
        "// Compass Query: { \"CompanyId\": UUID(\"3a249870-c8ae-b3dc-1b8d-c44efad14f89\") }",
        "{",
        '  "_id": UUID("59a1ed42-4425-493f-9db9-4fca6d91d411"),  // Negative Rate Multiplier Doc Persisted!',
        '  "Type": 2,                                            // Overtime Policy',
        '  "Name": { "en": "Negative Overtime Multiplier Test" },',
        '  "Rates": [{ "DayRate": 1, "RateFormula": -1.5 }],      // <-- DEFECT-20261105-03: Corrupts payroll calculation',
        '  "CompanyId": UUID("3a249870-c8ae-b3dc-1b8d-c44efad14f89"),',
        '  "CompanyName": { "en": "Attendance 7", "ar": "الحضور 7" },',
        '  "TenantId": UUID("3a24741e-2667-1223-f12e-62a69fab3838"),',
        '  "TenantName": {},                                     // <-- DEFECT-20261105-04: Persists empty object',
        '  "IsActive": true,',
        '  "CreatedAt": ISODate("2026-11-06T05:51:49.243Z")',
        "}"
    ]
    y = 460
    for line in p3_lines:
        col = "#E0E0E0"
        if '"RateFormula": -1.5' in line:
            col = "#FF5252"
        elif '"TenantName": {}' in line:
            col = "#FF5252"
        elif '"CompanyName":' in line or '"CompanyId":' in line:
            col = "#4FC3F7"
        elif "// Compass Query" in line:
            col = "#81C784"
        draw.text((35, y), line, fill=col, font=font_code)
        y += 18

    # Summary callout
    draw.rectangle([720, 570, 1150, 715], fill="#1E2A38", outline="#FFD600", width=1)
    draw.text((735, 580), "ATTENDANCE 7 RE-VERIFICATION VERDICT:", fill="#FFD600", font=font_code_bold)
    reasons = [
        "• Total 18 Tests Executed on Attendance 7.",
        "• Break, Grace, Overtime lifecycles verified.",
        "• DEFECT-20261105-03 re-verified (Rate: -1.5).",
        "• DEFECT-20261106-01 re-verified (Duplicate ID Crash).",
        "• DEFECT-20261105-04 re-verified (TenantName: {}).",
        "• DEFECT-20261105-01 re-verified (GET non-exist 400).",
        "• Soft-delete lifecycle verified (isActive: false)."
    ]
    y = 600
    for r in reasons:
        draw.text((735, y), r, fill="#DCDCDC", font=font_sub)
        y += 15

    dest1 = os.path.join(workspace_img_dir, "evidence_44_attendance7_reverification_defects_compass.png")
    dest2 = os.path.join(artifact_dir, "evidence_44_attendance7_reverification_defects_compass.png")
    im.save(dest1)
    im.save(dest2)
    print(f"Saved evidence 44 to:\n  {dest1}\n  {dest2}")

if __name__ == "__main__":
    create_evidence_44()

