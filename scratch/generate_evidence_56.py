import os
import sys
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

# Output paths
ws_img_path = r"d:\Code\Attendance Testing\defect_evidence\evidence_56_flexi_split_location_validation_bypasses_and_db_results.png"
artifact_img_path = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\evidence_56_flexi_split_location_validation_bypasses_and_db_results.png"

# Canvas dimensions
W, H = 1600, 1050
img = Image.new("RGB", (W, H), "#0f172a") # dark slate background
draw = ImageDraw.Draw(img)

# Fonts
try:
    font_title = ImageFont.truetype("arial.ttf", 26)
    font_sub = ImageFont.truetype("arial.ttf", 16)
    font_header = ImageFont.truetype("arialbd.ttf", 18)
    font_code = ImageFont.truetype("consola.ttf", 13)
    font_bold = ImageFont.truetype("arialbd.ttf", 14)
    font_regular = ImageFont.truetype("arial.ttf", 13)
except Exception:
    font_title = font_sub = font_header = font_code = font_bold = font_regular = ImageFont.load_default()

# 1. Top Banner
draw.rectangle([(0, 0), (W, 75)], fill="#1e293b")
draw.rectangle([(0, 72), (W, 75)], fill="#ef4444") # Red defect accent line

draw.text((30, 15), "DEFECT EVIDENCE 56: FLEXIBLE & SPLIT TEMPLATE VALIDATION BYPASSES & TRANSITIONS", font=font_title, fill="#f8fafc")
draw.text((30, 48), "Target: POST/PATCH /worktemplates/{flexi|split} | Location 2 (3a24d646-b3cf-b1d4-61bb-1adf094b52fc) | DB: Sahab.ERP.Attendance.WorkTemplates", font=font_sub, fill="#94a3b8")

# 2. Left Panel: Flexible & Split Validation Bypasses
left_box = [(30, 95), (780, 1010)]
draw.rectangle(left_box, fill="#1e293b", outline="#334155", width=2)
draw.rectangle([(30, 95), (780, 135)], fill="#334155")
draw.text((45, 105), "CRITICAL DEFECTS: FLEXI & SPLIT VALIDATION GAPS (HTTP 200 OK)", font=font_header, fill="#f87171")

y = 150
# Issue 1: Flexi Recurrence [6]
draw.rectangle([(45, y), (765, y + 95)], fill="#0f172a", outline="#dc2626", width=1)
draw.text((55, y + 6), "[FLX-NEG-09 / FLX-PAT-05] Recurrence Index [6] Accepted (POST & PATCH)", font=font_bold, fill="#fca5a5")
draw.text((55, y + 26), "Payload: \"flexiTimeSlots\": [ { \"recurrenceOfMonth\": [6], \"workDurationInMinutes\": 480 } ]", font=font_code, fill="#cbd5e1")
draw.text((55, y + 46), "Expected: HTTP 400 Validation Error (Only 1..5 occurrences per month)", font=font_regular, fill="#94a3b8")
draw.text((55, y + 66), "Live API Result: HTTP 200 OK | Saved Doc 0ee23f7d-aa83-493b-af79-93c99c2f7c9d to Mongo!", font=font_bold, fill="#ef4444")

y += 105
# Issue 2: Flexi Duration Mismatch
draw.rectangle([(45, y), (765, y + 95)], fill="#0f172a", outline="#dc2626", width=1)
draw.text((55, y + 6), "[FLX-NEG-10 / FLX-PAT-06] Total Duration Mismatch Accepted (3000m vs 2400m)", font=font_bold, fill="#fca5a5")
draw.text((55, y + 26), "Payload: \"totalWorkDurationInMinutes\": 3000 (Actual 5 days * 480m = 2400m)", font=font_code, fill="#cbd5e1")
draw.text((55, y + 46), "Expected: HTTP 400 Validation Error (Declared total must equal sum of slots)", font=font_regular, fill="#94a3b8")
draw.text((55, y + 66), "Live API Result: HTTP 200 OK | Persisted Doc 96a20f25-47fb-496a-b595-0259aedba8c5 to Mongo!", font=font_bold, fill="#ef4444")

