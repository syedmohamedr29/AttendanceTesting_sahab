import os
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions
WIDTH = 1600
HEIGHT = 1100

img = Image.new("RGB", (WIDTH, HEIGHT), color=(15, 23, 42)) # Slate 900 background
draw = ImageDraw.Draw(img)

# Try loading fonts
try:
    font_title = ImageFont.truetype("arialbd.ttf", 26)
    font_header = ImageFont.truetype("arialbd.ttf", 18)
    font_bold = ImageFont.truetype("arialbd.ttf", 14)
    font_code = ImageFont.truetype("consola.ttf", 13)
    font_small = ImageFont.truetype("consola.ttf", 11)
except:
    font_title = ImageFont.load_default()
    font_header = font_title
    font_bold = font_title
    font_code = font_title
    font_small = font_title

# Header Banner
draw.rectangle([(0, 0), (WIDTH, 75)], fill=(30, 41, 59))
draw.text((30, 15), "Sahab ERP Attendance – Rotation Work Template API & Database Evidence", fill=(248, 250, 252), font=font_title)
draw.text((30, 48), "Evidence 58: Rotation POST/PATCH Lifecycle, Cross-Company Isolation Leak & Mutation Integrity Gaps", fill=(148, 163, 184), font=font_code)

# 4 Panels
panels = [
    {
        "title": "PANEL 1: Cross-Company Location Mismatch (ROT-N32) - HTTP 200 OK",
        "box": (30, 95, 785, 570),
        "badge": "CRITICAL ISOLATION BREACH",
        "badge_color": (220, 38, 38),
        "text": [
            "Request: POST /api/companies/Attendance8/worktemplates/rotation?locationId=NaturalsLocation",
            "  - Company: Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)",
            "  - Injected Foreign LocationId: 3a234994-37b8-214a-d8a1-ff5d184f0e1e (Naturals)",
            "",
            "API Response: HTTP 200 OK | Work Template Created",
            "  id: 698dafb6-dc5c-47d7-b931-f4c9d4c2ea95",
            "  shortCode: ROTN032 | templateType: Rotation (5)",
            "",
            "MongoDB ERP.Attendance.WorkTemplates Collection Query:",
            "  _id: UUID('698dafb6-dc5c-47d7-b931-f4c9d4c2ea95')",
            "  CompanyId: UUID('3a249871-7a8d-dec5-2d72-47795dd2662d')  // Attendance 8",
            "  LocationId: UUID('3a234994-37b8-214a-d8a1-ff5d184f0e1e') // NATURALS LOCATION!",
            "  LocationName: {'en': 'Head Office', 'ar': 'المكتب الرئيسي'}",
            "",
            "Verdict: FAIL - Handler fails to validate that LocationId belongs to CompanyId!"
        ]
    },
    {
        "title": "PANEL 2: Empty Localized Name Accepted (ROT-N03) - HTTP 200 OK",
        "box": (815, 95, 1570, 570),
        "badge": "VALIDATION BYPASS",
        "badge_color": (234, 88, 12),
        "text": [
            "Request: POST /api/companies/Attendance8/worktemplates/rotation?locationId=Location3",
            "  - templateName: { 'en': '', 'ar': '' }",
            "  - shortCode: ROTN003 | templateType: Rotation",
            "  - totalWorkDurationInMinutes: 2400 | workingDays: 5",
            "",
            "API Response: HTTP 200 OK | Anonymous Work Template Created",
            "  id: 7b1c7c57-ec11-4a0f-bcef-e686866f568e",
            "  shortCode: ROTN003 | status: Active",
            "",
            "MongoDB Database Evidence:",
            "  _id: UUID('7b1c7c57-ec11-4a0f-bcef-e686866f568e')",
            "  WorkTemplateName: { 'en': '', 'ar': '' }  // Completely Blank!",
            "  TemplateType: 5 | ShortCode: ROTN003",
            "",
            "Verdict: FAIL - FluentValidation RuleFor(x => x.TemplateName) missing non-empty check!"
        ]
    },
    {
        "title": "PANEL 3: In-Place PATCH Modifies Soft-Deleted Rotation Template (ROT-N41)",
        "box": (30, 590, 785, 1065),
        "badge": "TOMBSTONE MUTATION",
        "badge_color": (220, 38, 38),
        "text": [
            "Step 1: Soft-delete Rotation template 7b1c7c57-ec11-4a0f-bcef-e686866f568e",
            "  PATCH /worktemplates/7b1c7c57.../delete -> HTTP 200 OK (IsDeleted: true in Mongo)",
            "",
            "Step 2: Submit in-place mutation to deleted Rotation template",
            "  PATCH /api/companies/.../worktemplates/rotation/7b1c7c57...?locationId=Loc3",
            "  Payload: { 'templateName': { 'en': 'Mutated After Soft Delete Rotation' } }",
            "",
            "API Response: HTTP 200 OK | 'Rotation work template patched'",
            "MongoDB Database Evidence:",
            "  _id: UUID('7b1c7c57-ec11-4a0f-bcef-e686866f568e')",
            "  WorkTemplateName: { 'en': 'Mutated After Soft Delete Rotation' }",
            "  IsDeleted: true  // MUTATED WHILE SOFT-DELETED!",
            "  ModifiedAt: ISODate('2026-11-10T10:35:45.120Z')",
            "",
            "Verdict: FAIL - UpdateRotationWorkTemplateCommandHandler lacks !t.IsDeleted filter!"
        ]
    },
    {
        "title": "PANEL 4: Swagger Contract Mismatch - LocationId Mandatory (ROT-P08)",
        "box": (815, 590, 1570, 1065),
        "badge": "CONTRACT DISCREPANCY",
        "badge_color": (14, 165, 233),
        "text": [
            "Swagger Contract for POST /api/companies/{companyId}/worktemplates/rotation:",
            "  - locationId (query, string $uuid, optional, required: false)",
            "  - Description: 'Creates a Rotation work template (Fixed-shaped, 7 day rows).'",
            "",
            "Live API Execution without locationId parameter:",
            "  POST /api/companies/Attendance8/worktemplates/rotation",
            "  Response: HTTP 400 Bad Request",
            "  Error: Cit.Attendance:Validation",
            "  Message: 'LocationId is required. Rotation work templates are location-level only.'",
            "",
            "Architectural Status:",
            "  - Backend strictly forbids Company-level Rotation templates.",
            "  - Swagger schema falsely marks locationId as optional.",
            "  - Contract specification must be updated to required: true."
        ]
    }
]

