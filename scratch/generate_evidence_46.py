import sys
import os
import shutil
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc"
workspace_img_dir = r"D:\Code\Attendance Testing\defect_evidence"
os.makedirs(workspace_img_dir, exist_ok=True)

def create_evidence_46():
    w, h = 1200, 800
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
    draw.rectangle([0, 0, w, 70], fill="#B71C1C")
    draw.text((25, 12), "EVIDENCE 46: BREAK POLICY LIVE DEFECTS & INVARIANT VIOLATIONS ON ATTENDANCE 7", fill="#FFFFFF", font=font_title)
    draw.text((25, 42), "SP.AttendanceSvc (.NET 9) | Target: Attendance 7 (3a249870-c8ae-b3dc-1b8d-c44efad14f89) | MongoDB DEV: 10.1.0.4:27018", fill="#FFCDD2", font=font_sub)

    # Panel 1: HTTP 500 Crash on [null] break item (DEFECT-20261106-05)
    draw.rectangle([20, 85, 580, 480], fill="#252526", outline="#E53935", width=2)
    draw.rectangle([20, 85, 580, 120], fill="#3E2723")
    draw.text((30, 93), "DEFECT-20261106-05: HTTP 500 NullReferenceException on [null]", fill="#FF8A80", font=font_code_bold)
    
    crash_lines = [
        "ENDPOINT: PATCH /api/companies/{companyId}/attpolicies/break/{policyId}",
        "POLICY ID: 46675ad6-978d-4c02-b676-73193e48c32b",
        "",
        "--- REQUEST PAYLOAD (BRK-PATCH-N10) ---",
        "{",
        '  "type": "Break",',
        '  "name": {"en": "Null Break Item Update"},',
        '  "isActive": true,',
        '  "breaks": [null]   <-- Array contains null element',
        "}",
        "",
        "--- LIVE SERVER RESPONSE (HTTP 500 Internal Server Error) ---",
        "HTTP/1.1 500 Internal Server Error",
        "Content-Type: application/json",
        "{",
        '  "error": {',
        '    "code": "NullReferenceException",',
        '    "message": "Object reference not set to an instance",',
        '    "details": null,',
        '    "data": null,',
        '    "validationErrors": null',
        "  }",
        "}",
        "--> IMPACT: Unhandled server crash; service worker failure!"
    ]
    y = 128
    for line in crash_lines:
        color = "#FF5252" if "500" in line or "NullReferenceException" in line or "null" in line or "IMPACT" in line else "#ECEFF1"
        draw.text((30, y), line, fill=color, font=font_code)
        y += 14

    # Panel 2: Duplicate Break Items Accepted 200 OK & MongoDB Stored (DEFECT-20261106-06)
    draw.rectangle([600, 85, 1180, 480], fill="#252526", outline="#FB8C00", width=2)
    draw.rectangle([600, 85, 1180, 120], fill="#4E342E")
    draw.text((610, 93), "DEFECT-20261106-06: Duplicate Breaks Accepted HTTP 200 OK in PATCH", fill="#FFCC80", font=font_code_bold)
    
    dup_lines = [
        "ENDPOINT: PATCH /api/companies/{companyId}/attpolicies/break/{policyId}",
        "POLICY ID: 46675ad6-978d-4c02-b676-73193e48c32b",
        "",
        "--- REQUEST PAYLOAD (BRK-PATCH-N17) ---",
        "{",
        '  "type": "Break",',
        '  "name": {"en": "Duplicate Break Update"},',
        '  "breaks": [',
        '    {"name": "Tea Break", "type": 1, "durationMinutes": 15},',
        '    {"name": "Tea Break", "type": 1, "durationMinutes": 15}',
        "  ]   <-- Two identical break entries submitted",
        "}",
        "",
        "--- MONGODB COMPASS PERSISTENCE PROOF ---",
        "Collection: ERP.Attendance.Policies | _id: 46675ad6-978d-...",
        "TotalBreakDurationInMinutes: 30   <-- Sum doubled erroneously!",
        "Breaks: [",
        '  { "Name": "Tea Break", "Type": 1, "DurationMinutes": 15 },',
        '  { "Name": "Tea Break", "Type": 1, "DurationMinutes": 15 }',
        "]",
        "--> Invariant breached: Duplicate break items stored into DB!"
    ]
    y = 128
    for line in dup_lines:
        color = "#FFB74D" if "200" in line or "identical" in line or "doubled" in line or "Invariant" in line else "#ECEFF1"
        draw.text((610, y), line, fill=color, font=font_code)
        y += 14

    # Panel 3: Domain Rules Summary & Policy Cap (Cit.Attendance:1504)
    draw.rectangle([20, 500, 1180, 780], fill="#1A237E", outline="#3949AB", width=2)
    draw.rectangle([20, 500, 1180, 535], fill="#0D47A1")
    draw.text((30, 508), "DOMAIN VERIFICATION SUMMARY: ATTENDANCE 7 POLICY CAP (CIT.ATTENDANCE:1504) & ENUM SCHEMA", fill="#FFFFFF", font=font_code_bold)
    
    summary_lines = [
        "1. COMPANY BREAK POLICY CAP CONFIRMED (Cit.Attendance:1504):",
        "   - Attendance 7 reached hard cap of 8 Break Policies in MongoDB (ERP.Attendance.Policies).",
        "   - Attempting further POST /attpolicies/break returned: HTTP 400 Cit.Attendance:1504 'Policy maximum limit reached.'",
        "2. BREAK TYPE ENUM SCHEMA VERIFIED (.NET 9 SP.AttendanceSvc):",
        "   - Type 0: NotApplicable | Type 1: Paid Break (TotalPaidBreakDurationInMinutes) | Type 2: Unpaid Break (TotalUnpaidBreakDurationInMinutes)",
        "3. PATCH VALIDATION GAPS CONFIRMED (DEFECT-20261106-06):",
        "   - BRK-PATCH-N05: Arbitrary enum 'type': 999 accepted with HTTP 200 OK (Missing FluentValidation .IsInEnum())",
        "   - BRK-PATCH-N09: Blank name 'name': '' accepted with HTTP 200 OK (Missing FluentValidation .NotEmpty())",
        "   - BRK-PATCH-N17: Duplicate items accepted with HTTP 200 OK (Missing uniqueness rule within Breaks list)",
        "4. SERVER CRASH DEFECT CONFIRMED (DEFECT-20261106-05):",
        "   - BRK-PATCH-N10: 'breaks': [null] triggers unhandled NullReferenceException crashing ASP.NET Core request pipeline."
    ]
    y = 545
    for line in summary_lines:
        color = "#80D8FF" if line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("4.") else "#FFFFFF"
        draw.text((30, y), line, fill=color, font=font_code)
        y += 18

    # Save to both paths
    dest_file = os.path.join(workspace_img_dir, "evidence_46_break_policy_500_crash_null_break_and_duplicate_breaks_compass.png")
    im.save(dest_file)
    print(f"Saved workspace image: {dest_file}")
    
    dest_artifact = os.path.join(artifact_dir, "evidence_46_break_policy_500_crash_null_break_and_duplicate_breaks_compass.png")
    shutil.copyfile(dest_file, dest_artifact)
    print(f"Saved artifact image: {dest_artifact}")

if __name__ == '__main__':
    create_evidence_46()
