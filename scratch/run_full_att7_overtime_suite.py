import urllib.request
import urllib.error
import json
import ssl
import sys
import uuid
import pymongo
import time

sys.stdout.reconfigure(encoding='utf-8')

company_id = "3a249870-c8ae-b3dc-1b8d-c44efad14f89"
base_url = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/attpolicies"

with open("scratch/current_token.json", "r") as f:
    token = json.load(f)["access_token"]

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

mongo_client = pymongo.MongoClient('mongodb://10.1.0.4:27018/', uuidRepresentation='standard', serverSelectionTimeoutMS=5000)
mongo_col = mongo_client['Sahab']['ERP.Attendance.Policies']

def call_api(method, endpoint, payload=None):
    url = f"{base_url}{endpoint}" if endpoint.startswith("/") else f"{base_url}/{endpoint}"
    data = json.dumps(payload).encode('utf-8') if payload is not None else None
    headers = {
        'Authorization': f'Bearer {token}',
        '__tenant': 'Attendance',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            body = resp.read().decode('utf-8')
            try:
                parsed = json.loads(body)
            except:
                parsed = body
            return resp.status, parsed
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8')
        try:
            parsed = json.loads(err_body)
        except:
            parsed = err_body
        return e.code, parsed
    except Exception as e:
        return 999, str(e)

results = []

def run_test(tc_id, name, method, endpoint, payload, expected_status):
    status, body = call_api(method, endpoint, payload)
    passed = (status == expected_status) or (expected_status == 400 and status in [400, 422]) or (expected_status == 200 and status in [200, 201])
    # check for specific defects
    is_defect = False
    defect_ref = ""
    if tc_id == "POST-N13" and status == 200:
        is_defect = True
        defect_ref = "DEFECT-20261105-03 (Negative rateFormula accepted)"
        passed = False
    elif tc_id == "POST-N08" and status == 500:
        is_defect = True
        defect_ref = "Integer overflow causes unhandled HTTP 500"
        passed = False
    
    res = {
        "tc_id": tc_id,
        "name": name,
        "method": method,
        "endpoint": endpoint,
        "payload": payload,
        "expected_status": expected_status,
        "actual_status": status,
        "actual_body": body,
        "passed": passed,
        "is_defect": is_defect,
        "defect_ref": defect_ref
    }
    results.append(res)
    print(f"[{'PASS' if passed else 'FAIL'}] {tc_id:<10} | HTTP {status} (exp {expected_status}) | {name}")
    if not passed:
        print(f"       -> Resp: {str(body)[:150]}")
    return status, body

print("================================================================================")
print("1. RUNNING POSITIVE POST SUITE (POST-P01 to POST-P12)")
print("================================================================================")

p_tests = [
    ("POST-P01", "Standard policy", {
        "type": "Overtime", "name": {"en": "Standard Overtime Policy", "ar": "سياسة العمل الإضافي القياسية"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }),
    ("POST-P02", "Inactive policy", {
        "type": "Overtime", "name": {"en": "Inactive Overtime Policy", "ar": "سياسة العمل الإضافي غير النشطة"},
        "isActive": False, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }),
    ("POST-P03", "Buffer disabled", {
        "type": "Overtime", "name": {"en": "No Buffer Policy", "ar": "سياسة بدون فترة سماح"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": False, "bufferMinutes": 0,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }),
    ("POST-P04", "Minimum positive buffer", {
        "type": "Overtime", "name": {"en": "Minimum Buffer Policy", "ar": "سياسة الحد الأدنى لفترة السماح"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 1,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }),
    ("POST-P05", "Maximum buffer candidate (1440m)", {
        "type": "Overtime", "name": {"en": "Maximum Buffer Policy", "ar": "سياسة الحد الأقصى لفترة السماح"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 1440,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }),
    ("POST-P06", "Multiple rates (1.5, 2.0, 2.5)", {
        "type": "Overtime", "name": {"en": "Multiple Rates Policy", "ar": "سياسة معدلات متعددة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 2.0}, {"dayRate": 3, "rateFormula": 2.5}]
    }),
    ("POST-P07", "Before shift starts rule (2)", {
        "type": "Overtime", "name": {"en": "Before Shift Overtime Policy", "ar": "سياسة العمل الإضافي قبل الوردية"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 2,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }),
    ("POST-P08", "After shift ends rule (3)", {
        "type": "Overtime", "name": {"en": "After Shift Overtime Policy", "ar": "سياسة العمل الإضافي بعد الوردية"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 3,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }),
    ("POST-P09", "English-only policy name", {
        "type": "Overtime", "name": {"en": "English Only Overtime Policy"},
        "isActive": True, "tenantName": {"en": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }),
    ("POST-P10", "Arabic-only policy name", {
        "type": "Overtime", "name": {"ar": "سياسة العمل الإضافي باللغة العربية"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }),
    ("POST-P11", "Zero rate formula (0)", {
        "type": "Overtime", "name": {"en": "Zero Rate Formula Policy", "ar": "سياسة بمعادلة معدل صفر"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": False, "bufferMinutes": 0,
        "rates": [{"dayRate": 1, "rateFormula": 0}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 2.0}]
    }),
    ("POST-P12", "NotApplicable enum values (0)", {
        "type": "Overtime", "name": {"en": "Not Applicable Overtime Policy", "ar": "سياسة عمل إضافي غير قابلة للتطبيق"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 0,
        "hasBufferBeforeOvertime": False, "bufferMinutes": 0,
        "rates": [{"dayRate": 0, "rateFormula": 0}]
    })
]

active_policy_id = None
for tc_id, name, payload in p_tests:
    st, resp = run_test(tc_id, name, "POST", "/overtime", payload, 200)
    if st == 200 and not active_policy_id:
        if isinstance(resp, dict) and "id" in resp:
            active_policy_id = resp["id"]
        elif isinstance(resp, dict) and "policy" in resp and "id" in resp["policy"]:
            active_policy_id = resp["policy"]["id"]

print(f"\nTarget Active Policy ID for PATCH tests: {active_policy_id}\n")

print("================================================================================")
print("2. RUNNING NEGATIVE POST SUITE (POST-N01 to POST-N17)")
print("================================================================================")

n_tests = [
    ("POST-N01", "Empty body", {}, 400),
    ("POST-N02", "Invalid policy type", {
        "type": "InvalidPolicy", "name": {"en": "Invalid Type Policy", "ar": "سياسة بنوع غير صالح"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }, 400),
    ("POST-N03", "Null policy name", {
        "type": "Overtime", "name": None, "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "overtimeRule": 1, "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }, 400),
    ("POST-N04", "Empty English name", {
        "type": "Overtime", "name": {"en": "", "ar": "سياسة العمل الإضافي"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }, 400),
    ("POST-N05", "Null tenant name", {
        "type": "Overtime", "name": {"en": "Null Tenant Name Policy", "ar": "سياسة باسم مستأجر فارغ"},
        "isActive": True, "tenantName": None, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }, 400),
    ("POST-N06", "Invalid overtimeRule (999)", {
        "type": "Overtime", "name": {"en": "Invalid Rule Policy", "ar": "سياسة بقاعدة غير صالحة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 999,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }, 400),
    ("POST-N07", "Negative buffer (-1)", {
        "type": "Overtime", "name": {"en": "Negative Buffer Policy", "ar": "سياسة بفترة سماح سالبة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": -1,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }, 400),
    ("POST-N08", "Buffer overflow (2147483648)", {
        "type": "Overtime", "name": {"en": "Excessive Buffer Policy", "ar": "سياسة بفترة سماح كبيرة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 2147483648,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }, 400),
    ("POST-N09", "Buffer disabled with nonzero minutes (30m)", {
        "type": "Overtime", "name": {"en": "Disabled Buffer Nonzero Policy", "ar": "سياسة بفترة سماح معطلة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": False, "bufferMinutes": 30,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }, 400),
    ("POST-N10", "Null rates array", {
        "type": "Overtime", "name": {"en": "Null Rates Policy", "ar": "سياسة بمعدلات فارغة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": None
    }, 400),
    ("POST-N11", "Empty rates array []", {
        "type": "Overtime", "name": {"en": "Empty Rates Policy", "ar": "سياسة بدون معدلات"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": []
    }, 400),
    ("POST-N12", "Invalid dayRate (999)", {
        "type": "Overtime", "name": {"en": "Invalid Day Rate Policy", "ar": "سياسة بمعدل يوم غير صالح"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 999, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }, 400),
    ("POST-N13", "Negative rate formula (-1)", {
        "type": "Overtime", "name": {"en": "Negative Rate Formula Policy", "ar": "سياسة بمعادلة معدل سالبة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": -1}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }, 400),
    ("POST-N14", "Duplicate dayRate (dayRate 1 twice)", {
        "type": "Overtime", "name": {"en": "Duplicate Day Rate Policy", "ar": "سياسة بمعدلات أيام مكررة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 1, "rateFormula": 2.0}, {"dayRate": 3, "rateFormula": 2.5}]
    }, 400),
    ("POST-N15", "NotApplicable dayRate (0)", {
        "type": "Overtime", "name": {"en": "Not Applicable Day Rate Policy", "ar": "سياسة بمعدل يوم غير محدد"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 0, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }, 400),
    ("POST-N16", "Invalid Boolean type (string 'true')", {
        "type": "Overtime", "name": {"en": "Invalid Boolean Policy", "ar": "سياسة بقيمة منطقية غير صالحة"},
        "isActive": "true", "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }, 400),
    ("POST-N17", "Decimal buffer minutes (1.5)", {
        "type": "Overtime", "name": {"en": "Decimal Buffer Policy", "ar": "سياسة بفترة سماح عشرية"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 1.5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }, 400)
]

for tc_id, name, payload, exp_st in n_tests:
    run_test(tc_id, name, "POST", "/overtime", payload, exp_st)

print("================================================================================")
print("3. RUNNING POSITIVE PATCH SUITE (PATCH-P01 to PATCH-P12)")
print("================================================================================")

if not active_policy_id:
    active_policy_id = "00000000-0000-0000-0000-000000000000"

patch_p_tests = [
    ("PATCH-P01", "Update policy name", {
        "id": active_policy_id, "type": "Overtime", "name": {"en": "Updated Overtime Policy", "ar": "سياسة العمل الإضافي المحدثة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }),
    ("PATCH-P02", "Deactivate policy (isActive: false)", {
        "id": active_policy_id, "type": "Overtime", "name": {"en": "Inactive Overtime Policy", "ar": "سياسة العمل الإضافي غير النشطة"},
        "isActive": False, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }),
    ("PATCH-P03", "Change overtime rule to BeforeShiftStarts (2)", {
        "id": active_policy_id, "type": "Overtime", "name": {"en": "Before Shift Policy", "ar": "سياسة قبل بداية الوردية"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 2,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }),
    ("PATCH-P04", "Change overtime rule to AfterShiftEnds (3)", {
        "id": active_policy_id, "type": "Overtime", "name": {"en": "After Shift Policy", "ar": "سياسة بعد نهاية الوردية"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 3,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }),
    ("PATCH-P05", "Disable buffer (hasBuffer: false, bufferMinutes: 0)", {
        "id": active_policy_id, "type": "Overtime", "name": {"en": "No Buffer Updated Policy", "ar": "سياسة محدثة بدون فترة سماح"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": False, "bufferMinutes": 0,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }),
    ("PATCH-P06", "Update buffer minutes (30m)", {
        "id": active_policy_id, "type": "Overtime", "name": {"en": "Updated Buffer Policy", "ar": "سياسة فترة السماح المحدثة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 30,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }),
    ("PATCH-P07", "Update WorkingDay rate formula (1.75)", {
        "id": active_policy_id, "type": "Overtime", "name": {"en": "Updated Working Day Rate", "ar": "تحديث معدل يوم العمل"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.75}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 2.5}]
    }),
    ("PATCH-P08", "Update DayOff rate formula (2.0)", {
        "id": active_policy_id, "type": "Overtime", "name": {"en": "Updated Day Off Rate", "ar": "تحديث معدل يوم الإجازة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 2.0}, {"dayRate": 3, "rateFormula": 2.5}]
    }),
    ("PATCH-P09", "Update Holiday rate formula (3.0)", {
        "id": active_policy_id, "type": "Overtime", "name": {"en": "Updated Holiday Rate", "ar": "تحديث معدل العطلات"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 2.0}, {"dayRate": 3, "rateFormula": 3.0}]
    }),
    ("PATCH-P10", "Update all three rate formulas (1.25, 1.75, 2.25)", {
        "id": active_policy_id, "type": "Overtime", "name": {"en": "All Rates Updated", "ar": "تحديث جميع معدلات العمل الإضافي"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 15,
        "rates": [{"dayRate": 1, "rateFormula": 1.25}, {"dayRate": 2, "rateFormula": 1.75}, {"dayRate": 3, "rateFormula": 2.25}]
    }),
    ("PATCH-P11", "Update policy with multiple rates", {
        "id": active_policy_id, "type": "Overtime", "name": {"en": "Multiple Rates Updated", "ar": "سياسة محدثة بمعدلات متعددة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 2,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 10,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 2.0}, {"dayRate": 3, "rateFormula": 2.5}]
    }),
    ("PATCH-P12", "Update with zero buffer and zero formula", {
        "id": active_policy_id, "type": "Overtime", "name": {"en": "Zero Boundary Updated Policy", "ar": "سياسة محدثة بحدود صفرية"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": False, "bufferMinutes": 0,
        "rates": [{"dayRate": 1, "rateFormula": 0}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 2.0}]
    })
]

for tc_id, name, payload in patch_p_tests:
    run_test(tc_id, name, "PATCH", f"/overtime/{active_policy_id}", payload, 200)

print("================================================================================")
print("4. RUNNING NEGATIVE PATCH SUITE (PATCH-N01 to PATCH-N12)")
print("================================================================================")

patch_n_tests = [
    ("PATCH-N01", "Null policy name", {
        "id": active_policy_id, "type": "Overtime", "name": None, "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "overtimeRule": 1, "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }, f"/overtime/{active_policy_id}", 400),
    ("PATCH-N02", "Invalid policy type", {
        "id": active_policy_id, "type": "InvalidPolicy", "name": {"en": "Invalid Type Update", "ar": "تحديث بنوع غير صالح"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }, f"/overtime/{active_policy_id}", 400),
    ("PATCH-N03", "Invalid overtime rule (999)", {
        "id": active_policy_id, "type": "Overtime", "name": {"en": "Invalid Rule Update", "ar": "تحديث بقاعدة غير صالحة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 999,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }, f"/overtime/{active_policy_id}", 400),
    ("PATCH-N04", "Negative buffer (-1)", {
        "id": active_policy_id, "type": "Overtime", "name": {"en": "Negative Buffer Update", "ar": "تحديث بفترة سماح سالبة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": -1,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }, f"/overtime/{active_policy_id}", 400),
    ("PATCH-N05", "Buffer disabled with nonzero minutes (30m)", {
        "id": active_policy_id, "type": "Overtime", "name": {"en": "Invalid Buffer Combination", "ar": "تركيبة فترة سماح غير صالحة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": False, "bufferMinutes": 30,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }, f"/overtime/{active_policy_id}", 400),
    ("PATCH-N06", "Null rates array", {
        "id": active_policy_id, "type": "Overtime", "name": {"en": "Null Rates Update", "ar": "تحديث بمعدلات فارغة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5, "rates": None
    }, f"/overtime/{active_policy_id}", 400),
    ("PATCH-N07", "Empty rates array []", {
        "id": active_policy_id, "type": "Overtime", "name": {"en": "Empty Rates Update", "ar": "تحديث بدون معدلات"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5, "rates": []
    }, f"/overtime/{active_policy_id}", 400),
    ("PATCH-N08", "Invalid dayRate (999)", {
        "id": active_policy_id, "type": "Overtime", "name": {"en": "Invalid Day Rate Update", "ar": "تحديث بمعدل يوم غير صالح"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 999, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }, f"/overtime/{active_policy_id}", 400),
    ("PATCH-N09", "Negative rate formula (-1)", {
        "id": active_policy_id, "type": "Overtime", "name": {"en": "Negative Rate Update", "ar": "تحديث بمعدل سالب"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": -1}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }, f"/overtime/{active_policy_id}", 400),
    ("PATCH-N10", "Duplicate dayRate (dayRate 1 twice)", {
        "id": active_policy_id, "type": "Overtime", "name": {"en": "Duplicate Day Rate Update", "ar": "تحديث بمعدلات أيام مكررة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 1, "rateFormula": 2.0}, {"dayRate": 3, "rateFormula": 2.5}]
    }, f"/overtime/{active_policy_id}", 400),
    ("PATCH-N11", "Body ID differs from URL ID", {
        "id": "11111111-1111-1111-1111-111111111111", "type": "Overtime", "name": {"en": "Mismatched ID Update", "ar": "تحديث بمعرف غير متطابق"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }, f"/overtime/{active_policy_id}", 400),
    ("PATCH-N12", "Non-existing policy ID in URL & body", {
        "id": "11111111-1111-1111-1111-111111111111", "type": "Overtime", "name": {"en": "Non Existing Policy", "ar": "سياسة غير موجودة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1,
        "hasBufferBeforeOvertime": True, "bufferMinutes": 5,
        "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]
    }, "/overtime/11111111-1111-1111-1111-111111111111", 400)
]

for tc_id, name, payload, endpoint, exp_st in patch_n_tests:
    run_test(tc_id, name, "PATCH", endpoint, payload, exp_st)

print("================================================================================")
print("5. VERIFYING IN MONGODB COMPASS (Sahab.ERP.Attendance.Policies)")
print("================================================================================")

docs = list(mongo_col.find({"CompanyId": uuid.UUID(company_id), "Type": 2}))
print(f"Total Overtime Policies in MongoDB for Attendance 7: {len(docs)}")
for i, d in enumerate(docs[:5], 1):
    print(f"Doc {i}: ID={d.get('_id')} | Name={d.get('Name')} | OvertimeRule={d.get('OvertimeRule')} | Rates={len(d.get('Rates', []))} | IsActive={d.get('IsActive')}")

# Save results JSON
with open("scratch/att7_overtime_suite_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, default=str)

print("\n=== COMPLETED LIVE OVERTIME TEST SUITE ON ATTENDANCE 7 ===")
