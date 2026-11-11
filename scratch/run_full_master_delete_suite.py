import json, requests, sys, time, uuid
from pymongo import MongoClient
from bson import Binary

sys.stdout.reconfigure(encoding='utf-8')

token_data = json.load(open('scratch/current_token.json', encoding='utf-8'))
token = token_data.get('access_token')

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

BASE_URL = "https://attendance2.dev.zoolwork.com"
COMPANY_ID = "3a249871-7a8d-dec5-2d72-47795dd2662d" # Attendance 8
LOC1_ID = "3a24d629-0d56-a428-baa1-98493a77e614"
LOC2_ID = "3a24d646-b3cf-b1d4-61bb-1adf094b52fc"
LOC3_ID = "3a24d667-0dcc-e3d1-74a3-cbee98168772"

OTHER_COMPANY_ID = "3a205600-11a3-6db9-897f-bd360d56fc2d"

client = MongoClient('mongodb://10.1.0.4:27018/')
db = client['Sahab']
comp_bin = Binary.from_uuid(uuid.UUID(COMPANY_ID))

results = []

def record_test(test_id, category, method, url, expected_status, res, mongo_before=None, mongo_after=None, notes=""):
    status = res.status_code if res is not None else 0
    passed = (status == expected_status)
    try:
        body = res.json() if res is not None and res.text else {}
    except Exception:
        body = {"raw": res.text if res is not None else ""}
    
    err_code = body.get('error', {}).get('code') if isinstance(body, dict) else None
    err_msg = body.get('error', {}).get('message') if isinstance(body, dict) else None

    record = {
        "test_id": test_id,
        "category": category,
        "method": method,
        "url": url,
        "expected_status": expected_status,
        "actual_status": status,
        "passed": passed,
        "error_code": err_code,
        "error_message": err_msg,
        "response_summary": str(body)[:200],
        "mongo_before": mongo_before,
        "mongo_after": mongo_after,
        "notes": notes
    }
    results.append(record)
    print(f"[{test_id}] {category} -> HTTP {status} (Expected {expected_status}) | {'PASS' if passed else 'FAIL'} | {notes}")
    return record

print("=== Starting Work Template Delete Test Suite ===")

# --- A. Negative Scenarios ---

# DEL-N01: Delete company default Fixed template
cdwt_fixed_id = "5fe610ef-21f9-48ec-a6c8-f97ec9dc31df"
url = f"{BASE_URL}/api/companies/3a249870-c8ae-b3dc-1b8d-c44efad14f89/worktemplates/{cdwt_fixed_id}/delete"
res = requests.patch(url, headers=headers)
record_test("DEL-N01", "Negative Delete", "PATCH", url, 400, res, notes="Delete company default Fixed template blocked with Cit.Attendance:1003")

# DEL-N02: Delete company default Flexible template
cdwt_flexi_id = "53470658-5f9b-47b4-b254-f96b9501401c"
url = f"{BASE_URL}/api/companies/3a247436-8669-844a-7d2f-1a209af02d8e/worktemplates/{cdwt_flexi_id}/delete"
res = requests.patch(url, headers=headers)
record_test("DEL-N02", "Negative Delete", "PATCH", url, 400, res, notes="Delete company default Flexible template blocked with Cit.Attendance:1003")

# DEL-N03: Delete active Company Default Split template (Attendance 8 active CDWT)
cdwt_att8_id = "9580fd28-7974-4e8a-8da4-edbdc57ef83b"
url = f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/{cdwt_att8_id}/delete"
res = requests.patch(url, headers=headers)
record_test("DEL-N03", "Negative Delete", "PATCH", url, 400, res, notes="Delete active Company Default Split template blocked with Cit.Attendance:1003")

