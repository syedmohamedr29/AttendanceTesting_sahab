import sys
import json
import requests
import uuid

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/current_token.json') as f:
    token = json.load(f)['access_token']

base_url = 'https://attendance2.dev.zoolwork.com'
valid_cid = '3a249870-184c-0373-f344-015d602678d7' # Attendance 6

headers = {
    'Authorization': f'Bearer {token}',
    '__tenant': 'Attendance',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

results = []

def run_test(test_id, category, title, method, url, payload=None, expected=None):
    print(f"\n======================================================================")
    print(f"[{test_id}] [{category}] {title}")
    print(f"ROUTE: {method.upper()} {url}")
    if payload is not None:
        print("PAYLOAD:", json.dumps(payload, ensure_ascii=False))
    try:
        if method.lower() == 'get':
            r = requests.get(url, headers=headers, timeout=15)
        elif method.lower() == 'post':
            r = requests.post(url, headers=headers, json=payload, timeout=15)
        elif method.lower() == 'patch':
            r = requests.patch(url, headers=headers, json=payload, timeout=15)
        elif method.lower() == 'delete':
            r = requests.delete(url, headers=headers, timeout=15)
        
        status = r.status_code
        try:
            body = r.json()
        except:
            body = r.text
        print(f"STATUS: {status} (Expected: {expected})")
        print(f"RESPONSE: {json.dumps(body, ensure_ascii=False) if isinstance(body, dict) else str(body)[:200]}")
        results.append({
            'test_id': test_id,
            'category': category,
            'title': title,
            'method': method,
            'url': url,
            'payload': payload,
            'expected': expected,
            'status': status,
            'response': body
        })
        return status, body
    except Exception as e:
        print("ERROR:", e)
        results.append({
            'test_id': test_id,
            'category': category,
            'title': title,
            'method': method,
            'url': url,
            'payload': payload,
            'expected': expected,
            'status': 'EXCEPTION',
            'response': str(e)
        })
        return 'EXCEPTION', str(e)

print("=== STARTING COMPANY ID & DOC ID COMPREHENSIVE LIVE VERIFICATION ===")

# ======================================================================
# 1. COMPANY ID (URL ROUTE & BOUNDARY & ISOLATION)
# ======================================================================

# C1: Malformed companyId in URL route
run_test('TC-CMP-01', 'Company ID', 'Malformed companyId in GET route parameter', 'get',
         f"{base_url}/api/companies/invalid-guid-xyz/attpolicies",
         expected='404 (Route not matched)')

# C2: Guid.Empty companyId in URL route
run_test('TC-CMP-02', 'Company ID', 'All-zeros Guid.Empty companyId in GET route parameter', 'get',
         f"{base_url}/api/companies/00000000-0000-0000-0000-000000000000/attpolicies",
         expected='200 OK (Empty list: No Policies are found)')

# C3: Non-existing companyId in URL route (GET)
fake_cid = '99999999-9999-9999-9999-999999999999'
run_test('TC-CMP-03', 'Company ID', 'Non-existing companyId in GET route parameter', 'get',
         f"{base_url}/api/companies/{fake_cid}/attpolicies",
         expected='200 OK (Empty list: No Policies are found)')

# C4: Non-existing companyId in POST route
run_test('TC-CMP-04', 'Company ID', 'Non-existing companyId in POST Break route', 'post',
         f"{base_url}/api/companies/{fake_cid}/attpolicies/break",
         {'name': {'en': 'Ghost Company Policy'}, 'breaks': [{'name': 'Tea', 'type': 'Paid', 'durationMinutes': 10}]},
         expected='400 / 404 / 500 (Company Svc 404/500 lookup failure)')

# C5: Client injects spoofed companyId in request body on POST
run_test('TC-CMP-05', 'Company ID', 'Client supplies foreign companyId in POST body (Anti-Spoofing)', 'post',
         f"{base_url}/api/companies/{valid_cid}/attpolicies/break",
         {'companyId': '11111111-2222-3333-4444-555555555555', 'name': {'en': 'Spoof Company In Body'}, 'breaks': [{'name': 'Tea', 'type': 'Paid', 'durationMinutes': 10}]},
         expected='200 / 201 (Server enforces route companyId, ignores body companyId)')

# ======================================================================
# 2. DOC ID (REQUEST BODY & URL ROUTE & SERVER GENERATION)
# ======================================================================

# D1: POST with doc id completely omitted from body -> Auto-generated
s1, b1 = run_test('TC-DOC-01', 'Doc ID', 'POST with doc id completely omitted (Server Auto-Generation)', 'post',
         f"{base_url}/api/companies/{valid_cid}/attpolicies/break",
         {'name': {'en': 'Break Auto ID Omitted'}, 'breaks': [{'name': 'Snack', 'type': 'Paid', 'durationMinutes': 10}]},
         expected='200 OK / 201 Created (Server generates unique GUID)')
created_id_d1 = b1.get('id') if isinstance(b1, dict) else None
print(f"--> [TC-DOC-01 Resulting ID]: {created_id_d1}")

# D2: POST with explicit id: null in request body -> DTO conversion
run_test('TC-DOC-02', 'Doc ID', 'POST with explicit id: null in request body', 'post',
         f"{base_url}/api/companies/{valid_cid}/attpolicies/break",
         {'id': None, 'name': {'en': 'Break ID Null'}, 'breaks': [{'name': 'Coffee', 'type': 'Paid', 'durationMinutes': 15}]},
         expected='400 Bad Request (Cannot convert null to System.Guid)')

# D3: POST with Guid.Empty (00000000-0000-0000-0000-000000000000)
s3, b3 = run_test('TC-DOC-03', 'Doc ID', 'POST with Guid.Empty (all-zeros) id in request body', 'post',
         f"{base_url}/api/companies/{valid_cid}/attpolicies/break",
         {'id': '00000000-0000-0000-0000-000000000000', 'name': {'en': 'Break ID Guid.Empty'}, 'breaks': [{'name': 'Coffee', 'type': 'Paid', 'durationMinutes': 15}]},
         expected='200 OK (Server overwrites Guid.Empty with real GUID)')
created_id_d3 = b3.get('id') if isinstance(b3, dict) else None
print(f"--> [TC-DOC-03 Resulting ID]: {created_id_d3}")

# D4: POST with custom client-dictated GUID in body
custom_uuid = str(uuid.uuid4())
s4, b4 = run_test('TC-DOC-04', 'Doc ID', 'POST with client-dictated custom GUID in request body', 'post',
         f"{base_url}/api/companies/{valid_cid}/attpolicies/break",
         {'id': custom_uuid, 'name': {'en': 'Break ID Client Dictated'}, 'breaks': [{'name': 'Tea', 'type': 'Paid', 'durationMinutes': 20}]},
         expected='200 OK (Check whether server uses custom_uuid or generates new UUID)')
created_id_d4 = b4.get('id') if isinstance(b4, dict) else None
print(f"--> [TC-DOC-04 Sent ID vs Returned ID]: Sent={custom_uuid} | Returned={created_id_d4} | Equal={custom_uuid == created_id_d4}")

# D5: POST with malformed id (non-GUID string)
run_test('TC-DOC-05', 'Doc ID', 'POST with malformed non-GUID string in id property', 'post',
         f"{base_url}/api/companies/{valid_cid}/attpolicies/break",
         {'id': 'INVALID-POLICY-ID-STRING', 'name': {'en': 'Doc ID Malformed'}, 'breaks': [{'name': 'Tea', 'type': 'Paid', 'durationMinutes': 15}]},
         expected='400 Bad Request (JSON conversion error System.Guid)')

# D6: GET policy by malformed policyId GUID in URL
run_test('TC-DOC-06', 'Doc ID', 'GET policy by malformed non-GUID policyId in URL', 'get',
         f"{base_url}/api/companies/{valid_cid}/attpolicies/invalid-uuid-in-url",
         expected='404 Not Found (Route not matched)')

# D7: GET policy by non-existing policyId GUID in URL
non_exist_id = '00000000-0000-0000-0000-999999999999'
run_test('TC-DOC-07', 'Doc ID', 'GET policy by non-existing policyId GUID in URL', 'get',
         f"{base_url}/api/companies/{valid_cid}/attpolicies/{non_exist_id}",
         expected='400 Bad Request / 404 (Cit.Attendance:1501 Policy not found)')

# D8: PATCH policy with URL policyId vs Body id mismatch
if created_id_d1:
    mismatch_id = str(uuid.uuid4())
    run_test('TC-DOC-08', 'Doc ID', 'PATCH policy with URL policyId vs Body id mismatch', 'patch',
             f"{base_url}/api/companies/{valid_cid}/attpolicies/break/{created_id_d1}",
             {'id': mismatch_id, 'name': {'en': 'Updated Break - Mismatch ID'}, 'breaks': [{'name': 'Snack', 'type': 'Paid', 'durationMinutes': 12}]},
             expected='200 OK (URL ID enforced, body ID ignored) or 400 Bad Request')

# D9: PATCH policy with malformed policyId in URL
run_test('TC-DOC-09', 'Doc ID', 'PATCH policy with malformed policyId in URL', 'patch',
         f"{base_url}/api/companies/{valid_cid}/attpolicies/break/invalid-uuid-in-url",
         {'name': {'en': 'Malformed URL ID'}, 'breaks': [{'name': 'Snack', 'type': 'Paid', 'durationMinutes': 12}]},
         expected='404 Not Found (Route not matched)')

# D10: PATCH policy with non-existing policyId in URL
run_test('TC-DOC-10', 'Doc ID', 'PATCH policy with non-existing policyId in URL', 'patch',
         f"{base_url}/api/companies/{valid_cid}/attpolicies/break/{non_exist_id}",
         {'name': {'en': 'Non-Existing URL ID'}, 'breaks': [{'name': 'Snack', 'type': 'Paid', 'durationMinutes': 12}]},
         expected='400 Bad Request (Cit.Attendance:1501 Policy not found)')

# D11: Soft-delete policy via PATCH /delete
if created_id_d1:
    run_test('TC-DOC-11', 'Doc ID', 'Soft-delete policy preserves _id in database', 'patch',
             f"{base_url}/api/companies/{valid_cid}/attpolicies/{created_id_d1}/delete",
             expected='200 OK / 204 No Content')

# D12: Soft-delete with malformed policyId
run_test('TC-DOC-12', 'Doc ID', 'Soft-delete with malformed policyId in URL', 'patch',
         f"{base_url}/api/companies/{valid_cid}/attpolicies/invalid-guid/delete",
         expected='404 Not Found')

# D13: Soft-delete with non-existing policyId
run_test('TC-DOC-13', 'Doc ID', 'Soft-delete with non-existing policyId in URL', 'patch',
         f"{base_url}/api/companies/{valid_cid}/attpolicies/{non_exist_id}/delete",
         expected='400 Bad Request (Cit.Attendance:1501 Policy not found)')

with open('scratch/company_and_doc_id_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\n=== COMPLETED ALL LIVE COMPANY ID & DOC ID TESTS ===")

