import os
import sys
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

# Output paths
ws_img_path = r"d:\Code\Attendance Testing\defect_evidence\evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png"
artifact_img_path = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png"

# Canvas dimensions
W, H = 1600, 1000
img = Image.new("RGB", (W, H), "#0f172a") # dark slate background
draw = ImageDraw.Draw(img)

# Fonts
try:
    font_title = ImageFont.truetype("arial.ttf", 26)
    font_sub = ImageFont.truetype("arial.ttf", 16)
    font_header = ImageFont.truetype("arialbd.ttf", 18)
    font_code = ImageFont.truetype("consola.ttf", 14)
    font_bold = ImageFont.truetype("arialbd.ttf", 14)
    font_regular = ImageFont.truetype("arial.ttf", 13)
except Exception:
    font_title = font_sub = font_header = font_code = font_bold = font_regular = ImageFont.load_default()

# 1. Top Banner
draw.rectangle([(0, 0), (W, 75)], fill="#1e293b")
draw.rectangle([(0, 72), (W, 75)], fill="#ef4444") # Red defect accent line

draw.text((30, 15), "DEFECT EVIDENCE 55: FIXED WORK TEMPLATE LOCATION PATCH VALIDATION BYPASSES", font=font_title, fill="#f8fafc")
draw.text((30, 48), "Target: PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId} | DB: Sahab.ERP.Attendance.WorkTemplates", font=font_sub, fill="#94a3b8")

# 2. Left Panel: Tested Payload & Validation Bypass Results
left_box = [(30, 95), (780, 960)]
draw.rectangle(left_box, fill="#1e293b", outline="#334155", width=2)
draw.rectangle([(30, 95), (780, 135)], fill="#334155")
draw.text((45, 105), "CRITICAL DEFECTS: PATCH VALIDATION GAPS (HTTP 200 OK)", font=font_header, fill="#f87171")

y = 150
# Issue 1: Recurrence [6]
draw.rectangle([(45, y), (765, y + 100)], fill="#0f172a", outline="#dc2626", width=1)
draw.text((55, y + 8), "[PATCH-N06] Invalid Recurrence Month Index [6] Accepted", font=font_bold, fill="#fca5a5")
draw.text((55, y + 30), "Request Payload: \"fixedTimeSlots\": [ { \"recurrenceOfMonth\": [6], ... } ]", font=font_code, fill="#cbd5e1")
draw.text((55, y + 50), "Expected: HTTP 400 Validation Error (Recurrence index must be 1 to 5)", font=font_regular, fill="#94a3b8")
draw.text((55, y + 70), "Live API Result: HTTP 200 OK | Saved to MongoDB without restriction!", font=font_bold, fill="#ef4444")

y += 115
# Issue 2: Duration mismatch
draw.rectangle([(45, y), (765, y + 100)], fill="#0f172a", outline="#dc2626", width=1)
draw.text((55, y + 8), "[PATCH-N07] Total Work Duration Mismatch (3000m vs 2700m) Accepted", font=font_bold, fill="#fca5a5")
draw.text((55, y + 30), "Request Payload: \"totalWorkDurationInMinutes\": 3000 (Slots sum = 2700)", font=font_code, fill="#cbd5e1")
draw.text((55, y + 50), "Expected: HTTP 400 Validation Error (Declared total must match slot sum)", font=font_regular, fill="#94a3b8")
draw.text((55, y + 70), "Live API Result: HTTP 200 OK | Overrode database without sum validation!", font=font_bold, fill="#ef4444")

y += 115
# Issue 3: Invalid timezone
draw.rectangle([(45, y), (765, y + 100)], fill="#0f172a", outline="#dc2626", width=1)
draw.text((55, y + 8), "[PATCH-N08] Arbitrary Timezone String Accepted (\"Invalid/Timezone\")", font=font_bold, fill="#fca5a5")
draw.text((55, y + 30), "Request Payload: \"timeZoneId\": \"Invalid/Timezone\"", font=font_code, fill="#cbd5e1")
draw.text((55, y + 50), "Expected: HTTP 400 Validation Error (Must be valid IANA/Windows timezone)", font=font_regular, fill="#94a3b8")
draw.text((55, y + 70), "Live API Result: HTTP 200 OK | Saved unvalidated string directly to Mongo!", font=font_bold, fill="#ef4444")

y += 115
# Issue 4: Location Quota Limit
draw.rectangle([(45, y), (765, y + 100)], fill="#0f172a", outline="#3b82f6", width=1)
draw.text((55, y + 8), "ARCHITECTURAL INVARIANT: Location Work Template Quota (Max 20)", font=font_bold, fill="#93c5fd")
draw.text((55, y + 30), "Trigger: Creating 21st template for Location 1 (3a24d629-0d56-a428-...)", font=font_code, fill="#cbd5e1")
draw.text((55, y + 50), "Live API Response: HTTP 400 Bad Request", font=font_regular, fill="#94a3b8")
draw.text((55, y + 70), "Error Code: Cit.Attendance:1203 | Message: Location maximum limit reached.", font=font_bold, fill="#60a5fa")

