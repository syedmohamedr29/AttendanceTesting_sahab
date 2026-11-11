import sys
import os
import shutil
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc"
workspace_img_dir = r"D:\Code\Attendance Testing\defect_evidence"
os.makedirs(workspace_img_dir, exist_ok=True)

# Copy user-uploaded images to defect_evidence
u1 = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\.user_uploaded\media_1794031792738_7e97faf7.png"
u2 = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\.user_uploaded\media_1794031837888_e1bbe16d.jpg"

if os.path.exists(u1):
    shutil.copyfile(u1, os.path.join(workspace_img_dir, "evidence_48_user_json_editor_crop.png"))
    print("Copied user crop image.")
if os.path.exists(u2):
    shutil.copyfile(u2, os.path.join(workspace_img_dir, "evidence_48_user_json_editor_full.jpg"))
    print("Copied user full image.")

def create_evidence_48():
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
    draw.text((25, 12), "EVIDENCE 48: OMITTED TENANTNAME IN PAYLOAD PERSISTS AS EMPTY OBJECT {} IN MONGODB", fill="#FFFFFF", font=font_title)
    draw.text((25, 42), "SP.AttendanceSvc (.NET 9) | Target: Attendance 7 (3a249870-c8ae-b3dc-1b8d-c44efad14f89) | MongoDB DEV: 10.1.0.4:27018", fill="#FFCDD2", font=font_sub)

    # Panel 1: Live POST Request & API Response with tenantName: {}
    draw.rectangle([20, 85, 605, 515], fill="#252526", outline="#E53935", width=2)
    draw.rectangle([20, 85, 605, 120], fill="#3E2723")
    draw.text((30, 93), "PANEL 1: LIVE API POST (tenantName OMITTED BY CLIENT) -> HTTP 200 OK", fill="#FF8A80", font=font_code_bold)

    req_lines = [
        "ENDPOINT: POST /api/companies/3a249870-c8ae-b3dc-1b8d-c44efad14f89/attpolicies/overtime",
        "HEADERS:  Authorization: Bearer <JWT> | __tenant: Attendance",
        "",
        "--- 1. CLIENT REQUEST PAYLOAD (CLEAN REST DTO: NO id, NO tenantName) ---",
        "{",
        '  "type": "Overtime",',
        '  "name": {',
        '    "en": "Standard Overtime Policy Missing TenantName b80480",',
        '    "ar": "سياسة العمل الإضافي القياسية بدون اسم المستأجر"',
        "  },",
        '  "isActive": true,',
        '  "overtimeRule": 2,',
        '  "hasBufferBeforeOvertime": true,',
        '  "bufferMinutes": 5,',
        '  "rates": [',
        '    {"dayRate": 1, "rateFormula": 1.5},',
        '    {"dayRate": 2, "rateFormula": 1.5},',
        '    {"dayRate": 3, "rateFormula": 1.5}',
        "  ]",
        "}",
        "",
        "--- 2. ACTUAL SERVER RESPONSE (HTTP 200 OK) ---",
        "HTTP/1.1 200 OK",
        "{",
        '  "message": "Overtime policy created",',
        '  "policy": {',
        '    "id": "7df9b2ba-3e42-4399-a456-82ae42890e93",',
        '    "tenantId": "3a24741e-2667-1223-f12e-62a69fab3838",  <-- Resolved from JWT',
        '    "tenantName": {},  <-- BUG: RETURNED AS EMPTY OBJECT {}!',
        '    "companyId": "3a249870-c8ae-b3dc-1b8d-c44efad14f89",',
        '    "companyName": {"en": "Attendance 7", "ar": "الحضور 7"}',
        "  }",
        "}"
    ]
    y = 126
    for line in req_lines:
        if 'tenantName": {}' in line or "BUG:" in line:
            color = "#FF1744"
        elif "200 OK" in line or "CLEAN REST DTO" in line:
            color = "#00E676"
        elif "ENDPOINT:" in line or "HEADERS:" in line:
            color = "#80D8FF"
        else:
            color = "#ECEFF1"
        draw.text((30, y), line, fill=color, font=font_code)
        y += 13.5

    # Panel 2: Live MongoDB Compass Persistence Proof (DEFECT-20261105-04)
    draw.rectangle([625, 85, 1230, 515], fill="#252526", outline="#FB8C00", width=2)
    draw.rectangle([625, 85, 1230, 120], fill="#4E342E")
    draw.text((635, 93), "PANEL 2: MONGODB COMPASS PERSISTENCE PROOF (Sahab.ERP.Attendance.Policies)", fill="#FFCC80", font=font_code_bold)

    mongo_lines = [
        "DATABASE: Sahab | COLLECTION: ERP.Attendance.Policies",
        'DOCUMENT ID: UUID("7df9b2ba-3e42-4399-a456-82ae42890e93")',
        'QUERY: {"_id": UUID("7df9b2ba-3e42-4399-a456-82ae42890e93")}',
        "",
        "--- DIRECT MONGODB PERSISTED DOCUMENT ---",
        "{",
        '  "_id": UUID("7df9b2ba-3e42-4399-a456-82ae42890e93"),',
        '  "_t": ["PolicyBase", "OvertimePolicy"],',
        '  "TenantId": UUID("3a24741e-2667-1223-f12e-62a69fab3838"),',
        '  "TenantName": {},  <-- CRITICAL DEFECT: PERSISTED AS EMPTY OBJECT {}!',
        '  "CompanyId": UUID("3a249870-c8ae-b3dc-1b8d-c44efad14f89"),',
        '  "CompanyName": {',
        '    "en": "Attendance 7",',
        '    "ar": "الحضور 7"',
        "  },",
        '  "Name": {',
        '    "en": "Standard Overtime Policy Missing TenantName b80480",',
        '    "ar": "سياسة العمل الإضافي القياسية بدون اسم المستأجر"',
        "  },",
        '  "IsActive": true,',
        '  "Type": 2,',
        '  "OvertimeRule": 2,',
        '  "HasBufferBeforeOvertime": true,',
        '  "BufferMinutes": 5,',
        '  "Rates": [',
        '    {"DayRate": 1, "RateFormula": 1.5},',
        '    {"DayRate": 2, "RateFormula": 1.5},',
        '    {"DayRate": 3, "RateFormula": 1.5}',
        "  ]",
        "}",
        "",
        "--> CONFIRMATION: Backend fails to populate TenantName without client input!"
    ]
    y = 126
    for line in mongo_lines:
        if 'TenantName": {}' in line or "CRITICAL DEFECT" in line or "CONFIRMATION:" in line:
            color = "#FF1744"
        elif 'UUID("7df9b2ba' in line or "TenantId\":" in line or "CompanyName\":" in line:
            color = "#FFB74D"
        elif "DATABASE:" in line or "QUERY:" in line:
            color = "#80D8FF"
        else:
            color = "#ECEFF1"
        draw.text((635, y), line, fill=color, font=font_code)
        y += 13.5

    # Panel 3: Technical Root Cause & Remediation (DEFECT-20261105-04 & DEFECT-20261106-03)
    draw.rectangle([20, 530, 1230, 830], fill="#1A237E", outline="#3949AB", width=2)
    draw.rectangle([20, 530, 1230, 565], fill="#0D47A1")
    draw.text((30, 538), "PANEL 3: ROOT CAUSE ANALYSIS, USER SCREENSHOT CORRELATION & ARCHITECTURAL REMEDIATION", fill="#FFFFFF", font=font_code_bold)

    root_lines = [
        "1. CORRELATION WITH USER SCREENSHOTS (JSON Editor Online / Swagger Comparison):",
        '   - User Screenshot shows Left: Clean request omitting id & highlighting tenantName; Right: Swagger DTO exposing id: 00000000-...',
        '   - User confirmed: "id should be removed from APIs request body... and TenantName should send the structure removed that".',
        '   - USER PROVED THE FATAL FLAW: When client legitimately removes tenantName, DB TenantName is missing / empty in MongoDB!',
        "",
        "2. TECHNICAL ROOT CAUSE IN SP.AttendanceSvc (.NET 9):",
        "   - The Application Service directly binds DTO.TenantName to PolicyEntity.TenantName without fallback.",
        "   - While TenantId is automatically injected from ICurrentTenant claim (3a24741e-2667-1223-f12e-62a69fab3838),",
        "     TenantName is NOT resolved from CompanySvc or AdministrationSvc. If client omits it, it defaults to new MultilingualObject() ({}).",
        "   - This creates an illegal architectural dependency on client-provided tenant metadata, violating multi-tenant isolation.",
        "",
        "3. REQUIRED PRODUCTION REMEDIATION:",
        "   A. DTO REFACTORING (DEFECT-20261106-03): Strip `id` and `tenantName` completely from Create/Update Policy DTOs.",
        "   B. SERVICE-LAYER LOOKUP (DEFECT-20261105-04): In PolicyAppService, resolve TenantName from ICurrentTenant / CompanySvc base info",
        "      and automatically populate PolicyEntity.TenantName before persisting to Sahab.ERP.Attendance.Policies in MongoDB."
    ]
    y = 575
    for line in root_lines:
        if line.startswith("1.") or line.startswith("2.") or line.startswith("3."):
            color = "#80D8FF"
        elif "FATAL FLAW" in line or "CRITICAL" in line:
            color = "#FF8A80"
        elif "A. DTO" in line or "B. SERVICE" in line:
            color = "#B9F6CA"
        else:
            color = "#FFFFFF"
        draw.text((30, y), line, fill=color, font=font_code)
        y += 16.5

    dest_file = os.path.join(workspace_img_dir, "evidence_48_policy_omitted_tenantname_persists_as_empty_object_compass.png")
    im.save(dest_file)
    print(f"Successfully generated workspace image: {dest_file}")

    dest_artifact = os.path.join(artifact_dir, "evidence_48_policy_omitted_tenantname_persists_as_empty_object_compass.png")
    shutil.copyfile(dest_file, dest_artifact)
    print(f"Successfully generated artifact image: {dest_artifact}")

if __name__ == '__main__':
    create_evidence_48()
