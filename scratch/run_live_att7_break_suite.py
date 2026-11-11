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
    
    is_defect = False
    defect_ref = ""
    # Detect critical gaps:
    if expected_status == 400 and status == 200:
        is_defect = True
        defect_ref = f"CRITICAL GAP: Negative test {tc_id} accepted with HTTP 200 OK!"
        passed = False
    elif status == 500:
        is_defect = True
        defect_ref = f"SERVER CRASH: Unhandled HTTP 500 on {tc_id}!"
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
    print(f"[{'PASS' if passed else 'FAIL'}] {tc_id:<12} | HTTP {status} (exp {expected_status}) | {name}")
    if not passed:
        print(f"       -> Resp: {str(body)[:150]}")
    return status, body

print("================================================================================")
print("1. RUNNING POSITIVE POST BREAK SUITE (P01 to P10)")
print("================================================================================")

p_tests = [
    ("BRK-POST-P01", "Create with two break entries (baseline)", {
        "type": "Break", "name": {"en": "Standard Break Policy P01", "ar": "سياسة الاستراحة القياسية 1"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15}, {"name": "Lunch Break", "type": 1, "durationMinutes": 30}]
    }),
    ("BRK-POST-P02", "Create with one break entry", {
        "type": "Break", "name": {"en": "Single Break Policy P02", "ar": "سياسة استراحة واحدة 2"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15}]
    }),
    ("BRK-POST-P03", "Create with multiple break entries (4 breaks)", {
        "type": "Break", "name": {"en": "Multiple Break Policy P03", "ar": "سياسة استراحات متعددة 3"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [
            {"name": "Morning Break", "type": 1, "durationMinutes": 10},
            {"name": "Tea Break", "type": 1, "durationMinutes": 15},
            {"name": "Lunch Break", "type": 2, "durationMinutes": 45},
            {"name": "Evening Break", "type": 1, "durationMinutes": 10}
        ]
    }),
    ("BRK-POST-P04", "Create with minimum positive duration (1m)", {
        "type": "Break", "name": {"en": "One Minute Break Policy P04", "ar": "سياسة استراحة دقيقة واحدة 4"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Short Break", "type": 1, "durationMinutes": 1}]
    }),
    ("BRK-POST-P05", "Create with longer duration (60m)", {
        "type": "Break", "name": {"en": "Long Break Policy P05", "ar": "سياسة استراحة طويلة 5"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Lunch Break", "type": 2, "durationMinutes": 60}]
    }),
    ("BRK-POST-P06", "Create inactive policy", {
        "type": "Break", "name": {"en": "Inactive Break Policy P06", "ar": "سياسة استراحة غير نشطة 6"},
        "isActive": False, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15}]
    }),
    ("BRK-POST-P07", "Create with English-only policy name", {
        "type": "Break", "name": {"en": "English Break Policy P07"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15}]
    }),
    ("BRK-POST-P08", "Create with Arabic-only policy name", {
        "type": "Break", "name": {"ar": "سياسة الاستراحة 8"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "استراحة الشاي", "type": 1, "durationMinutes": 15}]
    }),
    ("BRK-POST-P09", "Create with different break names and same duration", {
        "type": "Break", "name": {"en": "Same Duration Break Policy P09", "ar": "سياسة استراحات بنفس المدة 9"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [
            {"name": "Tea Break", "type": 1, "durationMinutes": 15},
            {"name": "Personal Break", "type": 1, "durationMinutes": 15},
            {"name": "Prayer Break", "type": 1, "durationMinutes": 15}
        ]
    }),
    ("BRK-POST-P10", "Create with different durations (5, 20, 45)", {
        "type": "Break", "name": {"en": "Variable Duration Break Policy P10", "ar": "سياسة استراحات بمدد مختلفة 10"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [
            {"name": "Short Break", "type": 1, "durationMinutes": 5},
            {"name": "Medium Break", "type": 1, "durationMinutes": 20},
            {"name": "Long Break", "type": 2, "durationMinutes": 45}
        ]
    })
]

active_break_id = None
for tc_id, name, payload in p_tests:
    st, resp = run_test(tc_id, name, "POST", "/break", payload, 200)
    if st == 200 and not active_break_id:
        if isinstance(resp, dict) and "id" in resp:
            active_break_id = resp["id"]
        elif isinstance(resp, dict) and "policy" in resp and "id" in resp["policy"]:
            active_break_id = resp["policy"]["id"]

print(f"\nTarget Active Break Policy ID for PATCH tests: {active_break_id}\n")

print("================================================================================")
print("2. RUNNING NEGATIVE POST BREAK SUITE (N01 to N20)")
print("================================================================================")

n_tests = [
    ("BRK-POST-N01", "Empty request body", {}, 400),
    ("BRK-POST-N02", "Invalid policy type", {
        "type": "InvalidBreak", "name": {"en": "Invalid Type Policy", "ar": "سياسة نوع غير صالح"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15}]
    }, 400),
    ("BRK-POST-N03", "Null policy name", {
        "type": "Break", "name": None, "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15}]
    }, 400),
    ("BRK-POST-N04", "Empty English policy name", {
        "type": "Break", "name": {"en": "", "ar": "سياسة الاستراحة"}, "isActive": True,
        "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15}]
    }, 400),
    ("BRK-POST-N05", "Null tenant name", {
        "type": "Break", "name": {"en": "Null Tenant Policy", "ar": "سياسة بدون مستأجر"}, "isActive": True,
        "tenantName": None, "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15}]
    }, 400),
    ("BRK-POST-N06", "Missing type property", {
        "name": {"en": "Missing Type Policy", "ar": "سياسة بدون نوع"}, "isActive": True,
        "tenantName": {"en": "Attendance", "ar": "Attendance"}, "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15}]
    }, 400),
    ("BRK-POST-N07", "Missing breaks property", {
        "type": "Break", "name": {"en": "Missing Breaks Policy", "ar": "سياسة بدون استراحات"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}
    }, 400),
    ("BRK-POST-N08", "Null breaks", {
        "type": "Break", "name": {"en": "Null Breaks Policy", "ar": "سياسة استراحات فارغة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "breaks": None
    }, 400),
    ("BRK-POST-N09", "Empty breaks array []", {
        "type": "Break", "name": {"en": "Empty Breaks Policy", "ar": "سياسة بدون عناصر استراحة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "breaks": []
    }, 400),
    ("BRK-POST-N10", "Null break item in array", {
        "type": "Break", "name": {"en": "Null Break Item Policy", "ar": "سياسة عنصر استراحة فارغ"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "breaks": [None]
    }, 400),
    ("BRK-POST-N11", "Missing break name", {
        "type": "Break", "name": {"en": "Missing Break Name Policy", "ar": "سياسة بدون اسم استراحة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "breaks": [{"type": 1, "durationMinutes": 15}]
    }, 400),
    ("BRK-POST-N12", "Empty break name", {
        "type": "Break", "name": {"en": "Empty Break Name Policy", "ar": "سياسة اسم استراحة فارغ"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "breaks": [{"name": "", "type": 1, "durationMinutes": 15}]
    }, 400),
    ("BRK-POST-N13", "Invalid break type (999)", {
        "type": "Break", "name": {"en": "Invalid Break Type Policy", "ar": "سياسة نوع استراحة غير صالح"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "breaks": [{"name": "Tea Break", "type": 999, "durationMinutes": 15}]
    }, 400),
    ("BRK-POST-N14", "Negative duration (-1)", {
        "type": "Break", "name": {"en": "Negative Duration Policy", "ar": "سياسة مدة سالبة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": -1}]
    }, 400),
    ("BRK-POST-N15", "Zero duration (0)", {
        "type": "Break", "name": {"en": "Zero Duration Policy", "ar": "سياسة مدة صفرية"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 0}]
    }, 400),
    ("BRK-POST-N16", "Decimal duration (15.5)", {
        "type": "Break", "name": {"en": "Decimal Duration Policy", "ar": "سياسة مدة عشرية"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15.5}]
    }, 400),
    ("BRK-POST-N17", "String duration ('15')", {
        "type": "Break", "name": {"en": "String Duration Policy", "ar": "سياسة مدة نصية"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": "15"}]
    }, 400),
    ("BRK-POST-N18", "String break type ('1')", {
        "type": "Break", "name": {"en": "String Break Type Policy", "ar": "سياسة نوع استراحة نصي"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "breaks": [{"name": "Tea Break", "type": "1", "durationMinutes": 15}]
    }, 400),
    ("BRK-POST-N19", "String isActive ('true')", {
        "type": "Break", "name": {"en": "Invalid Active Policy", "ar": "سياسة حالة غير صالحة"},
        "isActive": "true", "tenantName": {"en": "Attendance", "ar": "Attendance"}, "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15}]
    }, 400),
    ("BRK-POST-N20", "Duplicate break entries in array", {
        "type": "Break", "name": {"en": "Duplicate Break Entries Policy", "ar": "سياسة عناصر استراحة مكررة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15}, {"name": "Tea Break", "type": 1, "durationMinutes": 15}]
    }, 400)
]

for tc_id, name, payload, exp_st in n_tests:
    run_test(tc_id, name, "POST", "/break", payload, exp_st)

print("================================================================================")
print("3. RUNNING POSITIVE PATCH BREAK SUITE (P01 to P12)")
print("================================================================================")

if not active_break_id:
    active_break_id = "b48d4da6-36ca-4731-b6e2-d52e761841da"

patch_p_tests = [
    ("BRK-PATCH-P01", "Update policy name", {
        "type": "Break", "name": {"en": "Updated Standard Break Policy", "ar": "سياسة الاستراحة القياسية المحدثة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15}, {"name": "Lunch Break", "type": 1, "durationMinutes": 30}]
    }),
    ("BRK-PATCH-P02", "Deactivate policy (isActive: false)", {
        "type": "Break", "name": {"en": "Deactivated Break Policy", "ar": "سياسة استراحة غير نشطة"},
        "isActive": False, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15}, {"name": "Lunch Break", "type": 1, "durationMinutes": 30}]
    }),
    ("BRK-PATCH-P03", "Activate an inactive policy (isActive: true)", {
        "type": "Break", "name": {"en": "Activated Break Policy", "ar": "سياسة استراحة نشطة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15}, {"name": "Lunch Break", "type": 1, "durationMinutes": 30}]
    }),
    ("BRK-PATCH-P04", "Update one break duration (20m)", {
        "type": "Break", "name": {"en": "Updated Break Duration Policy", "ar": "سياسة مدة استراحة محدثة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 20}, {"name": "Lunch Break", "type": 1, "durationMinutes": 30}]
    }),
    ("BRK-PATCH-P05", "Update all break durations (10, 45, 10)", {
        "type": "Break", "name": {"en": "All Durations Updated Policy", "ar": "سياسة تحديث جميع مدد الاستراحة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [
            {"name": "Morning Break", "type": 1, "durationMinutes": 10},
            {"name": "Lunch Break", "type": 2, "durationMinutes": 45},
            {"name": "Evening Break", "type": 1, "durationMinutes": 10}
        ]
    }),
    ("BRK-PATCH-P06", "Add a new break entry (3 breaks)", {
        "type": "Break", "name": {"en": "Break Policy With New Entry", "ar": "سياسة استراحة مع عنصر جديد"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [
            {"name": "Tea Break", "type": 1, "durationMinutes": 15},
            {"name": "Lunch Break", "type": 2, "durationMinutes": 30},
            {"name": "Evening Break", "type": 1, "durationMinutes": 10}
        ]
    }),
    ("BRK-PATCH-P07", "Remove an existing break entry (1 break)", {
        "type": "Break", "name": {"en": "Break Policy With Removed Entry", "ar": "سياسة استراحة بعد حذف عنصر"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15}]
    }),
    ("BRK-PATCH-P08", "Change break names", {
        "type": "Break", "name": {"en": "Renamed Break Policy", "ar": "سياسة استراحة بأسماء محدثة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [
            {"name": "Morning Tea Break", "type": 1, "durationMinutes": 15},
            {"name": "Afternoon Lunch Break", "type": 2, "durationMinutes": 30}
        ]
    }),
    ("BRK-PATCH-P09", "Update to minimum positive duration (1m)", {
        "type": "Break", "name": {"en": "Minimum Duration Updated Policy", "ar": "سياسة مدة استراحة دنيا محدثة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Short Break", "type": 1, "durationMinutes": 1}]
    }),
    ("BRK-PATCH-P10", "Update to longer duration (120m)", {
        "type": "Break", "name": {"en": "Long Duration Updated Policy", "ar": "سياسة مدة استراحة طويلة محدثة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Lunch Break", "type": 2, "durationMinutes": 120}]
    }),
    ("BRK-PATCH-P11", "Update with multiple break entries (5 breaks)", {
        "type": "Break", "name": {"en": "Multiple Breaks Updated Policy", "ar": "سياسة استراحات متعددة محدثة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [
            {"name": "Morning Break", "type": 1, "durationMinutes": 10},
            {"name": "Tea Break", "type": 1, "durationMinutes": 15},
            {"name": "Lunch Break", "type": 2, "durationMinutes": 45},
            {"name": "Evening Break", "type": 1, "durationMinutes": 10},
            {"name": "Personal Break", "type": 1, "durationMinutes": 5}
        ]
    }),
    ("BRK-PATCH-P12", "Update policy with an empty breaks array []", {
        "type": "Break", "name": {"en": "Empty Breaks Updated Policy", "ar": "سياسة محدثة بدون استراحات"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "breaks": []
    })
]

for tc_id, name, payload in patch_p_tests:
    run_test(tc_id, name, "PATCH", f"/break/{active_break_id}", payload, 200)

print("================================================================================")
print("4. RUNNING NEGATIVE PATCH BREAK SUITE (N01 to N17)")
print("================================================================================")

patch_n_tests = [
    ("BRK-PATCH-N01", "Null policy name", {
        "type": "Break", "name": None, "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15}]
    }, f"/break/{active_break_id}", 400),
    ("BRK-PATCH-N02", "Invalid policy type", {
        "type": "InvalidBreak", "name": {"en": "Invalid Policy Type", "ar": "نوع سياسة غير صالح"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15}]
    }, f"/break/{active_break_id}", 400),
    ("BRK-PATCH-N03", "Null breaks", {
        "type": "Break", "name": {"en": "Null Breaks Update", "ar": "تحديث استراحات فارغة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "breaks": None
    }, f"/break/{active_break_id}", 400),
    ("BRK-PATCH-N04", "Missing breaks property", {
        "type": "Break", "name": {"en": "Missing Breaks Update", "ar": "تحديث بدون استراحات"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}
    }, f"/break/{active_break_id}", 400),
    ("BRK-PATCH-N05", "Invalid break type (999)", {
        "type": "Break", "name": {"en": "Invalid Break Type Update", "ar": "تحديث نوع استراحة غير صالح"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Tea Break", "type": 999, "durationMinutes": 15}]
    }, f"/break/{active_break_id}", 400),
    ("BRK-PATCH-N06", "Negative duration (-5)", {
        "type": "Break", "name": {"en": "Negative Duration Update", "ar": "تحديث مدة سالبة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": -5}]
    }, f"/break/{active_break_id}", 400),
    ("BRK-PATCH-N07", "Zero duration (0)", {
        "type": "Break", "name": {"en": "Zero Duration Update", "ar": "تحديث مدة صفرية"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 0}]
    }, f"/break/{active_break_id}", 400),
    ("BRK-PATCH-N08", "Decimal duration (15.5)", {
        "type": "Break", "name": {"en": "Decimal Duration Update", "ar": "تحديث مدة عشرية"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15.5}]
    }, f"/break/{active_break_id}", 400),
    ("BRK-PATCH-N09", "Empty break name", {
        "type": "Break", "name": {"en": "Empty Break Name Update", "ar": "تحديث اسم استراحة فارغ"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "", "type": 1, "durationMinutes": 15}]
    }, f"/break/{active_break_id}", 400),
    ("BRK-PATCH-N10", "Null break item", {
        "type": "Break", "name": {"en": "Null Break Item Update", "ar": "تحديث عنصر استراحة فارغ"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "breaks": [None]
    }, f"/break/{active_break_id}", 400),
    ("BRK-PATCH-N11", "String duration ('15')", {
        "type": "Break", "name": {"en": "String Duration Update", "ar": "تحديث مدة نصية"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": "15"}]
    }, f"/break/{active_break_id}", 400),
    ("BRK-PATCH-N12", "String break type ('1')", {
        "type": "Break", "name": {"en": "String Break Type Update", "ar": "تحديث نوع استراحة نصي"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Tea Break", "type": "1", "durationMinutes": 15}]
    }, f"/break/{active_break_id}", 400),
    ("BRK-PATCH-N13", "Wrong data type for breaks (string)", {
        "type": "Break", "name": {"en": "Wrong Breaks Data Type", "ar": "نوع بيانات الاستراحات غير صحيح"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "breaks": "Tea Break"
    }, f"/break/{active_break_id}", 400),
    ("BRK-PATCH-N14", "Mismatched company policy ID", {
        "type": "Break", "name": {"en": "Company Mismatch Policy", "ar": "سياسة شركة مختلفة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15}]
    }, f"/break/d533d491-02b1-4096-a072-170ac5d027f9", 400),
    ("BRK-PATCH-N15", "Non-existing policy ID", {
        "type": "Break", "name": {"en": "Non Existing Policy Update", "ar": "تحديث سياسة غير موجودة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15}]
    }, "/break/11111111-2222-3333-4444-555555555555", 400),
    ("BRK-PATCH-N16", "Invalid policy ID format", {
        "type": "Break", "name": {"en": "Invalid ID Format Update"}, "isActive": True,
        "tenantName": {"en": "Attendance"}, "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15}]
    }, "/break/invalid-policy-id", 400),
    ("BRK-PATCH-N17", "Duplicate break entries in PATCH", {
        "type": "Break", "name": {"en": "Duplicate Break Update", "ar": "تحديث استراحات مكررة"},
        "isActive": True, "tenantName": {"en": "Attendance", "ar": "Attendance"},
        "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15}, {"name": "Tea Break", "type": 1, "durationMinutes": 15}]
    }, f"/break/{active_break_id}", 400)
]

for tc_id, name, payload, endpoint, exp_st in patch_n_tests:
    run_test(tc_id, name, "PATCH", endpoint, payload, exp_st)

print("================================================================================")
print("5. RUNNING BVA SUITE ON DURATION (BVA-01 to BVA-14)")
print("================================================================================")

bva_tests = [
    ("BRK-BVA-01", "Duration -1", -1, 400),
    ("BRK-BVA-02", "Duration 0", 0, 400),
    ("BRK-BVA-03", "Duration 1", 1, 200),
    ("BRK-BVA-04", "Duration 2", 2, 200),
    ("BRK-BVA-05", "Duration 14", 14, 200),
    ("BRK-BVA-06", "Duration 15", 15, 200),
    ("BRK-BVA-07", "Duration 16", 16, 200),
    ("BRK-BVA-08", "Duration 59", 59, 200),
    ("BRK-BVA-09", "Duration 60", 60, 200),
    ("BRK-BVA-10", "Duration 120", 120, 200),
    ("BRK-BVA-11", "Duration 480", 480, 200),
    ("BRK-BVA-12", "Duration 1440", 1440, 200),
    ("BRK-BVA-13", "Duration 2147483647 (Int32 max)", 2147483647, 400),
    ("BRK-BVA-14", "Duration 2147483648 (Overflow)", 2147483648, 400)
]

for tc_id, name, val, exp_st in bva_tests:
    payload = {
        "type": "Break", "name": {"en": f"BVA Duration {val} Policy"},
        "isActive": True, "tenantName": {"en": "Attendance"},
        "breaks": [{"name": f"Break {val}m", "type": 1, "durationMinutes": val}]
    }
    run_test(tc_id, name, "POST", "/break", payload, exp_st)

# Inspect MongoDB
print("================================================================================")
print("6. MONGODB INSPECTION FOR ATTENDANCE 7 (Type == 1)")
print("================================================================================")

att7_guid = uuid.UUID(company_id)
docs = list(mongo_col.find({"CompanyId": att7_guid, "Type": 1}))
print(f"Total Break Policies in MongoDB for Attendance 7: {len(docs)}")
for i, d in enumerate(docs[:10], 1):
    print(f"Doc {i}: ID={d.get('_id')} | Name={d.get('Name', {}).get('en')} | TotalDuration={d.get('TotalBreakDurationInMinutes')} | Paid={d.get('TotalPaidBreakDurationInMinutes')} | Unpaid={d.get('TotalUnpaidBreakDurationInMinutes')} | Breaks count={len(d.get('Breaks', []))}")

with open("scratch/att7_break_suite_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, default=str)

print("\n=== COMPLETED LIVE BREAK TEST SUITE ON ATTENDANCE 7 ===")
