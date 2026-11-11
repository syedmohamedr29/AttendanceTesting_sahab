import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import time
import uuid
import requests
import pymongo
from bson.binary import Binary

# Connect to Mongo (Read-Only)
client = pymongo.MongoClient("mongodb://10.1.0.4:27018/", serverSelectionTimeoutMS=5000)
db = client["Sahab"]
col_wt = db["ERP.Attendance.WorkTemplates"]

with open('scratch/current_token.json', 'r') as f:
    token = json.load(f)['access_token']

BASE_URL = "https://attendance2.dev.zoolwork.com/api"
COMPANY_ID = "3a249871-7a8d-dec5-2d72-47795dd2662d" # Attendance 8
OTHER_COMPANY_ID = "3a23498e-e546-b040-2dda-43eb267a42a7" # Naturals
LOC3_ID = "3a24d667-0dcc-e3d1-74a3-cbee98168772" # Location 3 (plenty quota)
LOC2_ID = "3a24d646-b3cf-b1d4-61bb-1adf094b52fc" # Location 2
OTHER_LOC_ID = "3a234994-37b8-214a-d8a1-ff5d184f0e1e" # Naturals location

headers_auth = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

headers_noauth = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def get_mongo_doc(doc_id):
    if not doc_id:
        return None
    try:
        bin_id = Binary.from_uuid(uuid.UUID(doc_id))
        doc = col_wt.find_one({"_id": bin_id})
        if doc:
            return {
                "_id": str(uuid.UUID(bytes=doc["_id"])),
                "ShortCode": doc.get("ShortCode"),
                "TemplateType": doc.get("TemplateType"),
                "IsDeleted": doc.get("IsDeleted"),
                "Status": doc.get("Status"),
                "Version": doc.get("Version"),
                "CreatedAt": str(doc.get("CreatedAt")),
                "ModifiedAt": str(doc.get("ModifiedAt"))
            }
    except Exception as e:
        print("Mongo error:", e)
    return None

results = []

def run_test(test_id, category, method, url, payload, expected_status, notes="", headers=headers_auth):
    print(f"\n--- Running [{test_id}]: {category} ---")
    print(f"{method} {url}")
    
    target_id = None
    if "/rotation/" in url and method == "PATCH":
        parts = url.split("/rotation/")[1].split("?")[0]
        try:
            uuid.UUID(parts)
            target_id = parts
        except:
            pass
    
    doc_before = get_mongo_doc(target_id) if target_id else None
    
    start_t = time.time()
    try:
        if method == "POST":
            res = requests.post(url, headers=headers, json=payload, timeout=15)
        elif method == "PATCH":
            res = requests.patch(url, headers=headers, json=payload, timeout=15)
        elif method == "GET":
            res = requests.get(url, headers=headers, timeout=15)
        elif method == "DELETE":
            res = requests.delete(url, headers=headers, timeout=15)
    except Exception as e:
        print(f"Request exception: {e}")
        results.append({
            "test_id": test_id,
            "category": category,
            "method": method,
            "url": url,
            "payload": payload,
            "expected_status": expected_status,
            "actual_status": 0,
            "passed": False,
            "error": str(e),
            "notes": notes
        })
        return None
    
    dur = round(time.time() - start_t, 3)
    status = res.status_code
    resp_text = res.text
    print(f"Status: {status} ({dur}s)")
    
    err_code = None
    err_msg = None
    created_id = None
    
    try:
        resp_json = res.json()
        if isinstance(resp_json, dict):
            if "error" in resp_json and isinstance(resp_json["error"], dict):
                err_code = resp_json["error"].get("code")
                err_msg = resp_json["error"].get("message")
            elif "template" in resp_json and isinstance(resp_json["template"], dict):
                created_id = resp_json["template"].get("id")
            elif "id" in resp_json:
                created_id = resp_json.get("id")
    except:
        resp_json = resp_text[:300]
        
    doc_after = get_mongo_doc(target_id or created_id)
    
    passed = False
    if isinstance(expected_status, list):
        passed = status in expected_status
    else:
        passed = (status == expected_status)
        
    res_obj = {
        "test_id": test_id,
        "category": category,
        "method": method,
        "url": url,
        "payload": payload,
        "expected_status": expected_status,
        "actual_status": status,
        "passed": passed,
        "error_code": err_code,
        "error_message": err_msg,
        "created_id": created_id,
        "response_summary": str(resp_json)[:400],
        "mongo_before": doc_before,
        "mongo_after": doc_after,
        "notes": notes
    }
    results.append(res_obj)
    print(f"Verdict: {'PASS' if passed else 'FAIL'} | Error: {err_code} - {err_msg}")
    return res_obj

# Helper for 7 standard slots
def make_slots(work_days=5, daily_dur=480, start="09:00:00", end="17:00:00", day_off_dur=0):
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    slots = []
    for i, d in enumerate(days):
        is_work = (i < work_days)
        dur = daily_dur if is_work else day_off_dur
        s_time = start if is_work else "00:00:00"
        e_time = end if is_work else "00:00:00"
        rec = ["First", "Second", "Third", "Fourth", "Fifth"] if is_work else []
        slots.append({
            "workDurationInMinutes": dur,
            "dayEnum": d,
            "isWorkingDay": is_work,
            "recurrenceOfMonth": rec,
            "startTime": s_time,
            "endTime": e_time
        })
    return slots