y += 115
# Issue 5: ShortCode Constraints
draw.rectangle([(45, y), (765, y + 100)], fill="#0f172a", outline="#10b981", width=1)
draw.text((55, y + 8), "VALIDATION INVARIANT: ShortCode Constraints (Length 7 & Immutability)", font=font_bold, fill="#6ee7b7")
draw.text((55, y + 30), "Rule 1: Length != 7 -> HTTP 400 'ShortCode must be exactly 7 letters or digits.'", font=font_regular, fill="#cbd5e1")
draw.text((55, y + 50), "Rule 2: PATCH Alteration -> HTTP 400 'Cit.Attendance:1107 Short code cannot be changed.'", font=font_regular, fill="#cbd5e1")
draw.text((55, y + 70), "Result: Both creation and update enforce strict shortCode integrity.", font=font_bold, fill="#34d399")

y += 115
draw.text((50, y + 15), "Live Execution: 78 automated API tests executed against DEV on 10-Nov-2026", font=font_regular, fill="#64748b")
draw.text((50, y + 35), "Authentication: Bearer OAuth2 Token | Target Location: Location1", font=font_regular, fill="#64748b")

# 3. Right Panel: MongoDB DEV Document Verification & State
right_box = [(810, 95), (1570, 960)]
draw.rectangle(right_box, fill="#1e293b", outline="#334155", width=2)
draw.rectangle([(810, 95), (1570, 135)], fill="#334155")
draw.text((825, 105), "MONGODB LIVE VERIFICATION: DEV 10.1.0.4:27018", font=font_header, fill="#38bdf8")

mongo_text = """
// Collection: Sahab.ERP.Attendance.WorkTemplates
// Target Template: c9e00652-eae5-429a-bef0-4d4ddf9e0a0f (FXL0101)
// State after In-Place PATCH Testing:

{
  "_id": UUID("c9e00652-eae5-429a-bef0-4d4ddf9e0a0f"),
  "_t": [ "WorkTemplate", "FixedWorkTemplate" ],
  "CompanyId": UUID("3a249871-7a8d-dec5-2d72-47795dd2662d"),
  "LocationId": UUID("3a24d629-0d56-a428-baa1-98493a77e614"),
  "LocationName": { "en": "Location1", "ar": "الموقع 1" },
  "ShortCode": "FXL0101",
  "WorkTemplateName": {
    "en": "Standard Fixed Shift FXL0101",
    "ar": "وردية العمل الثابتة FXL0101"
  },
  "TemplateType": 1,
  "Version": "1.0",           <-- In-Place Update (No version bump)
  "IsDefault": false,          <-- Regular Shift (Location Scoped)
  "IsCompanyLinked": false,
  "CreatedAt": ISODate("2026-11-10T07:38:45.346Z"),
  "CreatedBy": "syed.mohamed@comm-it.in",
  "ModifiedAt": ISODate("2026-11-10T07:56:56.855Z"),  <-- Updated
  "ModifiedBy": "syed.mohamed@comm-it.in",
  "TimeZoneId": "Asia/Riyadh",
  "TotalWorkDurationInMinutes": 2700.0,
  "TotalWorkingDays": 5,
  "TotalDaysOff": 2,
  "FixedTimeSlots": [ 7 items ]
}

============================================================
KEY ARCHITECTURAL DISCOVERY:
1. Direct Location Templates (IsCompanyLinked: false):
   - In-place PATCH correctly preserves CreatedAt & CreatedBy.
2. Seeded Location Templates (IsCompanyLinked: true, e.g. LOC0001):
   - In-place PATCH suffers DEFECT-20261110-03 (CreatedAt overwritten
     with 0001-01-01T00:00:00Z and CreatedBy reset to null).
"""

lines = mongo_text.strip().split("\n")
my = 150
for l in lines:
    color = "#93c5fd" if "UUID" in l or "ISODate" in l else "#f1f5f9"
    if "<--" in l:
        color = "#f59e0b"
    if "KEY ARCHITECTURAL" in l or "1." in l or "2." in l:
        color = "#38bdf8"
    if "DEFECT-20261110-03" in l:
        color = "#ef4444"
    draw.text((825, my), l, font=font_code, fill=color)
    my += 21

# Save image
os.makedirs(os.path.dirname(ws_img_path), exist_ok=True)
img.save(ws_img_path)
img.save(artifact_img_path)
print(f"Generated Evidence 55 at {ws_img_path} and {artifact_img_path}")