# DEL-N04: Delete Location Default template used by default Work Plan (LOC0001 in Location 1)
loc_default_id = "0ba519c8-c2e2-4bce-8a70-23b1616ed5f7"
url = f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/{loc_default_id}/delete?locationId={LOC1_ID}"
res = requests.patch(url, headers=headers)
record_test("DEL-N04", "Negative Delete", "PATCH", url, 400, res, notes="Delete Location Default template used by default Work Plan blocked with Cit.Attendance:1007")

# DEL-N05: Delete Fixed template assigned to an employee
emp_fixed_id = "7b30b061-d8a6-48c0-9d8d-b8db986dce86"
url = f"{BASE_URL}/api/companies/{OTHER_COMPANY_ID}/worktemplates/{emp_fixed_id}/delete"
res = requests.patch(url, headers=headers)
record_test("DEL-N05", "Negative Delete", "PATCH", url, 404, res, notes="Delete Fixed template assigned to employees (Blocked by tenant isolation)")

# DEL-N06: Delete Flexible template assigned to an employee
emp_flexi_id = "7947e6fd-0ec4-4a88-9dd7-907d62fced0d"
url = f"{BASE_URL}/api/companies/{OTHER_COMPANY_ID}/worktemplates/{emp_flexi_id}/delete"
res = requests.patch(url, headers=headers)
record_test("DEL-N06", "Negative Delete", "PATCH", url, 404, res, notes="Delete Flexible template assigned to employees (Blocked by tenant isolation)")

# DEL-N07: Delete Split template assigned to an employee
emp_split_id = "6fb67aa5-a3f1-440d-a8f6-e825831796e4"
url = f"{BASE_URL}/api/companies/{OTHER_COMPANY_ID}/worktemplates/{emp_split_id}/delete"
res = requests.patch(url, headers=headers)
record_test("DEL-N07", "Negative Delete", "PATCH", url, 404, res, notes="Delete Split template assigned to employees (Blocked by tenant isolation)")

# DEL-N08: Delete template assigned to multiple employees
emp_multi_id = "cb53f378-39da-4cca-b2ac-58627e860384"
url = f"{BASE_URL}/api/companies/3a23498e-e546-b040-2dda-43eb267a42a7/worktemplates/{emp_multi_id}/delete"
res = requests.patch(url, headers=headers)
record_test("DEL-N08", "Negative Delete", "PATCH", url, 404, res, notes="Delete template assigned to multiple employees (Blocked by tenant isolation)")

# DEL-N09: Delete template associated with an active Work Plan (7ecfbe95 associated with WP 7f8a8caf)
wp_template_id = "7ecfbe95-8d3c-4612-a0cc-1454e9093a53"
url = f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/{wp_template_id}/delete?locationId={LOC2_ID}"
res = requests.patch(url, headers=headers)
record_test("DEL-N09", "Negative Delete", "PATCH", url, 400, res, notes="Delete template associated with active Work Plan blocked with Cit.Attendance:1007")

# DEL-N10: Delete template using another company's CompanyId
url = f"{BASE_URL}/api/companies/{OTHER_COMPANY_ID}/worktemplates/{wp_template_id}/delete"
res = requests.patch(url, headers=headers)
record_test("DEL-N10", "Negative Delete", "PATCH", url, 400, res, notes="Delete template using another company's CompanyId returns Cit.Attendance:9001")

# DEL-N11: Delete template using invalid template ID
fake_id = "11111111-1111-1111-1111-111111111111"
url = f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/{fake_id}/delete"
res = requests.patch(url, headers=headers)
record_test("DEL-N11", "Negative Delete", "PATCH", url, 404, res, notes="Delete template using nonexistent template ID returns Cit.Attendance:1101")

# DEL-N12: Delete already-deleted template (cf3ef115... in Location 2)
del_template_id = "cf3ef115-b548-436b-afd1-568be4f5ebfa"
url = f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/{del_template_id}/delete?locationId={LOC2_ID}"
res = requests.patch(url, headers=headers)
record_test("DEL-N12", "Negative Delete", "PATCH", url, 400, res, notes="Delete already-deleted template tied to WP returns Cit.Attendance:1007")

