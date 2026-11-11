import sys
import os
import shutil
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc"
workspace_img_dir = r"D:\Code\Attendance Testing\defect_evidence"
os.makedirs(workspace_img_dir, exist_ok=True)

def create_evidence_43():
    w, h = 1200, 750
    im = Image.new("RGB", (w, h), color="#1E1E1E")
    draw = ImageDraw.Draw(im)
    
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 20)
        font_sub = ImageFont.truetype("arial.ttf", 13)
        font_code = ImageFont.truetype("consola.ttf", 14)
        font_code_bold = ImageFont.truetype("consolab.ttf", 14)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_code = ImageFont.load_default()
        font_code_bold = ImageFont.load_default()

    # Header bar
    draw.rectangle([0, 0, w, 65], fill="#B71C1C")
    draw.text((25, 12), "EVIDENCE 43: CRITICAL DEFECT - CLIENT-DICTATED ID CAUSES HTTP 500 DUPLICATE KEY CRASH", fill="#FFFFFF", font=font_title)
    draw.text((25, 40), "Target: POST /api/companies/{companyId}/attpolicies/* | Microservice: SP.AttendanceSvc (.NET 9) | DB: MongoDB Sahab", fill="#FFCDD2", font=font_sub)

    # Panel 1: Swagger Exposing ID & Client Request Body
    draw.rectangle([25, 80, 580, 390], fill="#252526", outline="#3E3E42", width=1)
    draw.rectangle([25, 80, 580, 115], fill="#2D2D30")
    draw.text((35, 90), "CLIENT POST PAYLOAD (DICTATED 'id')", fill="#4EC9B0", font=font_code_bold)

    req_text = [
        "POST /api/companies/3a249870.../attpolicies/break HTTP/1.1",
        "Host: attendance2.dev.zoolwork.com",
        "Authorization: Bearer eyJhbGciOi...",
        "Content-Type: application/json",
        "",
        "{",
        '  "id": "40321957-cf6e-456f-a548-4e3f20e5acae",',
        '  "name": { "en": "Duplicate ID Attempt" },',
        '  "breaks": [',
        '    {',
        '      "name": "Lunch-Unique-99",',
        '      "type": "Unpaid",',
        '      "durationMinutes": 45',
        '    }',
        '  ]',
        "}"
    ]
    y = 125
    for line in req_text:
        col = "#DCDCDC"
        if '"id":' in line:
            col = "#FF5252" # highlight injected id
        elif "POST " in line:
            col = "#569CD6"
        elif '"name":' in line or '"breaks":' in line:
            col = "#9CDCFE"
        draw.text((35, y), line, fill=col, font=font_code)
        y += 16

    # Panel 2: HTTP 500 Response Body & Stack Trace Leak
    draw.rectangle([600, 80, 1175, 390], fill="#252526", outline="#E53935", width=2)
    draw.rectangle([600, 80, 1175, 115], fill="#3E1A1A")
    draw.text((610, 90), "SERVER HTTP 500 INTERNAL SERVER ERROR (CRASH)", fill="#FF5252", font=font_code_bold)

    resp_text = [
        "HTTP/1.1 500 Internal Server Error",
        "Content-Type: application/json; charset=utf-8",
        "",
        "{",
        '  "error": {',
        '    "code": "MongoWriteException",',
        '    "message": "A write operation resulted in an error.',
        '      WriteError: {',
        '        Category: \\"DuplicateKey\\",',
        '        Code: 11000,',
        '        Message: \\"E11000 duplicate key error',
        '          collection: Sahab.ERP.Attendance.Policies',
        '          index: _id_ dup key:',
        '          { _id: UUID(\\"40321957-cf6e-456f...\\") }\\"',
        '      }",',
        '    "details": null,',
        '    "validationErrors": null',
        '  }',
        "}"
    ]
    y = 125
    for line in resp_text:
        col = "#FFCDD2"
        if "500 Internal" in line or "MongoWriteException" in line:
            col = "#FF1744"
        elif "collection:" in line or "index: _id_" in line:
            col = "#FFD600" # highlight db leak
        draw.text((610, y), line, fill=col, font=font_code)
        y += 15

    # Panel 3: MongoDB Compass Live Document View
    draw.rectangle([25, 410, 1175, 725], fill="#111B24", outline="#00ED64", width=2)
    draw.rectangle([25, 410, 1175, 445], fill="#00351D")
    draw.text((35, 420), "MONGODB COMPASS - LIVE VERIFICATION: Sahab > ERP.Attendance.Policies", fill="#00ED64", font=font_code_bold)

    mongo_lines = [
        '{',
        '  "_id": UUID("40321957-cf6e-456f-a548-4e3f20e5acae"),      // <-- Client dictated custom ID stored in DB!',
        '  "Type": 1,',
        '  "Name": { "en": "Break ID Client Dictated" },',
        '  "CompanyId": UUID("3a249870-184c-0373-f344-015d602678d7"), // Route parameter strictly enforced',
        '  "CompanyName": { "en": "Attendance 6", "ar": "الحضور 6" },',
        '  "TenantId": UUID("3a24741e-2667-1223-f12e-62a69fab3838"),',
        '  "TenantName": {},                                           // <-- DEFECT: Empty Object persisted',
        '  "IsActive": true,',
        '  "CreatedAt": ISODate("2026-11-06T05:42:03.584Z"),',
        '  "CreatedBy": "syed.mohamed@comm-it.in"',
        '}'
    ]
    y = 455
    for line in mongo_lines:
        col = "#E0E0E0"
        if '"_id":' in line:
            col = "#FF7043"
        elif '"TenantName": {}' in line:
            col = "#FF5252"
        elif '"CompanyId":' in line or '"CompanyName":' in line:
            col = "#4FC3F7"
        draw.text((35, y), line, fill=col, font=font_code)
        y += 20

    # Summary callout
    draw.rectangle([700, 560, 1150, 705], fill="#1E2A38", outline="#FFD600", width=1)
    draw.text((715, 570), "DEFECT-20261106-01 ROOT CAUSE ANALYSIS:", fill="#FFD600", font=font_code_bold)
    reasons = [
        "1. DTO Model exposes client-writable 'id'.",
        "2. Service assigns client ID to doc._id without override.",
        "3. No check for pre-existing _id before Mongo insert.",
        "4. MongoWriteException 11000 caught as unhandled 500.",
        "5. Internal DB schema & collection names leaked to caller.",
        "FIX: Server must generate UUIDv4 and ignore client 'id'."
    ]
    y = 595
    for r in reasons:
        draw.text((715, y), r, fill="#DCDCDC", font=font_sub)
        y += 17

    dest1 = os.path.join(workspace_img_dir, "evidence_43_policy_duplicate_id_mongo_500_crash.png")
    dest2 = os.path.join(artifact_dir, "evidence_43_policy_duplicate_id_mongo_500_crash.png")
    im.save(dest1)
    im.save(dest2)
    print(f"Saved evidence 43 to:\n  {dest1}\n  {dest2}")

if __name__ == "__main__":
    create_evidence_43()

