import sys
import os
import shutil
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc"
workspace_img_dir = r"D:\Code\Attendance Testing\defect_evidence"
os.makedirs(workspace_img_dir, exist_ok=True)

user_src = os.path.join(workspace_img_dir, "evidence_53_user_flexi_sync_verification.jpg")
if not os.path.exists(user_src):
    u = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\.user_uploaded\media_1794292115344_8b7d5302.jpg"
    if os.path.exists(u):
        shutil.copyfile(u, user_src)

def create_evidence_53():
    w, h = 1300, 920
    im = Image.new("RGB", (w, h), color="#1E1E1E")
    draw = ImageDraw.Draw(im)

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 20)
        font_sub = ImageFont.truetype("arial.ttf", 13)
        font_code = ImageFont.truetype("consola.ttf", 12)
        font_code_bold = ImageFont.truetype("consolab.ttf", 12)
        font_badge = ImageFont.truetype("arialbd.ttf", 11)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_code = ImageFont.load_default()
        font_code_bold = ImageFont.load_default()
        font_badge = ImageFont.load_default()

    # Header bar
    draw.rectangle([0, 0, w, 70], fill="#0D47A1")
    draw.text((25, 12), "EVIDENCE 53: WORK TEMPLATE LOCATION SYNCHRONIZATION & API STATUS VERIFICATION", fill="#FFFFFF", font=font_title)
    draw.text((25, 42), "SP.AttendanceSvc (.NET 9) | Target: Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d) | MongoDB DEV: 10.1.0.4:27018", fill="#BBDEFB", font=font_sub)

    # Panel 1: Live MongoDB Compass Evidence (Flexible Location Template)
    draw.rectangle([20, 85, 635, 540], fill="#252526", outline="#1E88E5", width=2)
    draw.rectangle([20, 85, 635, 120], fill="#0D47A1")
    draw.text((30, 93), "PANEL 1: MONGODB COMPASS AUDIT (Flexible Location Template LOC0002)", fill="#90CAF9", font=font_code_bold)

    doc_lines = [
        "COLLECTION: Sahab.ERP.Attendance.WorkTemplates",
        'COMPANY ID: UUID("3a249871-7a8d-dec5-2d72-47795dd2662d") (Attendance 8)',
        'LOCATION ID: UUID("3a24d646-b3cf-b1d4-61bb-1adf094b52fc")',
        "",
        "--- LIVE MONGODB DOCUMENT RECORD ---",
        "{",
        '  "ShortCode": "LOC0002",',
        '  "TemplateType": 2,          <-- Polymorphic Type: Flexible (Daily Flexi)',
        '  "FlexibleType": 1,',
        '  "TotalWorkDurationInMinutes": 1800,  <-- 30 Hours (5 days x 6 hrs)',
        '  "TotalWorkingDays": 5,',
        '  "TotalDaysOff": 2,',
        '  "Status": 1,               <-- Active',
        '  "Version": "1.0",          <-- Version 1.0',
        '  "IsDefault": false,        <-- Location Template (Not CDWT)',
        '  "IsEditable": true,',
        '  "HasPendingLocSync": false, <-- USER OBSERVATION: Flag is False in DB',
        '  "IsCompanyLinked": true,   <-- CRITICAL: Marked Linked to Company Default!',
        '  "TimeZoneId": "Asia/Riyadh",',
        '  "FlexiTimeSlots": [ ... 7 items ... ],',
        '  "CreatedAt": ISODate("2026-11-10T06:20:22.176Z")',
        "}",
        "",
        "--- CRITICAL OBSERVATION ---",
        "• Newly created templates initialize HasPendingLocSync = false by default.",
        "• This does NOT prove CDWT v2.0 (2160m / 4 days) was synced down to it!",
        "• True synchronization status MUST be confirmed via the API endpoint."
    ]
    y = 126
    for line in doc_lines:
        if '"HasPendingLocSync": false' in line or "USER OBSERVATION:" in line:
            color = "#00E676"
        elif '"IsCompanyLinked": true' in line or "CRITICAL:" in line:
            color = "#FFD600"
        elif '"TemplateType": 2' in line or "1800" in line:
            color = "#80D8FF"
        elif "COLLECTION:" in line or "COMPANY ID:" in line or "LOCATION ID:" in line:
            color = "#80D8FF"
        elif "CRITICAL OBSERVATION" in line or "•" in line:
            color = "#FF8A80"
        else:
            color = "#ECEFF1"
        draw.text((30, y), line, fill=color, font=font_code)
        y += 14.5

    # Panel 2: API Verification Contract & Flow
    draw.rectangle([655, 85, 1280, 540], fill="#252526", outline="#43A047", width=2)
    draw.rectangle([655, 85, 1280, 120], fill="#1B5E20")
    draw.text((665, 93), "PANEL 2: API VERIFICATION CONTRACT & SYNC-STATUS FLOW", fill="#A5D6A7", font=font_code_bold)

    api_lines = [
        "1. STEP 1: QUERY COMPANY DEFAULT SYNC STATUS (API)",
        "   ENDPOINT: GET /api/companies/{companyId}/worktemplates/company-default/sync-status",
        "   PURPOSE:  Drives the Web UI 'Apply to Locations' banner.",
        "   CONTRACT RESPONSE:",
        "   {",
        '     "hasCompanyDefault": true,',
        '     "hasPendingLocSync": true,  <-- TRUE if CDWT v2.0 changes are pending!',
        '     "currentVersion": "2.0",',
        '     "changeLog": [ "Work template updated" ]',
        "   }",
        "   VERIFICATION RULE: If API returns hasPendingLocSync = false, all",
        "   locations are synchronized. If true, locations are behind CDWT v2.0!",
        "",
        "2. STEP 2: QUERY LOCATION WORK TEMPLATES LISTING",
        "   ENDPOINT: GET /api/companies/{companyId}/worktemplates?locationId={locId}",
        "   CHECKS:   - isCompanyLinked: true (renders 'Company WT' badge in UI)",
        "             - hasPendingLocSync: false (template itself has no local drift)",
        "             - version: '1.0' vs CDWT version '2.0'",
        "",
        "3. STEP 3: EXECUTE CASCADE SYNC (POST /apply-sync)",
        "   ENDPOINT: POST /api/companies/{companyId}/worktemplates/apply-sync",
        "   ACTION:   Pushes active CDWT v2.0 to all IsCompanyLinked = true templates.",
        "   RESPONSE: HTTP 200 OK -> { applied: true, templatesUpdated: 1 }"
    ]
    y = 126
    for line in api_lines:
        if "STEP 1:" in line or "STEP 2:" in line or "STEP 3:" in line:
            color = "#FFD54F"
        elif "ENDPOINT:" in line or "GET " in line or "POST " in line:
            color = "#80D8FF"
        elif '"hasPendingLocSync": true' in line or "VERIFICATION RULE:" in line:
            color = "#FF80AB"
        elif "HTTP 200 OK" in line or '"hasCompanyDefault": true' in line:
            color = "#00E676"
        else:
            color = "#ECEFF1"
        draw.text((665, y), line, fill=color, font=font_code)
        y += 14.5

    # Panel 3: Domain Architectural Invariants & Sync Analysis
    draw.rectangle([20, 555, 1280, 895], fill="#252526", outline="#AB47BC", width=2)
    draw.rectangle([20, 555, 1280, 590], fill="#4A148C")
    draw.text((30, 563), "PANEL 3: ARCHITECTURAL DOMAIN AUDIT: WHY HasPendingLocSync = false IN DB REQUIRES API CONFIRMATION", fill="#E1BEE7", font=font_code_bold)

    arch_lines = [
        "A. CREATION DEFAULT vs LIVE SYNCHRONIZATION STATE:",
        "   - In MongoDB, when any work template document is created (Fixed, Flexi, Split), HasPendingLocSync defaults to false.",
        "   - In Evidence 52, CDWT was edited to Version 2.0 (4 days / 2160 min), and its own document flagged HasPendingLocSync: true.",
        "   - Therefore, HasPendingLocSync: false on the 3 Flexible location templates does NOT mean they received Version 2.0!",
        "   - It means the location documents have not recorded an unapplied local modification, while CDWT v2.0 remains pending cascade.",
        "",
        "B. POLYMORPHIC WORK TEMPLATE OVERWRITE CONFLICT (IsCompanyLinked: true ON FLEXIBLE TEMPLATE):",
        "   - The Company Default Work Template is FIXED (TemplateType: 1) with 4 working days and 2160 minutes.",
        "   - The location template LOC0002 is FLEXIBLE (TemplateType: 2) with 5 working days and 1800 minutes (Daily Flexi).",
        "   - Yet LOC0002 has IsCompanyLinked: true! In the Attendance architecture, IsCompanyLinked = true marks templates that inherit CDWT.",
        "   - ARCHITECTURAL RISK: If POST /apply-sync is invoked, the handler pushes the Fixed CDWT schedule down to linked templates.",
        "     If applied, it will either: (1) Overwrite the Flexible template with Fixed slots (destroying flexi config), or (2) Fail due to type mismatch!",
        "",
        "C. STEP-BY-STEP VERIFICATION PROTOCOL FOR QA / USER:",
        "   1. Call GET /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/company-default/sync-status via Swagger UI.",
        "   2. Observe 'hasPendingLocSync' property: If true -> Company Default is out-of-sync with locations (UI banner visible).",
        "   3. Call GET /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc.",
        "   4. Check 'isCompanyLinked' and 'version' properties for each template to verify whether default location has synced v2.0 or retains v1.0."
    ]
    y = 598
    for line in arch_lines:
        if line.startswith("A. ") or line.startswith("B. ") or line.startswith("C. "):
            color = "#FFD54F"
        elif "ARCHITECTURAL RISK:" in line or "POLYMORPHIC WORK TEMPLATE OVERWRITE CONFLICT" in line:
            color = "#FF5252"
        elif "STEP-BY-STEP VERIFICATION PROTOCOL" in line:
            color = "#69F0AE"
        elif "GET /" in line or "POST /" in line:
            color = "#80D8FF"
        else:
            color = "#ECEFF1"
        draw.text((30, y), line, fill=color, font=font_code)
        y += 14.5

    out_ws = os.path.join(workspace_img_dir, "evidence_53_flexi_templates_location_sync_verification_compass.png")
    out_art = os.path.join(artifact_dir, "evidence_53_flexi_templates_location_sync_verification_compass.png")
    im.save(out_ws)
    im.save(out_art)
    print(f"Evidence 53 generated successfully:\n - {out_ws}\n - {out_art}")

if __name__ == "__main__":
    create_evidence_53()