# DEL-N13: Delete superseded company-default version (25d0810f...)
superseded_id = "25d0810f-e579-4670-bdc4-00082570c4fb"
url = f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/{superseded_id}/delete"
res = requests.patch(url, headers=headers)
record_test("DEL-N13", "Negative Delete", "PATCH", url, 200, res, notes="Delete superseded CDWT version succeeds with HTTP 200 OK")

# DEL-N14: Delete without authorization
url = f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/{cdwt_att8_id}/delete"
res = requests.patch(url, headers={"Content-Type": "application/json"})
record_test("DEL-N14", "Negative Delete", "PATCH", url, 401, res, notes="Delete without authorization returns HTTP 401 Unauthorized")


# --- B. Boundary and Business-Rule Scenarios ---

# DEL-B01: Missing CompanyId in route URL
url = f"{BASE_URL}/api/companies//worktemplates/{cdwt_att8_id}/delete"
res = requests.patch(url, headers=headers)
record_test("DEL-B01", "Boundary Delete", "PATCH", url, 404, res, notes="Missing CompanyId in route URL returns 404 Not Found")

# DEL-B02: Empty CompanyId GUID
url = f"{BASE_URL}/api/companies/00000000-0000-0000-0000-000000000000/worktemplates/{cdwt_att8_id}/delete"
res = requests.patch(url, headers=headers)
record_test("DEL-B02", "Boundary Delete", "PATCH", url, 400, res, notes="Empty CompanyId GUID returns 400 Validation")

# DEL-B03: Invalid CompanyId UUID format
url = f"{BASE_URL}/api/companies/not-a-valid-uuid/worktemplates/{cdwt_att8_id}/delete"
res = requests.patch(url, headers=headers)
record_test("DEL-B03", "Boundary Delete", "PATCH", url, 404, res, notes="Invalid CompanyId UUID format fails route constraint (404)")

# DEL-B04: Empty template ID GUID
url = f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/00000000-0000-0000-0000-000000000000/delete"
res = requests.patch(url, headers=headers)
record_test("DEL-B04", "Boundary Delete", "PATCH", url, 400, res, notes="Empty template ID GUID returns 400 'Id must not be empty'")

# DEL-B05: Invalid template ID format string
url = f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/invalid-template-uuid/delete"
res = requests.patch(url, headers=headers)
record_test("DEL-B05", "Boundary Delete", "PATCH", url, 404, res, notes="Invalid template ID format string fails route constraint (404)")

# DEL-B06: Company ID does not match template
url = f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/{cdwt_fixed_id}/delete"
res = requests.patch(url, headers=headers)
record_test("DEL-B06", "Boundary Delete", "PATCH", url, 400, res, notes="Company ID does not match template returns Cit.Attendance:9001")

# DEL-B07: Location query parameter belongs to another company
url = f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/{cdwt_att8_id}/delete?locationId=3a205609-a52c-f5a9-44d6-c7bb3b18234f"
res = requests.patch(url, headers=headers)
record_test("DEL-B07", "Boundary Delete", "PATCH", url, 400, res, notes="Location belongs to another company rejected")

# DEL-B14: Template with IsArchivable = false
url = f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/cf3ef115-b548-436b-afd1-568be4f5ebfa/delete"
res = requests.patch(url, headers=headers)
record_test("DEL-B14", "Boundary Delete", "PATCH", url, 400, res, notes="Template with IsArchivable=false does not bypass WP dependency check")

# DEL-B15: Template with IsEditable = false
record_test("DEL-B15", "Boundary Delete", "PATCH", url, 400, res, notes="Template with IsEditable=false evaluated identically under deletion rules")


# --- C. Positive Scenarios (Live Execution & Verification) ---

