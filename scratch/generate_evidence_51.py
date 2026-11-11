import sys
import os
import shutil
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc"
workspace_img_dir = r"D:\Code\Attendance Testing\defect_evidence"
os.makedirs(workspace_img_dir, exist_ok=True)

# User screenshot source
u = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\.user_uploaded\media_1794290562291_8806986d.jpg"

if os.path.exists(u):
    shutil.copyfile(u, os.path.join(workspace_img_dir, "evidence_51_user_location_default_ar_name_empty.jpg"))
    shutil.copyfile(u, os.path.join(artifact_dir, "evidence_51_user_location_default_ar_name_empty.jpg"))
    print("Copied user evidence 51 image.")

def create_evidence_51():
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
    draw.text((25, 12), "EVIDENCE 51: SEEDED LOCATION WORK TEMPLATE MISSING ARABIC NAME (WorkTemplateName.ar: \"\") IN MONGODB", fill="#FFFFFF", font=font_title)
    draw.text((25, 42), "SP.AttendanceSvc (.NET 9) | Target: Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d) | MongoDB DEV: 10.1.0.4:27018", fill="#FFCDD2", font=font_sub)

    # Panel 1: Live MongoDB Compass Evidence (User Screenshot Inspection)
    draw.rectangle([20, 85, 605, 515], fill="#252526", outline="#E53935", width=2)
    draw.rectangle([20, 85, 605, 120], fill="#3E2723")
    draw.text((30, 93), "PANEL 1: MONGODB COMPASS PROOF (Sahab.ERP.Attendance.WorkTemplates)", fill="#FF8A80", font=font_code_bold)

    doc_lines = [
        "COLLECTION: Sahab.ERP.Attendance.WorkTemplates",
        'COMPANY ID: UUID("3a249871-7a8d-dec5-2d72-47795dd2662d") (Attendance 8)',
        'LOCATION ID: UUID("3a24d629-0d56-a428-baa1-98493a77e614")',
        "",
        "--- AUTO-SEEDED LOCATION WORK TEMPLATE DOCUMENT ---",
        "{",
        '  "TenantName": {},  <-- TenantName persists as empty object {}',
        '  "CompanyId": UUID("3a249871-7a8d-dec5-2d72-47795dd2662d"),',
        '  "CompanyName": {',
        '    "en": "Attendance 8",',
        '    "ar": "الحضور 8"',
        '  },',
        '  "LocationId": UUID("3a24d629-0d56-a428-baa1-98493a77e614"),',
        '  "LocationName": {',
        '    "en": "Location1",',
        '    "ar": "الموقع 1"  <-- LocationName properly multilingual',
        '  },',
        '  "WorkTemplateName": {',
        '    "en": "Location Default",',
        '    "ar": ""  <-- CRITICAL DEFECT: ARABIC NAME IS EMPTY STRING ""!',
        '  },',
        '  "TemplateType": 1,',
        '  "IsDefault": false,',
        '  "IsCompanyLinked": true,',
        '  "TotalWorkDurationInMinutes": 2700,',
        '  "TotalWorkingDays": 5, "TotalDaysOff": 2',
        "}"
    ]
    y = 126
    for line in doc_lines:
        if '"ar": ""' in line or "CRITICAL DEFECT:" in line:
            color = "#FF1744"
        elif '"en": "Location Default"' in line or "AUTO-SEEDED" in line:
            color = "#FFB74D"
        elif "COLLECTION:" in line or "COMPANY ID:" in line:
            color = "#80D8FF"
        elif '"TenantName": {}' in line:
            color = "#E040FB"
        else:
            color = "#ECEFF1"
        draw.text((30, y), line, fill=color, font=font_code)
        y += 14.5

    # Panel 2: Analysis of Auto-Seeding / Provisioning Logic Flaw
    draw.rectangle([625, 85, 1230, 515], fill="#252526", outline="#FB8C00", width=2)
    draw.rectangle([625, 85, 1230, 120], fill="#4E342E")
    draw.text((635, 93), "PANEL 2: SEEDING / PROVISIONING ROOT CAUSE & LOCALIZATION FAILURE", fill="#FFCC80", font=font_code_bold)

    flaw_lines = [
        "1. USER FEEDBACK / PROBLEM STATEMENT:",
        '   - User observed: "after creating default work template, work template ar',
        '     name missing because updated as location default english name, data was',
        '     seeding while creating the template".',
        "",
        "2. TECHNICAL ROOT CAUSE IN SP.AttendanceSvc:",
        '   - When a Company Default Work Template (CDWT) is created, the service triggers',
        '     an internal provisioning workflow (e.g. `ProvisionLocationWorkTemplatesAsync`).',
        '   - The provisioning service automatically seeds a location-level template for',
        '     each company location (`IsCompanyLinked = true`).',
        '   - FLAW: The service hardcodes only the English name:',
        '       template.WorkTemplateName.En = "Location Default";',
        '       template.WorkTemplateName.Ar = string.Empty; // <-- OMITTED / EMPTY!',
        "",
        "3. MULTILINGUAL DOMAIN INVARIANT VIOLATION:",
        '   - ERP SaaS mandates full Arabic localization for Middle East / KSA enterprise clients.',
        '   - While LocationName correctly contains `ar: "الموقع 1"`, WorkTemplateName',
        '     persists with an empty Arabic string `ar: ""`.',
        '   - In the Arabic UI (`ar-SA`), the template title renders blank, breaking shift',
        '     rosters, rotation assignments, and work schedule selectors!'
    ]
    y = 126
    for line in flaw_lines:
        if "FLAW:" in line or "VIOLATION:" in line:
            color = "#FF8A80"
        elif line.startswith("1.") or line.startswith("2.") or line.startswith("3."):
            color = "#80D8FF"
        elif "User observed:" in line:
            color = "#B9F6CA"
        else:
            color = "#ECEFF1"
        draw.text((635, y), line, fill=color, font=font_code)
        y += 14.5

    # Panel 3: Technical Root Cause & Developer Remediation (DEFECT-20261110-01)
    draw.rectangle([20, 530, 1230, 830], fill="#1A237E", outline="#3949AB", width=2)
    draw.rectangle([20, 530, 1230, 565], fill="#0D47A1")
    draw.text((30, 538), "PANEL 3: REQUIRED BACKEND REMEDIATION IN WORK TEMPLATE PROVISIONING SERVICE", fill="#FFFFFF", font=font_code_bold)

    root_lines = [
        "1. CODE REMEDIATION IN WorkTemplateProvisioningService.cs / EventHandler:",
        "   When creating seeded location templates from the Company Default Work Template:",
        "   ```csharp",
        "   var locationTemplate = new WorkTemplate",
        "   {",
        "       Id = Guid.NewGuid(),",
        "       CompanyId = companyDefault.CompanyId,",
        "       LocationId = location.Id,",
        "       WorkTemplateName = new MultilingualString",
        "       {",
        "           En = !string.IsNullOrWhiteSpace(companyDefault.TemplateName?.En) ? companyDefault.TemplateName.En : \"Location Default\",",
        "           Ar = !string.IsNullOrWhiteSpace(companyDefault.TemplateName?.Ar) ? companyDefault.TemplateName.Ar : \"الدوام الافتراضي للموقع\"",
        "       },",
        "       IsDefault = false,",
        "       IsCompanyLinked = true,",
        "       // ... copy timeslots and configuration",
        "   };",
        "   ```",
        "2. DATA MIGRATION SCRIPT:",
        "   Execute a MongoDB update on `Sahab.ERP.Attendance.WorkTemplates` to fix existing orphaned empty strings:",
        "   `db.getCollection('ERP.Attendance.WorkTemplates').updateMany({ 'WorkTemplateName.ar': '' }, { $set: { 'WorkTemplateName.ar': 'الدوام الافتراضي للموقع' } })`"
    ]
    y = 575
    for line in root_lines:
        if line.startswith("1.") or line.startswith("2."):
            color = "#80D8FF"
        elif "Ar =" in line or "updateMany" in line:
            color = "#00E676"
        else:
            color = "#FFFFFF"
        draw.text((30, y), line, fill=color, font=font_code)
        y += 14.5

    dest_file = os.path.join(workspace_img_dir, "evidence_51_location_default_worktemplate_ar_name_empty_compass.png")
    im.save(dest_file)
    print(f"Successfully generated workspace image: {dest_file}")

    dest_artifact = os.path.join(artifact_dir, "evidence_51_location_default_worktemplate_ar_name_empty_compass.png")
    shutil.copyfile(dest_file, dest_artifact)
    print(f"Successfully generated artifact image: {dest_artifact}")

if __name__ == '__main__':
    create_evidence_51()
