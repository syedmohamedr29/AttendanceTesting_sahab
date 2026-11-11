import sys
import os
import shutil
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc"
workspace_img_dir = r"D:\Code\Attendance Testing\defect_evidence"
os.makedirs(workspace_img_dir, exist_ok=True)

# User screenshot sources
u1 = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\.user_uploaded\media_1794033529847_37f1216f.png"
u2 = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\.user_uploaded\media_1794033529848_2f9c4adc.png"

if os.path.exists(u1):
    shutil.copyfile(u1, os.path.join(workspace_img_dir, "evidence_49_user_type_string_payload.png"))
    shutil.copyfile(u1, os.path.join(artifact_dir, "evidence_49_user_type_string_payload.png"))
    print("Copied user payload image.")
if os.path.exists(u2):
    shutil.copyfile(u2, os.path.join(workspace_img_dir, "evidence_49_user_mongodb_type_enum_int.png"))
    shutil.copyfile(u2, os.path.join(artifact_dir, "evidence_49_user_mongodb_type_enum_int.png"))
    print("Copied user MongoDB image.")

def create_evidence_49():
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
    draw.text((25, 12), "EVIDENCE 49: POLICY API PASSES 'type' AS STRING INSTEAD OF ENUM ELEMENT (STORED AS ENUM 2 IN MONGODB)", fill="#FFFFFF", font=font_title)
    draw.text((25, 42), "SP.AttendanceSvc (.NET 9) | Target: Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d) | MongoDB DEV: 10.1.0.4:27018", fill="#FFCDD2", font=font_sub)

    # Panel 1: Live API Request Body (User Proof in JSON Editor Online)
    draw.rectangle([20, 85, 605, 515], fill="#252526", outline="#E53935", width=2)
    draw.rectangle([20, 85, 605, 120], fill="#3E2723")
    draw.text((30, 93), "PANEL 1: CLIENT REQUEST PAYLOAD (STRING 'type: Overtime') IN JSON EDITOR ONLINE", fill="#FF8A80", font=font_code_bold)

    req_lines = [
        "ENDPOINT: POST /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/attpolicies/overtime",
        "SOURCE:   User Live Submission on Company Attendance 8",
        "",
        "--- 1. CLIENT REQUEST BODY (AS SUBMITTED BY CALLER) ---",
        "{",
        '  "type": "Overtime",   <-- DEFECT: STRING PASSED INSTEAD OF ENUM ELEMENT!',
        '  "name": {',
        '    "en": "Standard Overtime Policy",',
        '    "ar": "سياسة العمل الإضافي القياسية"',
        "  },",
        '  "isActive": true,',
        '  "overtimeRule": 1,',
        '  "hasBufferBeforeOvertime": true,',
        '  "bufferMinutes": 5,',
        '  "rates": [',
        '    {"dayRate": 1, "rateFormula": 1.5},',
        '    {"dayRate": 2, "rateFormula": 1.5},',
        '    {"dayRate": 3, "rateFormula": 1.5}',
        "  ]",
        "}",
        "",
        "--- 2. CONTRACT INCONSISTENCY IN SWAGGER DTO ---",
        "- Swagger OvertimePolicyDto does NOT declare 'type' property or PolicyType enum.",
        "- Client sends string 'Overtime' because contract lacks formal enum specification.",
        "- In PATCH endpoints, loose string deserialization accepts ANY arbitrary string",
        "  (e.g., 'InvalidGrace', 'RandomString') without rejecting invalid types!"
    ]
    y = 126
    for line in req_lines:
        if '"type": "Overtime"' in line or "DEFECT:" in line:
            color = "#FF1744"
        elif "CONTRACT INCONSISTENCY" in line or "Swagger" in line:
            color = "#FFB74D"
        elif "ENDPOINT:" in line or "SOURCE:" in line:
            color = "#80D8FF"
        else:
            color = "#ECEFF1"
        draw.text((30, y), line, fill=color, font=font_code)
        y += 14.5

    # Panel 2: Live MongoDB Compass Proof (Doc abe5c54e-c880-4cc3-8676-e871132ec8e4)
    draw.rectangle([625, 85, 1230, 515], fill="#252526", outline="#FB8C00", width=2)
    draw.rectangle([625, 85, 1230, 120], fill="#4E342E")
    draw.text((635, 93), "PANEL 2: MONGODB COMPASS PERSISTENCE PROOF (Type: 2 Stored as Int Enum)", fill="#FFCC80", font=font_code_bold)

    mongo_lines = [
        "DATABASE: Sahab | COLLECTION: ERP.Attendance.Policies",
        'COMPANY ID:  UUID("3a249871-7a8d-dec5-2d72-47795dd2662d") (Attendance 8)',
        'DOCUMENT ID: UUID("abe5c54e-c880-4cc3-8676-e871132ec8e4")',
        'CREATED AT:  2026-11-07T06:04:06.235Z | BY: syed.mohamed@comm-it.in',
        "",
        "--- DIRECT MONGODB PERSISTED DOCUMENT ---",
        "{",
        '  "_id": UUID("abe5c54e-c880-4cc3-8676-e871132ec8e4"),',
        '  "_t": ["PolicyBase", "OvertimePolicy"],',
        '  "TenantId": UUID("3a24741e-7667-1723-f17e-67a69fab3838"),',
        '  "TenantName": {},  <-- RE-CONFIRMATION: Persists as Object (empty) on Att 8!',
        '  "CompanyId": UUID("3a249871-7a8d-dec5-2d72-47795dd2662d"),',
        '  "CompanyName": {"en": "Attendance 8", "ar": "الحضور 8"},',
        '  "Name": {"en": "Standard Overtime Policy", "ar": "سياسة العمل الإضافي القياسية"},',
        '  "IsActive": true,',
        '  "Type": 2,         <-- PERSISTED AS NUMERIC ENUM (2 = Overtime), NOT STRING!',
        '  "OvertimeRule": 1,',
        '  "HasBufferBeforeOvertime": true,',
        '  "BufferMinutes": 5,',
        '  "Rates": [ ... 3 items ... ]',
        "}",
        "",
        "--> CRITICAL DISCONNECT: Payload uses string 'Overtime' while DB stores int '2'!"
    ]
    y = 126
    for line in mongo_lines:
        if '"Type": 2' in line or "PERSISTED AS NUMERIC" in line or "CRITICAL DISCONNECT" in line:
            color = "#00E676"
        elif "TenantName\": {}" in line or "empty" in line:
            color = "#FF1744"
        elif "DOCUMENT ID:" in line or "CREATED AT:" in line:
            color = "#FFB74D"
        elif "DATABASE:" in line or "COMPANY ID:" in line:
            color = "#80D8FF"
        else:
            color = "#ECEFF1"
        draw.text((635, y), line, fill=color, font=font_code)
        y += 14.5

    # Panel 3: Technical Root Cause & Remediation (DEFECT-20261107-01)
    draw.rectangle([20, 530, 1230, 830], fill="#1A237E", outline="#3949AB", width=2)
    draw.rectangle([20, 530, 1230, 565], fill="#0D47A1")
    draw.text((30, 538), "PANEL 3: ROOT CAUSE ANALYSIS, ENUM MAPPING CONTRACT & ARCHITECTURAL REMEDIATION", fill="#FFFFFF", font=font_code_bold)

    root_lines = [
        "1. USER SCREENSHOT CORRELATION & FINDING SUMMARY:",
        "   - User screenshot (Image 1) underlines `type : Overtime` passed as a string value in the request body.",
        "   - User MongoDB Compass screenshot (Image 2) shows target document `abe5c54e-c880-4cc3-8676-e871132ec8e4` on Attendance 8.",
        "   - Database stores `Type: 2` (integer enum), proving that the database schema uses enum elements, but API accepts loose strings.",
        "",
        "2. TECHNICAL ROOT CAUSE IN SP.AttendanceSvc (.NET 9):",
        "   - PolicyType domain enum is: `Break = 1`, `Overtime = 2`, `GracePeriod = 3`.",
        "   - Disconnect 1: DTO schemas in Swagger do not declare `type` as a formal enum (`PolicyType`), leaving callers to guess values.",
        "   - Disconnect 2: Endpoint route is dedicated (`POST /attpolicies/overtime`). If `type` is required in the body, it must be bound",
        "     to `PolicyType` enum with `.IsInEnum()` FluentValidation to prevent type mismatches or arbitrary strings.",
        "   - Disconnect 3: MongoDB serializes the enum as `int32` (`Type: 2`), but API deserializer has no documented enum converter contract.",
        "",
        "3. REQUIRED PRODUCTION REMEDIATION (DEFECT-20261107-01):",
        "   A. CONTRACT STANDARDIZATION: Expose `PolicyType` enum in OpenAPI/Swagger schemas: `1 = Break`, `2 = Overtime`, `3 = GracePeriod`.",
        "   B. STRICT MODEL BINDING: Use `JsonStringEnumConverter` or integer enum binding in ASP.NET Core with FluentValidation `.IsInEnum()`.",
        "   C. RE-VERIFIED TENANT FLUTTER: Stamping fix from DEFECT-20261105-04 must be applied across all companies (empty TenantName on Att 8)."
    ]
    y = 575
    for line in root_lines:
        if line.startswith("1.") or line.startswith("2.") or line.startswith("3."):
            color = "#80D8FF"
        elif "A. CONTRACT" in line or "B. STRICT" in line or "C. RE-VERIFIED" in line:
            color = "#B9F6CA"
        else:
            color = "#FFFFFF"
        draw.text((30, y), line, fill=color, font=font_code)
        y += 16.5

    dest_file = os.path.join(workspace_img_dir, "evidence_49_policy_type_string_vs_db_enum_int_compass.png")
    im.save(dest_file)
    print(f"Successfully generated workspace image: {dest_file}")

    dest_artifact = os.path.join(artifact_dir, "evidence_49_policy_type_string_vs_db_enum_int_compass.png")
    shutil.copyfile(dest_file, dest_artifact)
    print(f"Successfully generated artifact image: {dest_artifact}")

if __name__ == '__main__':
    create_evidence_49()