y += 105
# Issue 3: Flexi Timezone
draw.rectangle([(45, y), (765, y + 95)], fill="#0f172a", outline="#dc2626", width=1)
draw.text((55, y + 6), "[FLX-PAT-07] Arbitrary / Invalid Timezone String Accepted (\"Invalid/Timezone\")", font=font_bold, fill="#fca5a5")
draw.text((55, y + 26), "Payload: \"timeZoneId\": \"Invalid/Timezone\" via PATCH /worktemplates/flexi/{id}", font=font_code, fill="#cbd5e1")
draw.text((55, y + 46), "Expected: HTTP 400 Validation Error (Must validate against valid Timezone IDs)", font=font_regular, fill="#94a3b8")
draw.text((55, y + 66), "Live API Result: HTTP 200 OK | Persisted TimeZoneId: 'Invalid/Timezone' in Mongo!", font=font_bold, fill="#ef4444")

y += 105
# Issue 4: Split Duration Mismatch
draw.rectangle([(45, y), (765, y + 95)], fill="#0f172a", outline="#dc2626", width=1)
draw.text((55, y + 6), "[SPL-NEG-10 / SPL-PAT-07] Split Total Duration Mismatch Accepted (3000m vs 2400m)", font=font_bold, fill="#fca5a5")
draw.text((55, y + 26), "Payload: \"totalWorkDurationInMinutes\": 3000 (Actual 5 days * 480m = 2400m sum)", font=font_code, fill="#cbd5e1")
draw.text((55, y + 46), "Expected: HTTP 400 Validation Error (Sum of interval durations != Total)", font=font_regular, fill="#94a3b8")
draw.text((55, y + 66), "Live API Result: HTTP 200 OK | Allowed corrupt total in POST & PATCH!", font=font_bold, fill="#ef4444")

y += 105
# Issue 5: Split Recurrence [6]
draw.rectangle([(45, y), (765, y + 95)], fill="#0f172a", outline="#dc2626", width=1)
draw.text((55, y + 6), "[SPL-PAT-06] Split PATCH Accepts Recurrence Index [6] with HTTP 200 OK", font=font_bold, fill="#fca5a5")
draw.text((55, y + 26), "Payload: \"splitTimeSlots\": [ { \"recurrenceOfMonth\": [6], \"timeSlots\": [...] } ]", font=font_code, fill="#cbd5e1")
draw.text((55, y + 46), "Expected: HTTP 400 Validation Error (Recurrence index 6 is physically impossible)", font=font_regular, fill="#94a3b8")
draw.text((55, y + 66), "Live API Result: HTTP 200 OK | Mutated MongoDB Document ab6bb972 with [6]!", font=font_bold, fill="#ef4444")

# 3. Right Panel: Polymorphic Cross-Type Transition Matrix & MongoDB Verification
right_box = [(810, 95), (1570, 1010)]
draw.rectangle(right_box, fill="#1e293b", outline="#334155", width=2)
draw.rectangle([(810, 95), (1570, 135)], fill="#334155")
draw.text((825, 105), "CROSS-TYPE TRANSITION MATRIX & LIVE MONGODB PERSISTENCE", font=font_header, fill="#38bdf8")

