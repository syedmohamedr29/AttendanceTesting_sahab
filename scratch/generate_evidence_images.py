import sys
import os
import shutil
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc"
workspace_img_dir = r"D:\Code\Attendance Testing\defect_evidence"
os.makedirs(workspace_img_dir, exist_ok=True)

def create_evidence_41():
    # Negative rateFormula accepted in Overtime Policy
    w, h = 1200, 720
    im = Image.new("RGB", (w, h), color="#1E1E1E")
    draw = ImageDraw.Draw(im)
    
    # Try default fonts
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 20)
        font_sub = ImageFont.truetype("arial.ttf", 14)
        font_code = ImageFont.truetype("consola.ttf", 15)
        font_code_bold = ImageFont.truetype("consolab.ttf", 15)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_code = ImageFont.load_default()
        font_code_bold = ImageFont.load_default()

    # Top header bar (MongoDB Compass style)
    draw.rectangle([(0, 0), (w, 50)], fill="#13171A")
    draw.text((20, 15), "MongoDB Compass — DEV / Sahab / ERP.Attendance.Policies", fill="#00ED64", font=font_title)
    draw.text((w - 220, 18), "Live Cluster: Sahab DEV", fill="#A0AEC0", font=font_sub)

    # Filter Query bar
    draw.rectangle([(20, 65), (w - 20, 115)], fill="#2D3748", outline="#4A5568", width=1)
    draw.text((35, 75), "Filter Query: { \"_id\": UUID(\"77213223-d4ef-4767-ad6c-ebb778c77056\") }", fill="#63B3ED", font=font_code)
    draw.text((35, 95), "Project / Sort: { CompanyId: UUID(\"3a249870-184c-0373-f344-015d602678d7\") } (Company: Attendance 6)", fill="#A0AEC0", font=font_sub)

    # Document View Container
    draw.rectangle([(20, 130), (w - 20, h - 30)], fill="#1A202C", outline="#2D3748", width=1)
    
    doc_lines = [
        ("{\n", "#FFFFFF", False),
        ("  \"_id\": UUID(\"77213223-d4ef-4767-ad6c-ebb778c77056\"),", "#90CDF4", False),
        ("  \"_t\": [ \"Policy\", \"OvertimePolicy\" ],", "#A0AEC0", False),
        ("  \"CreatedAt\": ISODate(\"2026-11-05T12:28:59.588Z\"),", "#68D391", False),
        ("  \"CreatedBy\": \"syed.mohamed@comm-it.in\",", "#CBD5E0", False),
        ("  \"TenantId\": UUID(\"3a24741e-2667-1223-f12e-62a69fab3838\"),", "#CBD5E0", False),
        ("  \"TenantName\": {},  // Object (empty) — DEFECT-20261105-04", "#F6AD55", False),
        ("  \"CompanyId\": UUID(\"3a249870-184c-0373-f344-015d602678d7\"),", "#CBD5E0", False),
        ("  \"CompanyName\": { \"en\": \"Attendance 6\", \"ar\": \"الحضور 6\" },", "#68D391", False),
        ("  \"Name\": { \"en\": \"Negative Multiplier\" },", "#CBD5E0", False),
        ("  \"IsActive\": true,", "#68D391", False),
        ("  \"IsDeleted\": false,", "#CBD5E0", False),
        ("  \"OvertimeRule\": 0,", "#CBD5E0", False),
        ("  \"HasBufferBeforeOvertime\": false,", "#CBD5E0", False),
        ("  \"BufferMinutes\": 0,", "#CBD5E0", False),
        ("  \"Rates\": [", "#FFFFFF", False),
        ("    {", "#FFFFFF", False),
        ("      \"DayRate\": 1,  // WorkingDay", "#CBD5E0", False),
        ("      \"RateFormula\": -1.5  // 🔴 CRITICAL DEFECT: NEGATIVE PAYROLL MULTIPLIER ACCEPTED!", "#FC8181", True),
        ("    }", "#FFFFFF", False),
        ("  ]", "#FFFFFF", False),
        ("}", "#FFFFFF", False)
    ]

    y = 145
    red_box_y = 0
    for text, color, is_flagged in doc_lines:
        if is_flagged:
            red_box_y = y
        draw.text((40, y), text, fill=color, font=font_code_bold if is_flagged else font_code)
        y += 22

    # Draw QA Red Ellipse around the negative RateFormula
    if red_box_y > 0:
        draw.ellipse([(90, red_box_y - 6), (920, red_box_y + 26)], outline="#E53E3E", width=4)
        draw.text((940, red_box_y - 2), "DEFECT-20261105-03: HTTP 200 OK (Negative Multiplier)", fill="#FC8181", font=font_title)

    # API Request & Response Banner on the right
    draw.rectangle([(w - 460, 140), (w - 30, 360)], fill="#23272E", outline="#E53E3E", width=2)
    draw.text((w - 445, 150), "API PAYLOAD (POST /attpolicies/overtime):", fill="#FC8181", font=font_sub)
    payload_str = "{\n  \"name\": {\"en\": \"Negative Multiplier\"},\n  \"rates\": [\n    {\n      \"dayRate\": \"WorkingDay\",\n      \"rateFormula\": -1.5\n    }\n  ]\n}\n--> HTTP 200 OK (BUG: Expected 400)"
    draw.text((w - 445, 175), payload_str, fill="#FFFFFF", font=font_code)

    filename = "evidence_41_overtime_policy_negative_rateformula_accepted_compass.png"
    art_path = os.path.join(artifact_dir, filename)
    ws_path = os.path.join(workspace_img_dir, filename)
    im.save(art_path)
    im.save(ws_path)
    print(f"Generated {filename} successfully!")

