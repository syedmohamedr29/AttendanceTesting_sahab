# Fix extractors in scratch/run_full_scheduler_test_suite.py

with open("scratch/run_full_scheduler_test_suite.py", "r", encoding="utf-8") as f:
    code = f.read()

# Replace board id extractions
old_snippet = """r = requests.post(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards?locationId={LOC_DAMMAM}", headers=headers, json=payload_b01, verify=False, timeout=10)
if r.status_code == 200:
    b_data = r.json()
    b_id = b_data.get("id") or b_data.get("boardId")
    context["board1_id"] = b_id
    # extract area ids
    areas = b_data.get("areas", [])
    if areas and len(areas) >= 2:
        context["area1_id"] = areas[0].get("id")
        context["area2_id"] = areas[1].get("id")"""

new_snippet = """r = requests.post(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards?locationId={LOC_DAMMAM}", headers=headers, json=payload_b01, verify=False, timeout=10)
if r.status_code == 200:
    res_json = r.json()
    b_data = res_json.get("board") or res_json
    b_id = b_data.get("id") or b_data.get("boardId")
    context["board1_id"] = b_id
    areas = b_data.get("areas", [])
    if areas and len(areas) >= 2:
        context["area1_id"] = areas[0].get("areaId") or areas[0].get("id")
        context["area2_id"] = areas[1].get("areaId") or areas[1].get("id")"""

code = code.replace(old_snippet, new_snippet)

# Replace board2 extraction
old_b2 = """r = requests.post(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards?locationId={LOC_DAMMAM}", headers=headers, json=payload_b02, verify=False, timeout=10)
if r.status_code == 200:
    b_id = r.json().get("id")
    context["board2_id"] = b_id"""

new_b2 = """r = requests.post(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards?locationId={LOC_DAMMAM}", headers=headers, json=payload_b02, verify=False, timeout=10)
if r.status_code == 200:
    b_data2 = r.json().get("board") or r.json()
    b_id = b_data2.get("id")
    context["board2_id"] = b_id"""

code = code.replace(old_b2, new_b2)

with open("scratch/run_full_scheduler_test_suite.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated extractors in runner script.")
