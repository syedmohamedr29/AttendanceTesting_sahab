import os, sys
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

ws_img_path = r"d:\Code\Attendance Testing\defect_evidence\evidence_57_worktemplate_delete_lifecycle_and_bypasses.png"
artifact_img_path = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\evidence_57_worktemplate_delete_lifecycle_and_bypasses.png"

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
draw.rectangle([(0, 72), (W, 75)], fill="#ef4444")

draw.text((30, 15), "DEFECT EVIDENCE 57: WORK TEMPLATE DELETE API LIFECYCLE & CRITICAL INTEGRITY GAPS", font=font_title, fill="#f8fafc")
draw.text((30, 48), "Target: PATCH /worktemplates/{id}/delete | Company: Attendance 8 | DB: Sahab.ERP.Attendance.WorkTemplates & WorkPlans", font=font_sub, fill="#94a3b8")

# 2. Left Panel: Delete Invariants & Positive Soft-Delete Verification
left_box = [(30, 95), (780, 1010)]
draw.rectangle(left_box, fill="#1e293b", outline="#334155", width=2)
draw.rectangle([(30, 95), (780, 135)], fill="#334155")
draw.text((45, 105), "SOFT-DELETE VERIFICATION & CONFIRMED GUARDRAILS", font=font_header, fill="#38bdf8")

y = 150
# Guardrail 1: CDWT Protection
draw.rectangle([(45, y), (765, y + 95)], fill="#0f172a", outline="#0284c7", width=1)
draw.text((55, y + 6), "[DEL-N03] Active Company Default Protected (Cit.Attendance:1003)", font=font_bold, fill="#38bdf8")
draw.text((55, y + 26), "Target: PATCH /worktemplates/9580fd28-7974.../delete (Version 4.0 CDWT)", font=font_code, fill="#cbd5e1")
draw.text((55, y + 46), "Result: HTTP 400 Bad Request | Code: Cit.Attendance:1003", font=font_bold, fill="#22c55e")
draw.text((55, y + 66), "Message: 'Company default cannot be deleted.' | IsDeleted remains false in DB", font=font_regular, fill="#94a3b8")

y += 105
# Guardrail 2: Location Default Protection
draw.rectangle([(45, y), (765, y + 95)], fill="#0f172a", outline="#0284c7", width=1)
draw.text((55, y + 6), "[DEL-N04] Location Default Work Template Protected (Cit.Attendance:1007)", font=font_bold, fill="#38bdf8")
draw.text((55, y + 26), "Target: PATCH /worktemplates/0ba519c8.../delete?locationId=3a24d629... (LOC0001)", font=font_code, fill="#cbd5e1")
draw.text((55, y + 46), "Result: HTTP 400 Bad Request | Code: Cit.Attendance:1007", font=font_bold, fill="#22c55e")
draw.text((55, y + 66), "Message: 'Company default in use cannot be deactivated.' | MongoDB untouched", font=font_regular, fill="#94a3b8")

y += 105
# Guardrail 3: Company Mismatch Guard
draw.rectangle([(45, y), (765, y + 95)], fill="#0f172a", outline="#0284c7", width=1)
draw.text((55, y + 6), "[DEL-N10 / B06] Company Mismatch Guardrail (Cit.Attendance:9001)", font=font_bold, fill="#38bdf8")
draw.text((55, y + 26), "Target: PATCH /companies/{otherCompanyId}/worktemplates/{targetId}/delete", font=font_code, fill="#cbd5e1")
draw.text((55, y + 46), "Result: HTTP 400 Bad Request | Code: Cit.Attendance:9001", font=font_bold, fill="#22c55e")
draw.text((55, y + 66), "Message: 'The provided company does not match the entity company.'", font=font_regular, fill="#94a3b8")

y += 105
# Positive Soft-Delete Proof
draw.rectangle([(45, y), (765, y + 175)], fill="#0f172a", outline="#10b981", width=1)
draw.text((55, y + 8), "[DEL-P01 - P06] Positive Soft Delete Proof in MongoDB Compass", font=font_bold, fill="#34d399")
draw.text((55, y + 30), "• Fixed Template DLPOS01 (cf3ef115...): HTTP 200 OK -> IsDeleted: true", font=font_regular, fill="#f8fafc")
draw.text((55, y + 52), "• Flexible Template DLFLX01 (9f356dd2...): HTTP 200 OK -> IsDeleted: true", font=font_regular, fill="#f8fafc")
draw.text((55, y + 74), "• Split Template DLSPL01 (dc63768b...): HTTP 200 OK -> IsDeleted: true", font=font_regular, fill="#f8fafc")
draw.text((55, y + 96), "• Superseded CDWT (25d0810f...): HTTP 200 OK -> IsDeleted: true", font=font_regular, fill="#f8fafc")
draw.text((55, y + 118), "Audit Proof: ModifiedAt updated to UTC now, CreatedAt & CreatedBy preserved!", font=font_code, fill="#fbbf24")
draw.text((55, y + 140), "Physical State: Documents remain intact in MongoDB; IsDeleted flag flipped to true.", font=font_regular, fill="#94a3b8")

