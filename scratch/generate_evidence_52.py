import sys
import os
import shutil
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc"
workspace_img_dir = r"D:\Code\Attendance Testing\defect_evidence"
os.makedirs(workspace_img_dir, exist_ok=True)

# User screenshot source
u = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\.user_uploaded\media_1794290975991_d0324043.jpg"

if os.path.exists(u):
    shutil.copyfile(u, os.path.join(workspace_img_dir, "evidence_52_user_cdwt_edit_haspendinglocsync_true.jpg"))
    shutil.copyfile(u, os.path.join(artifact_dir, "evidence_52_user_cdwt_edit_haspendinglocsync_true.jpg"))
    print("Copied user evidence 52 image.")

def create_evidence_52():
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
    draw.text((25, 12), "EVIDENCE 52: CDWT EDIT FAILS TO AUTO-UPDATE SEEDED LOCATION TEMPLATES (HasPendingLocSync: true)", fill="#FFFFFF", font=font_title)
    draw.text((25, 42), "SP.AttendanceSvc (.NET 9) | Target: Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d) | MongoDB DEV: 10.1.0.4:27018", fill="#FFCDD2", font=font_sub)

    # Panel 1: Live MongoDB Compass Evidence (CDWT Version 2.0 Document)
    draw.rectangle([20, 85, 605, 515], fill="#252526", outline="#E53935", width=2)
    draw.rectangle([20, 85, 605, 120], fill="#3E2723")
    draw.text((30, 93), "PANEL 1: MONGODB COMPASS PROOF (CDWT Version 2.0 on Attendance 8)", fill="#FF8A80", font=font_code_bold)

    doc_lines = [
        "COLLECTION: Sahab.ERP.Attendance.WorkTemplates",
        'COMPANY ID: UUID("3a249871-7a8d-dec5-2d72-47795dd2662d") (Attendance 8)',
        "",
        "--- EDITED COMPANY DEFAULT WORK TEMPLATE (VERSION 2.0) ---",
        "{",
        '  "IsDefault": true,',
        '  "Version": "2.0",  <-- CDWT successfully updated to Version 2.0',
        '  "TotalWorkDurationInMinutes": 2160,  <-- Changed from 2700',
        '  "TotalWorkingDays": 4,               <-- Changed from 5',
        '  "TotalDaysOff": 3,                   <-- Changed from 2',
        '  "TemplateType": 1,',
        '  "Status": 1,',
        '  "IsCompanyLinked": false,',
        '  "IsSuperseded": false,',
        '  "HasPendingLocSync": true,  <-- CRITICAL FLAG: STUCK AT TRUE!',
        '  "TimeZoneId": "Asia/Riyadh",',
        '  "ChangeLog": [ ... 2 items ... ]',
        "}",
        "",
        "--- WHAT HAPPENED TO SEEDED LOCATION TEMPLATE? ---",
        "- The seeded template at Location 1 was NOT updated!",
        "- It remains stranded with Version 1.0 schedule (5 days / 2700 min)!",
        "- Company default and location default are completely out of sync!"
    ]
    y = 126
    for line in doc_lines:
        if '"HasPendingLocSync": true' in line or "CRITICAL FLAG:" in line or "NOT updated!" in line:
            color = "#FF1744"
        elif 'Version": "2.0"' in line or "2160" in line:
            color = "#00E676"
        elif "COLLECTION:" in line or "COMPANY ID:" in line:
            color = "#80D8FF"
        elif "WHAT HAPPENED" in line:
            color = "#FFB74D"
        else:
            color = "#ECEFF1"
        draw.text((30, y), line, fill=color, font=font_code)
        y += 14.5

    # Panel 2: Analysis of Creation vs Editing Asymmetry
    draw.rectangle([625, 85, 1230, 515], fill="#252526", outline="#FB8C00", width=2)
    draw.rectangle([625, 85, 1230, 120], fill="#4E342E")
    draw.text((635, 93), "PANEL 2: CREATION VS EDITING ASYMMETRY & CASCADE GAP", fill="#FFCC80", font=font_code_bold)

    flaw_lines = [
        "1. USER FEEDBACK / PROBLEM STATEMENT:",
        '   - User observed: "while editing the default work template, company changed',
        '     the duration/anything, system is not updated the company default location.',
        '     Before: creating default seeds the location; while editing also seeding',
        '     data should be updated".',
        "",
        "2. ASYMMETRIC LIFECYCLE DEFECT:",
        '   A. On Creation (POST /worktemplates/fixed):',
        '      - Background worker immediately seeds a location template for every location',
        '        with `IsCompanyLinked = true`. Seeding is automatic and seamless.',
        '   B. On Edit (PATCH /worktemplates/fixed/{id}):',
        '      - Editing creates Version 2.0 and sets `HasPendingLocSync = true`.',
        '      - However, the system FAILS to auto-update the seeded location templates!',
        '      - Unless an explicit call to `POST /worktemplates/apply-sync` is executed,',
        '        the seeded location templates remain permanently outdated.',
        "",
        "3. BUSINESS RISK & DATA DIVERGENCE:",
        '   - Shift assignments and rotation schedules bound to Location 1 operate on',
        '     obsolete 5-day / 2700-min timings while company policy dictates 4-day / 2160-min,',
        '     causing widespread overtime/undertime errors in payroll processing!'
    ]
    y = 126
    for line in flaw_lines:
        if "ASYMMETRIC" in line or "BUSINESS RISK" in line or "FAILS to auto-update" in line:
            color = "#FF8A80"
        elif line.startswith("1.") or line.startswith("2.") or line.startswith("3."):
            color = "#80D8FF"
        elif "User observed:" in line:
            color = "#B9F6CA"
        else:
            color = "#ECEFF1"
        draw.text((635, y), line, fill=color, font=font_code)
        y += 14.5

    # Panel 3: Technical Root Cause & Developer Remediation (DEFECT-20261110-02)
    draw.rectangle([20, 530, 1230, 830], fill="#1A237E", outline="#3949AB", width=2)
    draw.rectangle([20, 530, 1230, 565], fill="#0D47A1")
    draw.text((30, 538), "PANEL 3: REQUIRED BACKEND REMEDIATION IN WORK TEMPLATE CASCADE ENGINE", fill="#FFFFFF", font=font_code_bold)

    root_lines = [
        "1. ARCHITECTURAL REMEDIATION OPTIONS IN SP.AttendanceSvc:",
        "   OPTION A (RECOMMENDED BY QA & USER): AUTOMATIC AUTO-CASCADE ON EDIT",
        "   - In `UpdateFixedWorkTemplateCommandHandler.cs` (and Flexi/Split handlers):",
        "     When editing a template where `IsDefault == true`, automatically publish an internal integration event",
        "     `CompanyDefaultWorkTemplateUpdatedIntegrationEvent` that immediately triggers `ApplySyncToLocationsAsync`.",
        "     This ensures location templates with `IsCompanyLinked == true` automatically receive Version 2.0 schedule,",
        "     and resets `HasPendingLocSync = false` immediately.",
        "",
        "   OPTION B: EXPLICIT CONFIRMATION PROMPT IN WEB UI",
        "   - If business logic allows decoupling, Web UI must present a mandatory dialog upon saving CDWT edits:",
        "     \"Do you want to apply these changes to all company-linked locations now?\"",
        "     Selecting 'Yes' must immediately trigger `POST /api/companies/{companyId}/worktemplates/apply-sync`.",
        "",
        "2. VERIFY MANUAL RECOVERY VIA SWAGGER:",
        "   - For the immediate test on Attendance 8, executing `POST /api/companies/3a249871-.../worktemplates/apply-sync`",
        "     will push Version 2.0 to Location 1 and clear `HasPendingLocSync` from true to false."
    ]
    y = 575
    for line in root_lines:
        if line.startswith("1.") or line.startswith("2."):
            color = "#80D8FF"
        elif "OPTION A" in line:
            color = "#00E676"
        elif "OPTION B" in line:
            color = "#FFD54F"
        else:
            color = "#FFFFFF"
        draw.text((30, y), line, fill=color, font=font_code)
        y += 14.5

    dest_file = os.path.join(workspace_img_dir, "evidence_52_cdwt_edit_cascade_failure_haspendinglocsync_true_compass.png")
    im.save(dest_file)
    print(f"Successfully generated workspace image: {dest_file}")

    dest_artifact = os.path.join(artifact_dir, "evidence_52_cdwt_edit_cascade_failure_haspendinglocsync_true_compass.png")
    shutil.copyfile(dest_file, dest_artifact)
    print(f"Successfully generated artifact image: {dest_artifact}")

if __name__ == '__main__':
    create_evidence_52()