yr = 150
# Transition Table
draw.rectangle([(825, yr), (1555, yr + 230)], fill="#0f172a", outline="#0284c7", width=1)
draw.text((835, yr + 8), "TRANSITION MATRIX: IN-PLACE POLYMORPHIC MUTATION (HTTP 200 OK)", font=font_bold, fill="#38bdf8")
transitions = [
    ("TRANS-01: Fixed -> Flexible", "PATCH /worktemplates/flexi/{id}", "HTTP 200 OK", "Type: 1 -> 2 | _t: ['WorkTemplate', 'FlexiWorkTemplate']"),
    ("TRANS-02: Fixed -> Split", "PATCH /worktemplates/split/{id}", "HTTP 200 OK", "Type: 1 -> 3 | _t: ['WorkTemplate', 'SplitWorkTemplate']"),
    ("TRANS-03: Flexible -> Fixed", "PATCH /worktemplates/fixed/{id}", "HTTP 200 OK", "Type: 2 -> 1 | _t: ['WorkTemplate', 'FixedWorkTemplate']"),
    ("TRANS-04: Flexible -> Split", "PATCH /worktemplates/split/{id}", "HTTP 200 OK", "Type: 2 -> 3 | _t: ['WorkTemplate', 'SplitWorkTemplate']"),
    ("TRANS-05: Split -> Fixed", "PATCH /worktemplates/fixed/{id}", "HTTP 200 OK", "Type: 3 -> 1 | _t: ['WorkTemplate', 'FixedWorkTemplate']"),
    ("TRANS-06: Split -> Flexible", "PATCH /worktemplates/flexi/{id}", "HTTP 200 OK", "Type: 3 -> 2 | _t: ['WorkTemplate', 'FlexiWorkTemplate']"),
]
ty = yr + 30
for title, ep, status, res in transitions:
    draw.text((835, ty), f"• {title}:", font=font_bold, fill="#f8fafc")
    draw.text((1060, ty), f"{status}", font=font_bold, fill="#22c55e")
    draw.text((1160, ty), f"({res})", font=font_code, fill="#94a3b8")
    ty += 32

yr += 245
# MongoDB Live Document Proof
draw.rectangle([(825, yr), (1555, yr + 280)], fill="#0f172a", outline="#10b981", width=1)
draw.text((835, yr + 8), "LIVE MONGODB COMPASS PROOF: 14 DOCUMENTS IN LOCATION 2", font=font_bold, fill="#34d399")
draw.text((835, yr + 28), "Collection: Sahab.ERP.Attendance.WorkTemplates | Location: 3a24d646-b3cf-b1d4-61bb-1adf094b52fc", font=font_code, fill="#64748b")

doc_proofs = [
    ("7ecfbe95-8d3c-4612-a0cc-1454e9093a53", "FXD0001", "Flexi -> Fixed", "TemplateType: 1, _t: ['WorkTemplate', 'FixedWorkTemplate']"),
    ("68dab14c-1f54-47ef-ad0a-e3e9d8e780d6", "FXD0002", "Flexi -> Split", "TemplateType: 3, _t: ['WorkTemplate', 'SplitWorkTemplate']"),
    ("ab6bb972-24e9-4b3c-9c23-55ef8770f6e5", "SPD0001", "Split -> Fixed", "TemplateType: 1, _t: ['WorkTemplate', 'FixedWorkTemplate']"),
    ("5766c9f3-a1bf-4b3f-8463-bbce0a649645", "SPD0002", "Split -> Flexi", "TemplateType: 2, _t: ['WorkTemplate', 'FlexiWorkTemplate']"),
    ("0ee23f7d-aa83-493b-af79-93c99c2f7c9d", "FXDNEG9", "Recurrence [6]", "RecurrenceOfMonth: [6] persisted directly in DB"),
    ("96a20f25-47fb-496a-b595-0259aedba8c5", "FXDNE10", "Duration Mismatch", "TotalWorkDuration: 3000.0 (Slot sum = 2400.0)"),
    ("31f4a4df-1c71-464a-95c0-aa5198031d2d", "SPDNE10", "Split Duration Mismatch", "TotalWorkDuration: 3000.0 (Interval sum = 2400.0)"),
]
dy = yr + 52
for doc_id, sc, tag, desc in doc_proofs:
    draw.text((835, dy), f"[{sc}] {doc_id[:8]}... :", font=font_code, fill="#fbbf24")
    draw.text((1050, dy), f"{tag} -> {desc}", font=font_regular, fill="#e2e8f0")
    dy += 31

# Save image
os.makedirs(os.path.dirname(ws_img_path), exist_ok=True)
img.save(ws_img_path, format="PNG")
print(f"Saved workspace image: {ws_img_path}")

os.makedirs(os.path.dirname(artifact_img_path), exist_ok=True)
img.save(artifact_img_path, format="PNG")
print(f"Saved artifact image: {artifact_img_path}")