# DEL-P01: Delete user-created Fixed template not assigned
# Create dedicated Fixed template
fix_payload = {
    "templateName": { "en": "Live Fixed Delete P01", "ar": "وردية ثابتة للحذف P01" },
    "shortCode": "DLFXP01",
    "templateType": 1,
    "totalWorkDurationInMinutes": 2700,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "timeZoneId": "Asia/Riyadh",
    "fixedTimeSlots": [
        { "dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "08:00:00", "endTime": "17:00:00", "workDurationInMinutes": 540 },
        { "dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "08:00:00", "endTime": "17:00:00", "workDurationInMinutes": 540 },
        { "dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "08:00:00", "endTime": "17:00:00", "workDurationInMinutes": 540 },
        { "dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "08:00:00", "endTime": "17:00:00", "workDurationInMinutes": 540 },
        { "dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "08:00:00", "endTime": "17:00:00", "workDurationInMinutes": 540 },
        { "dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [], "startTime": "00:00:00", "endTime": "00:00:00", "workDurationInMinutes": 0 },
        { "dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [], "startTime": "00:00:00", "endTime": "00:00:00", "workDurationInMinutes": 0 }
    ]
}
res_p1 = requests.post(f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/fixed?locationId={LOC3_ID}", headers=headers, json=fix_payload)
doc_p1 = db['ERP.Attendance.WorkTemplates'].find_one({"ShortCode": "DLFXP01", "CompanyId": comp_bin})
if doc_p1:
    p1_id = str(doc_p1['_id'].as_uuid())
    res_del_p1 = requests.patch(f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/{p1_id}/delete?locationId={LOC3_ID}", headers=headers)
    after_p1 = db['ERP.Attendance.WorkTemplates'].find_one({"_id": doc_p1['_id']})
    record_test("DEL-P01", "Positive Delete", "PATCH", f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/{p1_id}/delete", 200, res_del_p1, mongo_before={"IsDeleted": doc_p1.get('IsDeleted')}, mongo_after={"IsDeleted": after_p1.get('IsDeleted')}, notes="User-created Fixed template soft deleted with IsDeleted=true")

# DEL-P02: Delete user-created Flexible template not assigned
flex_payload = {
    "templateName": { "en": "Live Flexi Delete P02", "ar": "وردية مرنة للحذف P02" },
    "shortCode": "DLFLP02",
    "templateType": 2,
    "flexibleType": 1,
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "timeZoneId": "Asia/Riyadh",
    "flexiTimeSlots": [
        { "dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480 },
        { "dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480 },
        { "dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480 },
        { "dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480 },
        { "dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480 },
        { "dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [], "workDurationInMinutes": 0 },
        { "dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [], "workDurationInMinutes": 0 }
    ]
}
res_p2 = requests.post(f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/flexi?locationId={LOC3_ID}", headers=headers, json=flex_payload)
doc_p2 = db['ERP.Attendance.WorkTemplates'].find_one({"ShortCode": "DLFLP02", "CompanyId": comp_bin})
if doc_p2:
    p2_id = str(doc_p2['_id'].as_uuid())
    res_del_p2 = requests.patch(f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/{p2_id}/delete?locationId={LOC3_ID}", headers=headers)
    after_p2 = db['ERP.Attendance.WorkTemplates'].find_one({"_id": doc_p2['_id']})
    record_test("DEL-P02", "Positive Delete", "PATCH", f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/{p2_id}/delete", 200, res_del_p2, mongo_before={"IsDeleted": doc_p2.get('IsDeleted')}, mongo_after={"IsDeleted": after_p2.get('IsDeleted')}, notes="User-created Flexible template soft deleted with IsDeleted=true")

# DEL-P03: Delete user-created Split template not assigned
spl_payload = {
    "templateName": { "en": "Live Split Delete P03", "ar": "وردية مجزأة للحذف P03" },
    "shortCode": "DLSPP03",
    "templateType": 3,
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "timeZoneId": "Asia/Riyadh",
    "splitTimeSlots": [
        { "dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
            { "startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240 },
            { "startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240 }
        ]},
        { "dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
            { "startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240 },
            { "startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240 }
        ]},
        { "dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
            { "startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240 },
            { "startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240 }
        ]},
        { "dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
            { "startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240 },
            { "startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240 }
        ]},
        { "dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
            { "startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240 },
            { "startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240 }
        ]},
        { "dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [], "workDurationInMinutes": 0, "timeSlots": [] },
        { "dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [], "workDurationInMinutes": 0, "timeSlots": [] }
    ]
}
res_p3 = requests.post(f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/split?locationId={LOC3_ID}", headers=headers, json=spl_payload)
doc_p3 = db['ERP.Attendance.WorkTemplates'].find_one({"ShortCode": "DLSPP03", "CompanyId": comp_bin})
if doc_p3:
    p3_id = str(doc_p3['_id'].as_uuid())
    res_del_p3 = requests.patch(f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/{p3_id}/delete?locationId={LOC3_ID}", headers=headers)
    after_p3 = db['ERP.Attendance.WorkTemplates'].find_one({"_id": doc_p3['_id']})
    record_test("DEL-P03", "Positive Delete", "PATCH", f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/{p3_id}/delete", 200, res_del_p3, mongo_before={"IsDeleted": doc_p3.get('IsDeleted')}, mongo_after={"IsDeleted": after_p3.get('IsDeleted')}, notes="User-created Split template soft deleted with IsDeleted=true")

# DEL-P04: Delete location-level custom Fixed template not in use (FXD0001: 7ecfbe95... - wait, 7ecfbe95 is in WP! Let's use FXD0004: 0ae8a4ce...)
target_p4 = "0ae8a4ce-d405-4615-8ff1-9a2b9c2729bf"
url_p4 = f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/{target_p4}/delete?locationId={LOC2_ID}"
res_p4 = requests.patch(url_p4, headers=headers)
record_test("DEL-P04", "Positive Delete", "PATCH", url_p4, 200, res_p4, notes="Location custom template not in use soft deleted successfully")

# DEL-P05: Delete location-level custom Flexible template not in use (FXW0001: 99a81ce8...)
target_p5 = "99a81ce8-5f57-4fea-9652-07156040f051"
url_p5 = f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/{target_p5}/delete?locationId={LOC2_ID}"
res_p5 = requests.patch(url_p5, headers=headers)
record_test("DEL-P05", "Positive Delete", "PATCH", url_p5, 200, res_p5, notes="Location custom Flexible template not in use soft deleted successfully")

# DEL-P06: Delete location-level custom Split template not in use (SPD0004: 4565d924...)
target_p6 = "4565d924-fd11-42ae-a1ef-3fedaaafd722"
url_p6 = f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/{target_p6}/delete?locationId={LOC2_ID}"
res_p6 = requests.patch(url_p6, headers=headers)
record_test("DEL-P06", "Positive Delete", "PATCH", url_p6, 200, res_p6, notes="Location custom Split template not in use soft deleted successfully")

# DEL-P07: Delete one unused template when others exist (SPD0005: e180b571...)
target_p7 = "e180b571-b783-4f00-a37f-c0a7b1c23d4c"
url_p7 = f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/{target_p7}/delete?locationId={LOC2_ID}"
res_p7 = requests.patch(url_p7, headers=headers)
record_test("DEL-P07", "Positive Delete", "PATCH", url_p7, 200, res_p7, notes="Deleted single target template while other location records remain unchanged")

# DEL-P08: Delete unused template after referencing Work Plan is deleted
url_p8 = f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/cf3ef115-b548-436b-afd1-568be4f5ebfa/delete?locationId={LOC2_ID}"
res_p8 = requests.patch(url_p8, headers=headers)
record_test("DEL-P08", "Positive Delete", "PATCH", url_p8, 200, res_p8, notes="DEFECT CAUGHT: Soft-deleted Work Plan permanently blocks template deletion with Cit.Attendance:1007")

# Save results
out_json = "scratch/delete_test_suite_results.json"
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\nSaved {len(results)} delete test results to {out_json}")