# 3. Right Panel: 4 Critical Bugs Discovered
right_box = [(810, 95), (1570, 1010)]
draw.rectangle(right_box, fill="#1e293b", outline="#334155", width=2)
draw.rectangle([(810, 95), (1570, 135)], fill="#334155")
draw.text((825, 105), "CRITICAL DEFECTS DISCOVERED IN DELETE LIFECYCLE", font=font_header, fill="#f87171")

yr = 150
# Defect 15: In-place PATCH allows mutating soft-deleted template
draw.rectangle([(825, yr), (1555, yr + 115)], fill="#0f172a", outline="#dc2626", width=1)
draw.text((835, yr + 6), "DEFECT-20261110-15: PATCH Allows Editing Soft-Deleted Templates (HTTP 200)", font=font_bold, fill="#fca5a5")
draw.text((835, yr + 26), "Trigger: PATCH /worktemplates/fixed/cf3ef115... on template with IsDeleted=true", font=font_code, fill="#cbd5e1")
draw.text((835, yr + 46), "Live API Result: HTTP 200 OK | Message: 'Fixed work template patched'", font=font_bold, fill="#ef4444")
draw.text((835, yr + 66), "MongoDB Proof: Doc updated to 'Revived Shift' while IsDeleted: true remained!", font=font_regular, fill="#f8fafc")
draw.text((835, yr + 86), "Root Cause: In-place update query fails to verify '!template.IsDeleted'.", font=font_code, fill="#94a3b8")

yr += 125
# Defect 16: Work Plan creation allows referencing soft-deleted template
draw.rectangle([(825, yr), (1555, yr + 115)], fill="#0f172a", outline="#dc2626", width=1)
draw.text((835, yr + 6), "DEFECT-20261110-16: Work Plan Creation Embeds Soft-Deleted Templates (HTTP 200)", font=font_bold, fill="#fca5a5")
draw.text((835, yr + 26), "Trigger: POST /workplans with workTemplateId: 'cf3ef115...' (IsDeleted: true)", font=font_code, fill="#cbd5e1")
draw.text((835, yr + 46), "Live API Result: HTTP 200 OK | Created Work Plan 0dea229a-7c98-4cf2-a819...", font=font_bold, fill="#ef4444")
draw.text((835, yr + 66), "Impact: Soft-deleted/tombstoned templates get provisioned into active plans!", font=font_regular, fill="#f8fafc")
draw.text((835, yr + 86), "Root Cause: CreateWorkPlanValidator does not check 'workTemplate.IsDeleted == false'.", font=font_code, fill="#94a3b8")

yr += 125
# Defect 17: Soft-deleted Work Plan permanently locks Work Template deletion
draw.rectangle([(825, yr), (1555, yr + 115)], fill="#0f172a", outline="#dc2626", width=1)
draw.text((835, yr + 6), "DEFECT-20261110-17: Soft-Deleted Work Plans Permanently Lock Template Deletion", font=font_bold, fill="#fca5a5")
draw.text((835, yr + 26), "Trigger: Soft-delete Work Plan 0dea229a... then delete referenced template cf3ef115...", font=font_code, fill="#cbd5e1")
draw.text((835, yr + 46), "Live API Result: HTTP 400 Bad Request | Cit.Attendance:1007", font=font_bold, fill="#ef4444")
draw.text((835, yr + 66), "Message: 'Company default in use cannot be deactivated.'", font=font_regular, fill="#f8fafc")
draw.text((835, yr + 86), "Root Cause: DeleteAsync checks Work Plans without filtering '{ IsDeleted: false }'.", font=font_code, fill="#94a3b8")

yr += 125
# Defect 18: Quota count includes soft-deleted templates
draw.rectangle([(825, yr), (1555, yr + 115)], fill="#0f172a", outline="#eab308", width=1)
draw.text((835, yr + 6), "DEFECT-20261110-18: Location 20-Quota Count Includes Soft-Deleted Templates", font=font_bold, fill="#fde047")
draw.text((835, yr + 26), "Location 1 State: Total=20, Active=19, Deleted=1 in Sahab.ERP.Attendance.WorkTemplates", font=font_code, fill="#cbd5e1")
draw.text((835, yr + 46), "Result: Creating 20th active template blocked with Cit.Attendance:1203", font=font_bold, fill="#eab308")
draw.text((835, yr + 66), "Impact: Deleting templates NEVER frees up quota slots; location is permanently full!", font=font_regular, fill="#f8fafc")
draw.text((835, yr + 86), "Root Cause: Quota query executes count_documents({ LocationId: id }) without IsDeleted.", font=font_code, fill="#94a3b8")

# Save
os.makedirs(os.path.dirname(ws_img_path), exist_ok=True)
img.save(ws_img_path, format="PNG")
print(f"Saved workspace image: {ws_img_path}")

os.makedirs(os.path.dirname(artifact_img_path), exist_ok=True)
img.save(artifact_img_path, format="PNG")
print(f"Saved artifact image: {artifact_img_path}")