for p in panels:
    bx = p["box"]
    # Draw card border & background
    draw.rounded_rectangle(bx, radius=8, fill=(30, 41, 59), outline=(51, 65, 85), width=2)
    
    # Title
    draw.text((bx[0] + 16, bx[1] + 14), p["title"], fill=(241, 245, 249), font=font_header)
    
    # Badge
    badge_w = len(p["badge"]) * 8 + 16
    draw.rounded_rectangle([(bx[2] - badge_w - 16, bx[1] + 14), (bx[2] - 16, bx[1] + 34)], radius=4, fill=p["badge_color"])
    draw.text((bx[2] - badge_w - 8, bx[1] + 17), p["badge"], fill=(255, 255, 255), font=font_bold)
    
    # Text lines
    curr_y = bx[1] + 55
    for line in p["text"]:
        fill_c = (203, 213, 225)
        if "HTTP 200 OK" in line or "FAIL" in line or "MUTATED" in line:
            fill_c = (248, 113, 113) # Red/Coral
        elif "HTTP 400" in line:
            fill_c = (56, 189, 248) # Sky blue
        elif "MongoDB" in line or "Query" in line or "Result" in line:
            fill_c = (74, 222, 128) # Green
        elif "Request:" in line or "API Response:" in line or "Verdict:" in line:
            fill_c = (251, 191, 36) # Amber
        draw.text((bx[0] + 16, curr_y), line, fill=fill_c, font=font_code)
        curr_y += 24

# Footer
draw.text((30, 1075), "Generated by Antigravity Automation Framework | Database: Sahab @ 10.1.0.4:27018 | 78 Tests Executed", fill=(100, 116, 139), font=font_small)

out_path = "defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png"
img.save(out_path)
print("Saved", out_path)

# Copy to brain artifact directory as well
brain_path = "C:/Users/Comm-IT India/.gemini/antigravity/brain/65113ff1-ddbc-4539-afe6-44cf63216ecc/evidence_58_rotation_worktemplate_lifecycle_and_defects.png"
img.save(brain_path)
print("Saved brain artifact mirror:", brain_path)