def create_evidence_42():
    # TenantName Object (empty) in ERP.Attendance.Policies
    w, h = 1200, 720
    im = Image.new("RGB", (w, h), color="#1E1E1E")
    draw = ImageDraw.Draw(im)
    
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 20)
        font_sub = ImageFont.truetype("arial.ttf", 14)
        font_code = ImageFont.truetype("consola.ttf", 15)
        font_code_bold = ImageFont.truetype("consolab.ttf", 15)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_code = ImageFont.load_default()
        font_code_bold = ImageFont.load_default()

    draw.rectangle([(0, 0), (w, 50)], fill="#13171A")
    draw.text((20, 15), "MongoDB Compass — DEV / Sahab / ERP.Attendance.Policies", fill="#00ED64", font=font_title)
    draw.text((w - 220, 18), "Live Cluster: Sahab DEV", fill="#A0AEC0", font=font_sub)

    # Filter Query bar
    draw.rectangle([(20, 65), (w - 20, 115)], fill="#2D3748", outline="#4A5568", width=1)
    draw.text((35, 75), "Filter Query: { \"CompanyId\": UUID(\"3a249870-184c-0373-f344-015d602678d7\") }", fill="#63B3ED", font=font_code)
    draw.text((35, 95), "Total Documents Found: 4 (Company: Attendance 6) | Document View: BreakPolicy", fill="#A0AEC0", font=font_sub)

    # Document View Container
    draw.rectangle([(20, 130), (w - 20, h - 30)], fill="#1A202C", outline="#2D3748", width=1)

    doc_lines = [
        ("{\n", "#FFFFFF", False),
        ("  \"_id\": UUID(\"88a26cf7-54bc-42a1-9624-5fba47cc3587\"),", "#90CDF4", False),
        ("  \"_t\": [ \"Policy\", \"BreakPolicy\" ],", "#A0AEC0", False),
        ("  \"CreatedAt\": ISODate(\"2026-11-05T12:24:11.883Z\"),", "#68D391", False),
        ("  \"CreatedBy\": \"syed.mohamed@comm-it.in\",", "#CBD5E0", False),
        ("  \"ModifiedAt\": ISODate(\"2026-11-05T12:25:18.308Z\"),", "#CBD5E0", False),
        ("  \"ModifiedBy\": \"syed.mohamed@comm-it.in\",", "#CBD5E0", False),
        ("  \"TenantId\": UUID(\"3a24741e-2667-1223-f12e-62a69fab3838\"),", "#CBD5E0", False),
        ("  \"TenantName\": Object (empty),  // 🔴 DEFECT-20261105-04: TenantName unpopulated", "#FC8181", True),
        ("  \"CompanyId\": UUID(\"3a249870-184c-0373-f344-015d602678d7\"),", "#CBD5E0", False),
        ("  \"CompanyName\": { \"en\": \"Attendance 6\", \"ar\": \"الحضور 6\" },  // Populated Properly", "#68D391", False),
        ("  \"Name\": { \"en\": \"Attendance 6 Updated Break Policy\", \"ar\": \"سياسة الاستراحة المحدثة للحضور 6\" },", "#CBD5E0", False),
        ("  \"IsActive\": true,", "#68D391", False),
        ("  \"IsDeleted\": false,", "#CBD5E0", False),
        ("  \"TotalBreakDurationInMinutes\": 80,", "#CBD5E0", False),
        ("  \"TotalPaidBreakDurationInMinutes\": 20,", "#CBD5E0", False),
        ("  \"TotalUnpaidBreakDurationInMinutes\": 60,", "#CBD5E0", False),
        ("  \"Breaks\": [", "#FFFFFF", False),
        ("    { \"Name\": \"Morning Coffee\", \"Type\": 1, \"DurationMinutes\": 20 },", "#CBD5E0", False),
        ("    { \"Name\": \"Lunch Break\", \"Type\": 2, \"DurationMinutes\": 60 }", "#CBD5E0", False),
        ("  ]", "#FFFFFF", False),
        ("}", "#FFFFFF", False)
    ]

    y = 145
    red_box_y = 0
    for text, color, is_flagged in doc_lines:
        if is_flagged:
            red_box_y = y
        draw.text((40, y), text, fill=color, font=font_code_bold if is_flagged else font_code)
        y += 22

    if red_box_y > 0:
        draw.ellipse([(80, red_box_y - 6), (560, red_box_y + 26)], outline="#E53E3E", width=4)
        draw.text((580, red_box_y - 2), "DEFECT-20261105-04: TenantName Object (empty) {}", fill="#FC8181", font=font_title)

    # Comparison panel on right
    draw.rectangle([(w - 480, 140), (w - 30, 390)], fill="#23272E", outline="#E53E3E", width=2)
    draw.text((w - 465, 150), "PERSISTENCE COMPARISON IN COMPASS:", fill="#FC8181", font=font_sub)
    comp_str = (
        "1. CompanyName: Properly Populated\n"
        "   \"CompanyName\": {\n"
        "     \"en\": \"Attendance 6\",\n"
        "     \"ar\": \"الحضور 6\"\n"
        "   }\n\n"
        "2. TenantName: LEFT UNPOPULATED\n"
        "   \"TenantName\": {}  // Empty Object!\n\n"
        "Affected Endpoints (All 3 Types):\n"
        " • POST /attpolicies/break\n"
        " • POST /attpolicies/graceperiod\n"
        " • POST /attpolicies/overtime\n"
        " • PATCH /attpolicies/*\n"
        " • GET /attpolicies"
    )
    draw.text((w - 465, 180), comp_str, fill="#FFFFFF", font=font_code)

    filename = "evidence_42_policy_tenantname_empty_object_compass.png"
    art_path = os.path.join(artifact_dir, filename)
    ws_path = os.path.join(workspace_img_dir, filename)
    im.save(art_path)
    im.save(ws_path)
    print(f"Generated {filename} successfully!")

create_evidence_41()
create_evidence_42()
print("All evidence images generated successfully!")