# ==============================================================================
# SECTION 1: POSITIVE POST SCENARIOS (ROT-P01 to ROT-P13)
# ==============================================================================

# ROT-P01: Standard 5 working days (Sun-Thu), 2 days off (Fri-Sat) in Location 3
p1_payload = {
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "templateName": {"en": "Rotation Standard 5D", "ar": "تناوب قياسي 5 أيام"},
    "shortCode": "ROTP001",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": make_slots(5, 480, "09:00:00", "17:00:00")
}
r_p01 = run_test("ROT-P01", "Positive POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", p1_payload, 200, "Valid 5 working days, 2 days off")
rot_primary_id = r_p01.get("created_id") if r_p01 else None

# ROT-P02: 6 working days (Sun-Fri), 1 day off (Sat)
p2_payload = {
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "templateName": {"en": "Rotation 6D Shift", "ar": "تناوب 6 أيام"},
    "shortCode": "ROTP002",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2880,
    "totalWorkingDays": 6,
    "totalDaysOff": 1,
    "rotationTimeSlots": make_slots(6, 480, "09:00:00", "17:00:00")
}
run_test("ROT-P02", "Positive POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", p2_payload, 200, "Valid 6 working days, 1 off day")

# ROT-P03: 4 working days (Sun-Wed), 3 days off (Thu-Sat)
p3_payload = {
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "templateName": {"en": "Rotation 4D Shift", "ar": "تناوب 4 أيام"},
    "shortCode": "ROTP003",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 1920,
    "totalWorkingDays": 4,
    "totalDaysOff": 3,
    "rotationTimeSlots": make_slots(4, 480, "09:00:00", "17:00:00")
}
run_test("ROT-P03", "Positive POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", p3_payload, 200, "Valid 4 working days, 3 off days")

# ROT-P04: 7 working days (All 7 days working, 0 off days)
p4_payload = {
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "templateName": {"en": "Rotation 7D Continuous", "ar": "تناوب 7 أيام متواصل"},
    "shortCode": "ROTP004",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 3360,
    "totalWorkingDays": 7,
    "totalDaysOff": 0,
    "rotationTimeSlots": make_slots(7, 480, "09:00:00", "17:00:00")
}
run_test("ROT-P04", "Positive POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", p4_payload, [200, 400], "Valid 7 working days if supported")

# ROT-P05: 1 working day (Sun working, 6 days off)
p5_payload = {
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "templateName": {"en": "Rotation 1D Single Day", "ar": "تناوب يوم واحد"},
    "shortCode": "ROTP005",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 1,
    "totalDaysOff": 6,
    "rotationTimeSlots": make_slots(1, 480, "09:00:00", "17:00:00")
}
run_test("ROT-P05", "Positive POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", p5_payload, [200, 400], "Valid 1 working day if supported")

# ROT-P06: Different working hours by day (Sun 8h, Mon 9h, Tue 7h, Wed 8h, Thu 6h = 38h = 2280 min)
slots_diff = [
    {"workDurationInMinutes": 480, "dayEnum": "Sun", "isWorkingDay": True, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "17:00:00"},
    {"workDurationInMinutes": 540, "dayEnum": "Mon", "isWorkingDay": True, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "08:00:00", "endTime": "17:00:00"},
    {"workDurationInMinutes": 420, "dayEnum": "Tue", "isWorkingDay": True, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "16:00:00"},
    {"workDurationInMinutes": 480, "dayEnum": "Wed", "isWorkingDay": True, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "17:00:00"},
    {"workDurationInMinutes": 360, "dayEnum": "Thu", "isWorkingDay": True, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "15:00:00"},
    {"workDurationInMinutes": 0, "dayEnum": "Fri", "isWorkingDay": False, "recurrenceOfMonth": [], "startTime": "00:00:00", "endTime": "00:00:00"},
    {"workDurationInMinutes": 0, "dayEnum": "Sat", "isWorkingDay": False, "recurrenceOfMonth": [], "startTime": "00:00:00", "endTime": "00:00:00"}
]
p6_payload = {
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "templateName": {"en": "Rotation Variable Daily Hours", "ar": "تناوب ساعات متغيرة"},
    "shortCode": "ROTP006",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2280,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_diff
}
run_test("ROT-P06", "Positive POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", p6_payload, 200, "Different working hours by day")

# ROT-P07: Localized Arabic and English Names with Special Characters
p7_payload = {
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "templateName": {"en": "Rotation Specialized Shift (Operations & Logistics)", "ar": "وردية التناوب التخصصية (العمليات واللوجستيات)"},
    "shortCode": "ROTP007",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": make_slots(5, 480, "08:30:00", "16:30:00")
}
run_test("ROT-P07", "Positive POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", p7_payload, 200, "Arabic and English names")

# ROT-P08: Valid Company-level Rotation template (omitted locationId query param)
p8_payload = {
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "templateName": {"en": "Company Wide Rotation Shift", "ar": "وردية التناوب العامة للشركة"},
    "shortCode": "ROTP008",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": make_slots(5, 480, "09:00:00", "17:00:00")
}
run_test("ROT-P08", "Positive POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation", p8_payload, [200, 400], "Company-level Rotation template without locationId")

