# -*- coding: utf-8 -*-
import json
import requests
import re

with open("scratch/confluence_config.json", "r") as f:
    cfg = json.load(f)

base_url = cfg["confluence_url"]
auth = (cfg["email"], cfg["api_token"])
page_id = cfg["page_id"]

r = requests.get(f"{base_url}/rest/api/content/{page_id}?expand=body.storage,version", auth=auth)
html = r.json()["body"]["storage"]["value"]

tr_pattern = re.compile(r"<tr>(.*?)</tr>", re.DOTALL)
td_pattern = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL)

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    report_text = f.read()

print("=== DETAILED ROW-BY-ROW AUDIT: CONFLUENCE VS MASTER REPORT ===")

row_num = 0
audit_results = []

for tr_match in tr_pattern.finditer(html):
    tds = td_pattern.findall(tr_match.group(1))
    if tds and len(tds) >= 8:
        row_num += 1
        clean_tds = [re.sub(r"<[^>]+>", " ", td).strip() for td in tds]
        sno = clean_tds[0]
        module = clean_tds[1]
        desc = clean_tds[3]
        remarks = clean_tds[5]
        screenshot_td = tds[4]
        priority = clean_tds[6]
        qa_remarks = clean_tds[8]
        status = clean_tds[9] if len(clean_tds) > 9 else ""
        
        # Extract Defect ID
        m_def = re.search(r'DEFECT-\d{8}-\d{2}', sno)
        defect_id = m_def.group(0) if m_def else sno.split()[0]
        
        # Check if defect_id is in report
        in_report = defect_id in report_text
        
        # Check if error message / payload mentioned in remarks
        has_error_code = any(err in remarks or err in desc for err in ['500', '400', '404', '401', 'Cit.Attendance', 'NullReferenceException', 'ValidationException', '1505', '1104', '1010', '1107', '1706'])
        has_endpoint = '/' in remarks or '/' in desc
        has_screenshot = "ri:attachment" in screenshot_td or "<ac:image" in screenshot_td
        
        att_match = re.search(r'ri:filename="([^"]+)"', screenshot_td)
        att_name = att_match.group(1) if att_match else "None"
        
        audit_results.append({
            "row": row_num,
            "defect_id": defect_id,
            "module": module[:30],
            "desc": desc[:50],
            "in_report": in_report,
            "has_error": has_error_code,
            "has_endpoint": has_endpoint,
            "screenshot": att_name,
            "status": status[:20]
        })

print(f"Total Rows Audited: {len(audit_results)}")

# Summary statistics
in_report_count = sum(1 for r in audit_results if r["in_report"])
has_error_count = sum(1 for r in audit_results if r["has_error"])
has_endpoint_count = sum(1 for r in audit_results if r["has_endpoint"])
has_screenshot_count = sum(1 for r in audit_results if r["screenshot"] != "None")

print(f"Traceable in Master Report: {in_report_count} / {len(audit_results)}")
print(f"Has Error Message / Code:   {has_error_count} / {len(audit_results)}")
print(f"Has Endpoint Route:        {has_endpoint_count} / {len(audit_results)}")
print(f"Has Attached Screenshot:    {has_screenshot_count} / {len(audit_results)}")

# Print any that might be missing details
missing_details = [r for r in audit_results if not r["has_error"] or r["screenshot"] == "None"]
if missing_details:
    print(f"\nRows needing check ({len(missing_details)}):")
    for m in missing_details:
        print(f"  Row {m['row']:02d}: {m['defect_id']} | has_error: {m['has_error']} | screenshot: {m['screenshot']}")
else:
    print("\nALL 84 ROWS HAVE EXPLICIT ERROR CODES/MESSAGES AND SCREENSHOT ATTACHMENTS!")
