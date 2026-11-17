import json
import requests
import re
from collections import defaultdict

with open("scratch/confluence_config.json", "r") as f:
    cfg = json.load(f)

base_url = cfg["confluence_url"]
auth = (cfg["email"], cfg["api_token"])
page_id = cfg["page_id"]

r = requests.get(f"{base_url}/rest/api/content/{page_id}?expand=body.storage,version", auth=auth)
html = r.json()["body"]["storage"]["value"]

# Parse rows
rows = []
tr_pattern = re.compile(r"<tr>(.*?)</tr>", re.DOTALL)
td_pattern = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL)

for tr_match in tr_pattern.finditer(html):
    tr_content = tr_match.group(1)
    tds = td_pattern.findall(tr_content)
    if tds and len(tds) >= 8:
        clean_tds = [re.sub(r"<[^>]+>", " ", td).strip() for td in tds]
        rows.append({
            "sno": clean_tds[0],
            "module": clean_tds[1],
            "desc": clean_tds[3],
            "remarks": clean_tds[5] if len(clean_tds) > 5 else "",
        })

print("=" * 60)
print("CHECKING COMMON THEMES ACROSS CONFLUENCE ROWS:")

themes = {
    "TenantName Empty": ["tenantname", "empty", "object"],
    "CreatedBy Plain Email": ["createdby", "email"],
    "CompanyName Empty": ["companyname", "empty"],
    "Checklist Sync": ["checklist", "sync"],
    "Overtime Negative Rate": ["negative", "rateformula"],
    "Overtime Invariants (Enum 999/Rates)": ["overtime", "999"],
    "Break Null Crash": ["breaks", "null"],
    "Break Invariants (Enum 999/Duplicate)": ["break", "999"],
    "Grace Period Invariants": ["grace", "deviationperiod"],
    "Inverted Shift Timings": ["inverted", "endtime", "starttime"],
    "ShortCode Boundaries": ["shortcode"],
    "Publish Empty Calendar": ["publish", "empty"],
    "JWT Validation Bypass": ["jwt", "bypass"],
    "Swagger OAuth2": ["oauth2", "swagger"],
    "Location Delhi Cascade": ["delhi", "location"]
}

for theme_name, keywords in themes.items():
    matched_rows = []
    for idx, r in enumerate(rows, start=1):
        text = (r["desc"] + " " + r["remarks"] + " " + r["module"] + " " + r["sno"]).lower()
        if all(kw in text for kw in keywords):
            matched_rows.append((idx, r["sno"], r["module"], r["desc"][:80]))
    if len(matched_rows) > 1:
        print(f"\n[Theme: {theme_name}] Matches in {len(matched_rows)} rows:")
        for mr in matched_rows:
            print(f"  Row {mr[0]} | S.No: {mr[1]} | Module: {mr[2]} | Desc: {mr[3]}")
    elif len(matched_rows) == 1:
        print(f"[Theme: {theme_name}] Matches 1 row: Row {matched_rows[0][0]} ({matched_rows[0][1]})")
    else:
        print(f"[Theme: {theme_name}] Matches 0 rows")