# ROT-P09: Unique 7-character alphanumeric short code
p9_payload = {
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "templateName": {"en": "Rotation AlphaNum Shift", "ar": "تناوب رمز فريد"},
    "shortCode": "ROTX999",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": make_slots(5, 480, "09:00:00", "17:00:00")
}
run_test("ROT-P09", "Positive POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", p9_payload, 200, "Unique short code")

# ROT-P10: Valid recurrence combinations (Selected weeks [First, Third, Fifth])
slots_rec = make_slots(5, 480, "09:00:00", "17:00:00")
for s in slots_rec[:5]:
    s["recurrenceOfMonth"] = ["First", "Third", "Fifth"]
p10_payload = {
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "templateName": {"en": "Rotation Bi-Weekly Recurrence", "ar": "تناوب أسبوعي متناوب"},
    "shortCode": "ROTP010",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_rec
}
run_test("ROT-P10", "Positive POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", p10_payload, 200, "Valid recurrence combinations")

# ROT-P11: Valid minimum duration (1 minute per working day)
slots_min = make_slots(5, 1, "09:00:00", "09:01:00")
p11_payload = {
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "templateName": {"en": "Rotation Minimum Duration Boundary", "ar": "تناوب الحد الأدنى للمدة"},
    "shortCode": "ROTP011",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 5,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_min
}
run_test("ROT-P11", "Positive POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", p11_payload, [200, 400], "Valid minimum duration")

# ROT-P12: Valid maximum duration (1440 min / 24 hours per working day)
slots_max = make_slots(5, 1440, "00:00:00", "23:59:59")
p12_payload = {
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "templateName": {"en": "Rotation 24H Full Day Shift", "ar": "تناوب 24 ساعة"},
    "shortCode": "ROTP012",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 7200,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_max
}
run_test("ROT-P12", "Positive POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", p12_payload, [200, 400], "Valid maximum duration boundary")

# ROT-P13: Overnight shift (e.g. 22:00:00 to 06:00:00, 480 min)
slots_night = make_slots(5, 480, "22:00:00", "06:00:00")
p13_payload = {
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "templateName": {"en": "Rotation Overnight Night Shift", "ar": "وردية التناوب الليلية"},
    "shortCode": "ROTP013",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_night
}
run_test("ROT-P13", "Positive POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", p13_payload, [200, 400], "Overnight shift (end earlier than start)")

# ==============================================================================
# SECTION 2: POSITIVE PATCH SCENARIOS (ROT-U01 to ROT-U10)
# ==============================================================================

# Target for PATCH testing: rot_primary_id or create one if needed
patch_target_id = rot_primary_id or "5aa227f7-3b96-444c-9c2d-51ecbf52b7ee"
patch_code = "ROTP001" if rot_primary_id else "ROT0002"

# ROT-U01: Update template name only
u1_payload = {
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "templateName": {"en": "Rotation Updated Name Only", "ar": "تحديث الاسم فقط"},
    "shortCode": patch_code,
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": make_slots(5, 480, "09:00:00", "17:00:00")
}
run_test("ROT-U01", "Positive PATCH", "PATCH", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation/{patch_target_id}?locationId={LOC3_ID}", u1_payload, 200, "Update template name")

# ROT-U02: Update daily hours (8h -> 6h, total 2400 -> 1800)
u2_payload = {
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "templateName": {"en": "Rotation 6H Schedule", "ar": "تناوب 6 ساعات يوميا"},
    "shortCode": patch_code,
    "totalWorkDurationInMinutes": 1800,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": make_slots(5, 360, "09:00:00", "15:00:00")
}
run_test("ROT-U02", "Positive PATCH", "PATCH", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation/{patch_target_id}?locationId={LOC3_ID}", u2_payload, 200, "Update daily hours")

# ROT-U03: Change working days (5 days -> 4 days, total 1800 -> 1440)
u3_payload = {
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "templateName": {"en": "Rotation 4 Days Schedule", "ar": "تناوب 4 أيام عمل"},
    "shortCode": patch_code,
    "totalWorkDurationInMinutes": 1440,
    "totalWorkingDays": 4,
    "totalDaysOff": 3,
    "rotationTimeSlots": make_slots(4, 360, "09:00:00", "15:00:00")
}
run_test("ROT-U03", "Positive PATCH", "PATCH", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation/{patch_target_id}?locationId={LOC3_ID}", u3_payload, 200, "Change working days")

# ROT-U04: Change day-off pattern (Off on Sun & Mon instead of Fri & Sat)
slots_off_sun_mon = [
    {"workDurationInMinutes": 0, "dayEnum": "Sun", "isWorkingDay": False, "recurrenceOfMonth": [], "startTime": "00:00:00", "endTime": "00:00:00"},
    {"workDurationInMinutes": 0, "dayEnum": "Mon", "isWorkingDay": False, "recurrenceOfMonth": [], "startTime": "00:00:00", "endTime": "00:00:00"},
    {"workDurationInMinutes": 480, "dayEnum": "Tue", "isWorkingDay": True, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "17:00:00"},
    {"workDurationInMinutes": 480, "dayEnum": "Wed", "isWorkingDay": True, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "17:00:00"},
    {"workDurationInMinutes": 480, "dayEnum": "Thu", "isWorkingDay": True, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "17:00:00"},
    {"workDurationInMinutes": 480, "dayEnum": "Fri", "isWorkingDay": True, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "17:00:00"},
    {"workDurationInMinutes": 480, "dayEnum": "Sat", "isWorkingDay": True, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "17:00:00"}
]
u4_payload = {
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "templateName": {"en": "Rotation Tue-Sat Shift", "ar": "تناوب من الثلاثاء للسبت"},
    "shortCode": patch_code,
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_off_sun_mon
}
run_test("ROT-U04", "Positive PATCH", "PATCH", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation/{patch_target_id}?locationId={LOC3_ID}", u4_payload, 200, "Change day-off pattern")

# ROT-U05: Update recurrence pattern ([First, Third] only)
slots_u5 = make_slots(5, 480, "09:00:00", "17:00:00")
for s in slots_u5[:5]:
    s["recurrenceOfMonth"] = ["First", "Third"]
u5_payload = {
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "templateName": {"en": "Rotation 1st and 3rd Weeks", "ar": "تناوب الأسبوع الأول والثالث"},
    "shortCode": patch_code,
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_u5
}
run_test("ROT-U05", "Positive PATCH", "PATCH", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation/{patch_target_id}?locationId={LOC3_ID}", u5_payload, 200, "Update recurrence")

# ROT-U06: Update slot start/end times (08:00:00 to 16:00:00)
u6_payload = {
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "templateName": {"en": "Rotation 08:00 to 16:00", "ar": "تناوب من 8 إلى 4"},
    "shortCode": patch_code,
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": make_slots(5, 480, "08:00:00", "16:00:00")
}
run_test("ROT-U06", "Positive PATCH", "PATCH", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation/{patch_target_id}?locationId={LOC3_ID}", u6_payload, 200, "Update slot times")

# ROT-U07: Update localization (New Arabic & English names)
u7_payload = {
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "templateName": {"en": "Rotation Fully Localized V2", "ar": "وردية التناوب المعربة بالكامل الإصدار الثاني"},
    "shortCode": patch_code,
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": make_slots(5, 480, "08:00:00", "16:00:00")
}
run_test("ROT-U07", "Positive PATCH", "PATCH", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation/{patch_target_id}?locationId={LOC3_ID}", u7_payload, 200, "Update localization")

# ROT-U08: Update all editable fields simultaneously
u8_payload = {
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "templateName": {"en": "Rotation Master Updated All Fields", "ar": "تناوب شامل التحديث لكافة الحقول"},
    "shortCode": patch_code,
    "totalWorkDurationInMinutes": 2100,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": make_slots(5, 420, "08:30:00", "15:30:00")
}
run_test("ROT-U08", "Positive PATCH", "PATCH", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation/{patch_target_id}?locationId={LOC3_ID}", u8_payload, 200, "Update all editable fields")

# ROT-U09: Update location-level Rotation template preserving LocationId
run_test("ROT-U09", "Positive PATCH", "PATCH", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation/{patch_target_id}?locationId={LOC3_ID}", u8_payload, 200, "Update location-level Rotation template")

# ROT-U10: Repeat unchanged payload (idempotency check)
run_test("ROT-U10", "Positive PATCH", "PATCH", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation/{patch_target_id}?locationId={LOC3_ID}", u8_payload, 200, "Repeat unchanged payload")

# Save checkpoint
with open("scratch/rotation_test_suite_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
print("Saved Section 1 & 2 results. Count:", len(results))

# ==============================================================================
# SECTION 3: NEGATIVE POST & PATCH SCENARIOS (ROT-N01 to ROT-N45)
# ==============================================================================

# ROT-N01: Duplicate short code (ROTP001 already created)
n1_payload = {
    "templateName": {"en": "Duplicate Code Shift", "ar": "رمز مكرر"},
    "shortCode": "ROTP001",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": make_slots(5, 480)
}
run_test("ROT-N01", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n1_payload, 400, "Duplicate short code")

# ROT-N02: Duplicate template name (same as ROT-P01, unique shortCode)
n2_payload = {
    "templateName": {"en": "Rotation Standard 5D", "ar": "تناوب قياسي 5 أيام"},
    "shortCode": "ROTN002",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": make_slots(5, 480)
}
run_test("ROT-N02", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n2_payload, [200, 400], "Duplicate template name check")

# ROT-N03: Empty name {"en": "", "ar": ""}
n3_payload = {
    "templateName": {"en": "", "ar": ""},
    "shortCode": "ROTN003",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": make_slots(5, 480)
}
run_test("ROT-N03", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n3_payload, 400, "Empty template name")

# ROT-N04: Null name
n4_payload = {
    "templateName": None,
    "shortCode": "ROTN004",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": make_slots(5, 480)
}
run_test("ROT-N04", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n4_payload, 400, "Null template name")

# ROT-N05: Missing short code (omitted)
n5_payload = {
    "templateName": {"en": "Missing Code Shift"},
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": make_slots(5, 480)
}
run_test("ROT-N05", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n5_payload, 400, "Missing short code")

# ROT-N06: Empty short code ""
n6_payload = {
    "templateName": {"en": "Empty Code Shift"},
    "shortCode": "",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": make_slots(5, 480)
}
run_test("ROT-N06", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n6_payload, 400, "Empty short code")

# ROT-N07: Invalid template type "Fixed"
n7_payload = {
    "templateName": {"en": "Wrong Type Shift"},
    "shortCode": "ROTN007",
    "templateType": "Fixed",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": make_slots(5, 480)
}
run_test("ROT-N07", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n7_payload, 400, "Invalid template type Fixed")

# ROT-N08: NotApplicable template type
n8_payload = {
    "templateName": {"en": "NotApplicable Type Shift"},
    "shortCode": "ROTN008",
    "templateType": "NotApplicable",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": make_slots(5, 480)
}
run_test("ROT-N08", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n8_payload, 400, "NotApplicable template type")

# ROT-N09: Invalid weekday enum "InvalidDay"
slots_n9 = make_slots(5, 480)
slots_n9[0]["dayEnum"] = "InvalidDay"
n9_payload = {
    "templateName": {"en": "Invalid Day Shift"},
    "shortCode": "ROTN009",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_n9
}
run_test("ROT-N09", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n9_payload, 400, "Invalid weekday enum InvalidDay")

# ROT-N10: Duplicate weekday (two "Mon" rows instead of Sun and Mon)
slots_n10 = make_slots(5, 480)
slots_n10[0]["dayEnum"] = "Mon"
n10_payload = {
    "templateName": {"en": "Duplicate Weekday Shift"},
    "shortCode": "ROTN010",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_n10
}
run_test("ROT-N10", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n10_payload, 400, "Duplicate weekday Mon")

# ROT-N11: Missing weekday (six rows instead of seven)
n11_payload = {
    "templateName": {"en": "Six Days Shift"},
    "shortCode": "ROTN011",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 1,
    "rotationTimeSlots": make_slots(5, 480)[:6]
}
run_test("ROT-N11", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n11_payload, 400, "Missing weekday (6 rows)")

# ROT-N12: Extra weekday (eight rows)
slots_n12 = make_slots(5, 480)
slots_n12.append({"workDurationInMinutes": 0, "dayEnum": "Sun", "isWorkingDay": False, "recurrenceOfMonth": [], "startTime": "00:00:00", "endTime": "00:00:00"})
n12_payload = {
    "templateName": {"en": "Eight Days Shift"},
    "shortCode": "ROTN012",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 3,
    "rotationTimeSlots": slots_n12
}
run_test("ROT-N12", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n12_payload, 400, "Extra weekday (8 rows)")

# ROT-N13: Empty slots []
n13_payload = {
    "templateName": {"en": "Empty Slots Shift"},
    "shortCode": "ROTN013",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 0,
    "totalWorkingDays": 0,
    "totalDaysOff": 0,
    "rotationTimeSlots": []
}
run_test("ROT-N13", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n13_payload, 400, "Empty rotationTimeSlots")

# ROT-N14: Null slots null
n14_payload = {
    "templateName": {"en": "Null Slots Shift"},
    "shortCode": "ROTN014",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 0,
    "totalWorkingDays": 0,
    "totalDaysOff": 0,
    "rotationTimeSlots": None
}
run_test("ROT-N14", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n14_payload, 400, "Null rotationTimeSlots")

# ROT-N15: Negative duration -1
slots_n15 = make_slots(5, 480)
slots_n15[0]["workDurationInMinutes"] = -1
n15_payload = {
    "templateName": {"en": "Negative Duration Shift"},
    "shortCode": "ROTN015",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_n15
}
run_test("ROT-N15", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n15_payload, 400, "Negative duration -1")

# ROT-N16: Decimal duration 480.5
slots_n16 = make_slots(5, 480)
slots_n16[0]["workDurationInMinutes"] = 480.5
n16_payload = {
    "templateName": {"en": "Decimal Duration Shift"},
    "shortCode": "ROTN016",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400.5,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_n16
}
run_test("ROT-N16", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n16_payload, [200, 400], "Decimal duration 480.5 (double vs int)")

# ROT-N17: Working day zero duration
slots_n17 = make_slots(5, 480)
slots_n17[0]["workDurationInMinutes"] = 0
n17_payload = {
    "templateName": {"en": "Zero Duration Working Day"},
    "shortCode": "ROTN017",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 1920,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_n17
}
run_test("ROT-N17", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n17_payload, 400, "Working day with zero duration")

# ROT-N18: Day off non-zero duration
slots_n18 = make_slots(5, 480)
slots_n18[5]["workDurationInMinutes"] = 480 # Friday is day off
n18_payload = {
    "templateName": {"en": "NonZero Duration Day Off"},
    "shortCode": "ROTN018",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2880,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_n18
}
run_test("ROT-N18", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n18_payload, 400, "Day off with non-zero duration")

# ROT-N19: Total duration mismatch (1500 declared vs 2400 actual sum)
n19_payload = {
    "templateName": {"en": "Duration Mismatch Shift"},
    "shortCode": "ROTN019",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 1500, # Declared 1500, actual 5*480 = 2400
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": make_slots(5, 480)
}
run_test("ROT-N19", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n19_payload, 400, "Total duration mismatch (1500 vs 2400)")

# ROT-N20: Working-day count mismatch (declared 4 vs actual 5)
n20_payload = {
    "templateName": {"en": "Working Day Count Mismatch"},
    "shortCode": "ROTN020",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 4, # Declared 4, actual 5
    "totalDaysOff": 2,
    "rotationTimeSlots": make_slots(5, 480)
}
run_test("ROT-N20", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n20_payload, 400, "Working day count mismatch (4 vs 5)")

# ROT-N21: Day-off count mismatch (declared 3 vs actual 2)
n21_payload = {
    "templateName": {"en": "Day Off Count Mismatch"},
    "shortCode": "ROTN021",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 3, # Declared 3, actual 2
    "rotationTimeSlots": make_slots(5, 480)
}
run_test("ROT-N21", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n21_payload, 400, "Day off count mismatch (3 vs 2)")

# ROT-N22: Invalid start time "25:00:00"
slots_n22 = make_slots(5, 480)
slots_n22[0]["startTime"] = "25:00:00"
n22_payload = {
    "templateName": {"en": "Invalid Start Time Shift"},
    "shortCode": "ROTN022",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_n22
}
run_test("ROT-N22", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n22_payload, 400, "Invalid start time 25:00:00")

# ROT-N23: Invalid end time "99:00:00"
slots_n23 = make_slots(5, 480)
slots_n23[0]["endTime"] = "99:00:00"
n23_payload = {
    "templateName": {"en": "Invalid End Time Shift"},
    "shortCode": "ROTN023",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_n23
}
run_test("ROT-N23", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n23_payload, 400, "Invalid end time 99:00:00")

# ROT-N24: Start equals end "09:00:00" on working day with 480 duration
slots_n24 = make_slots(5, 480)
slots_n24[0]["startTime"] = "09:00:00"
slots_n24[0]["endTime"] = "09:00:00"
n24_payload = {
    "templateName": {"en": "Start Equals End Shift"},
    "shortCode": "ROTN024",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_n24
}
run_test("ROT-N24", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n24_payload, 400, "Start equals end with 480m duration")

# ROT-N25: End earlier than start on non-overnight slot without duration justification
slots_n25 = make_slots(5, 480)
slots_n25[0]["startTime"] = "17:00:00"
slots_n25[0]["endTime"] = "09:00:00"
slots_n25[0]["workDurationInMinutes"] = 480
n25_payload = {
    "templateName": {"en": "End Earlier Than Start Shift"},
    "shortCode": "ROTN025",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_n25
}
run_test("ROT-N25", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n25_payload, [200, 400], "End earlier than start")

# ROT-N26: Duration/time mismatch (480 minutes declared for 09:00 to 15:00 = 360m window)
slots_n26 = make_slots(5, 480)
slots_n26[0]["startTime"] = "09:00:00"
slots_n26[0]["endTime"] = "15:00:00" # 6 hours window
slots_n26[0]["workDurationInMinutes"] = 480 # 8 hours duration!
n26_payload = {
    "templateName": {"en": "Slot Duration Time Window Mismatch"},
    "shortCode": "ROTN026",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_n26
}
run_test("ROT-N26", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n26_payload, 400, "Slot duration exceeds time window")

# ROT-N27: Invalid recurrence "Sixth" or out-of-range index 6
slots_n27 = make_slots(5, 480)
slots_n27[0]["recurrenceOfMonth"] = ["Sixth"]
n27_payload = {
    "templateName": {"en": "Invalid Recurrence Sixth"},
    "shortCode": "ROTN027",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_n27
}
run_test("ROT-N27", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n27_payload, 400, "Invalid recurrence Sixth")

# ROT-N28: Duplicate recurrence ["First", "First"]
slots_n28 = make_slots(5, 480)
slots_n28[0]["recurrenceOfMonth"] = ["First", "First"]
n28_payload = {
    "templateName": {"en": "Duplicate Recurrence Shift"},
    "shortCode": "ROTN028",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_n28
}
run_test("ROT-N28", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n28_payload, [200, 400], "Duplicate recurrence First, First")

# ROT-N29: Invalid recurrence type (string instead of array)
slots_n29 = make_slots(5, 480)
slots_n29[0]["recurrenceOfMonth"] = "First"
n29_payload = {
    "templateName": {"en": "Recurrence String Shift"},
    "shortCode": "ROTN029",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_n29
}
run_test("ROT-N29", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", n29_payload, 400, "Invalid recurrence type string")

# ROT-N30: Invalid CompanyId (malformed UUID)
run_test("ROT-N30", "Negative POST", "POST", f"{BASE_URL}/companies/invalid-uuid/worktemplates/rotation?locationId={LOC3_ID}", p1_payload, 404, "Invalid CompanyId route")

# ROT-N31: Invalid LocationId (malformed UUID)
run_test("ROT-N31", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId=malformed-location-uuid", p1_payload, 400, "Invalid LocationId query param")

# ROT-N32: Company/Location mismatch (Location from Naturals company)
n32_payload = {
    "templateName": {"en": "Cross Company Loc Shift"},
    "shortCode": "ROTN032",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": make_slots(5, 480)
}
run_test("ROT-N32", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={OTHER_LOC_ID}", n32_payload, [400, 404], "Company/location mismatch")

# ROT-N33: Duplicate request (attempt to create with same shortCode ROTP001)
run_test("ROT-N33", "Negative POST", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", p1_payload, 400, "Duplicate request with same shortCode")

# ROT-N34: Wrong company on PATCH (Naturals company ID with Attendance 8 template ID)
run_test("ROT-N34", "Negative PATCH", "PATCH", f"{BASE_URL}/companies/{OTHER_COMPANY_ID}/worktemplates/rotation/{patch_target_id}?locationId={LOC3_ID}", u1_payload, [400, 404], "Wrong company on PATCH")

# ROT-N35: Nonexistent template ID on PATCH
random_id = str(uuid.uuid4())
run_test("ROT-N35", "Negative PATCH", "PATCH", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation/{random_id}?locationId={LOC3_ID}", u1_payload, 404, "Nonexistent template ID on PATCH")

# ROT-N36: Invalid PATCH ID (malformed UUID)
run_test("ROT-N36", "Negative PATCH", "PATCH", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation/invalid-id-string?locationId={LOC3_ID}", u1_payload, 404, "Invalid PATCH ID string")

# ROT-N37: Attempt to modify immutable short code on PATCH
u37_payload = dict(u1_payload)
u37_payload["shortCode"] = "ROTMUT8"
run_test("ROT-N37", "Negative PATCH", "PATCH", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation/{patch_target_id}?locationId={LOC3_ID}", u37_payload, [200, 400], "Attempt to modify immutable short code on PATCH")

# ROT-N38: Attempt to change Rotation to Fixed on PATCH
u38_payload = dict(u1_payload)
u38_payload["templateType"] = "Fixed"
run_test("ROT-N38", "Negative PATCH", "PATCH", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation/{patch_target_id}?locationId={LOC3_ID}", u38_payload, [200, 400], "Change Rotation to Fixed on PATCH")

# ROT-N39: Update Fixed template through Rotation endpoint
# Target Fixed template from earlier: 0ba519c8-c2e2-4bce-8a70-23b1616ed5f7
run_test("ROT-N39", "Negative PATCH", "PATCH", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation/0ba519c8-c2e2-4bce-8a70-23b1616ed5f7?locationId={LOC3_ID}", u1_payload, [400, 404], "Update Fixed template through Rotation endpoint")

# ROT-N40: Update Flexi/Split template through Rotation endpoint
# Target Flexi: 7ecfbe95-8d3c-4612-a0cc-1454e9093a53
run_test("ROT-N40", "Negative PATCH", "PATCH", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation/7ecfbe95-8d3c-4612-a0cc-1454e9093a53?locationId={LOC3_ID}", u1_payload, [400, 404], "Update Flexi template through Rotation endpoint")

# ROT-N41: Update soft-deleted Rotation template (DEFECT-15 check on Rotation!)
# First soft-delete a template or use existing soft-deleted template
# Soft-deleted rotation template or create a throwaway rotation, delete it, then try PATCH!
p_throw = {
    "templateName": {"en": "Throwaway Rotation For Delete Check"},
    "shortCode": "ROTDEL1",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": make_slots(5, 480)
}
res_del = requests.post(f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", headers=headers_auth, json=p_throw)
if res_del.status_code == 200:
    del_target = res_del.json().get("template", {}).get("id")
    # Soft delete it
    requests.patch(f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/{del_target}/delete?locationId={LOC3_ID}", headers=headers_auth)
    # Now attempt to PATCH it
    u_del_payload = dict(u1_payload)
    u_del_payload["shortCode"] = "ROTDEL1"
    run_test("ROT-N41", "Negative PATCH", "PATCH", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation/{del_target}?locationId={LOC3_ID}", u_del_payload, [400, 404], "Update soft-deleted Rotation template")

# ROT-N42: Update non-editable / protected template
# 59dd499a-0f08-4ae0-8a20-05682614d27f has IsEditable: false in Naturals company
run_test("ROT-N42", "Negative PATCH", "PATCH", f"{BASE_URL}/companies/{OTHER_COMPANY_ID}/worktemplates/rotation/59dd499a-0f08-4ae0-8a20-05682614d27f?locationId={OTHER_LOC_ID}", u1_payload, [400, 403, 404], "Update non-editable template")

# ROT-N43: Missing authorization (no bearer token)
run_test("ROT-N43", "Negative Auth", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", p1_payload, 401, "Missing bearer token", headers=headers_noauth)

# ROT-N44: Unauthorized company access (using invalid company header/context)
bad_comp_id = "00000000-0000-0000-0000-000000000000"
run_test("ROT-N44", "Negative Auth", "POST", f"{BASE_URL}/companies/{bad_comp_id}/worktemplates/rotation?locationId={LOC3_ID}", p1_payload, [400, 404], "Unauthorized/empty company")

# ROT-N45: Unexpected extra DTO property
p45_payload = dict(p1_payload)
p45_payload["shortCode"] = "ROTN045"
p45_payload["unexpectedField"] = "InjectingExtraData"
run_test("ROT-N45", "Negative DTO", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", p45_payload, [200, 400], "Unexpected extra DTO property")

# ==============================================================================
# SECTION 4: BOUNDARY VALUE ANALYSIS & EQUIVALENCE PARTITIONING (ROT-B01 to ROT-B15)
# ==============================================================================

# ROT-B01: RecurrenceOfMonth [0] (Numeric 0) on working day
slots_b1 = make_slots(5, 480)
slots_b1[0]["recurrenceOfMonth"] = [0]
b1_payload = {
    "templateName": {"en": "Recurrence Index 0 Boundary"},
    "shortCode": "ROTB001",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_b1
}
run_test("ROT-B01", "BVA Boundary", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", b1_payload, 400, "RecurrenceOfMonth index [0]")

# ROT-B02: RecurrenceOfMonth [6] (Numeric 6) on working day
slots_b2 = make_slots(5, 480)
slots_b2[0]["recurrenceOfMonth"] = [6]
b2_payload = {
    "templateName": {"en": "Recurrence Index 6 Boundary"},
    "shortCode": "ROTB002",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_b2
}
run_test("ROT-B02", "BVA Boundary", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", b2_payload, 400, "RecurrenceOfMonth index [6]")

# ROT-B03: DayEnum numeric 0
slots_b3 = make_slots(5, 480)
slots_b3[0]["dayEnum"] = 0
b3_payload = {
    "templateName": {"en": "DayEnum 0 Boundary"},
    "shortCode": "ROTB003",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_b3
}
run_test("ROT-B03", "BVA Boundary", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", b3_payload, 400, "DayEnum numeric 0")

# ROT-B04: DayEnum numeric 8
slots_b4 = make_slots(5, 480)
slots_b4[0]["dayEnum"] = 8
b4_payload = {
    "templateName": {"en": "DayEnum 8 Boundary"},
    "shortCode": "ROTB004",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_b4
}
run_test("ROT-B04", "BVA Boundary", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", b4_payload, 400, "DayEnum numeric 8")

# ROT-B05: WorkDurationInMinutes = 0 on working day
slots_b5 = make_slots(5, 0)
b5_payload = {
    "templateName": {"en": "Zero Duration All Working Days"},
    "shortCode": "ROTB005",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 0,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_b5
}
run_test("ROT-B05", "BVA Boundary", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", b5_payload, 400, "0 duration on all working days")

# ROT-B06: WorkDurationInMinutes = 1441 (> 24 hours per day)
slots_b6 = make_slots(5, 1441)
b6_payload = {
    "templateName": {"en": "Over 24H Duration Shift"},
    "shortCode": "ROTB006",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 7205,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots_b6
}
run_test("ROT-B06", "BVA Boundary", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", b6_payload, 400, "1441m (>24h) daily duration")

# ROT-B07: Continuous 10,080 min weekly work duration (168h nonstop week)
slots_b7 = make_slots(7, 1440)
b7_payload = {
    "templateName": {"en": "Continuous 168H Nonstop Rotation"},
    "shortCode": "ROTB007",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 10080,
    "totalWorkingDays": 7,
    "totalDaysOff": 0,
    "rotationTimeSlots": slots_b7
}
run_test("ROT-B07", "BVA Boundary", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", b7_payload, [200, 400], "Continuous 10,080m weekly duration")

# ROT-B08: TotalWorkingDays = 8
b8_payload = {
    "templateName": {"en": "Total Working Days 8"},
    "shortCode": "ROTB008",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 8,
    "totalDaysOff": 0,
    "rotationTimeSlots": make_slots(7, 480)
}
run_test("ROT-B08", "BVA Boundary", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", b8_payload, 400, "TotalWorkingDays = 8")

# ROT-B09: TotalDaysOff = -1
b9_payload = {
    "templateName": {"en": "Negative Days Off"},
    "shortCode": "ROTB009",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": -1,
    "rotationTimeSlots": make_slots(5, 480)
}
run_test("ROT-B09", "BVA Boundary", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", b9_payload, 400, "TotalDaysOff = -1")

# ROT-B10: TotalDaysOff = 8
b10_payload = {
    "templateName": {"en": "Days Off 8 Boundary"},
    "shortCode": "ROTB010",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 0,
    "totalWorkingDays": 0,
    "totalDaysOff": 8,
    "rotationTimeSlots": make_slots(0, 0)
}
run_test("ROT-B10", "BVA Boundary", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", b10_payload, 400, "TotalDaysOff = 8")

# ROT-B11: Int32 Overflow on totalWorkDurationInMinutes (2147483648)
b11_payload = {
    "templateName": {"en": "Int32 Overflow Duration"},
    "shortCode": "ROTB011",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2147483648,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": make_slots(5, 480)
}
run_test("ROT-B11", "BVA Boundary", "POST", f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation?locationId={LOC3_ID}", b11_payload, 400, "Int32 overflow duration")

# Final Save
with open("scratch/rotation_test_suite_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
print("COMPLETED FULL SUITE! Total tests executed:", len(results))
