import json
import requests

with open('scratch/confluence_config.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)

r = requests.get(f"{cfg['confluence_url']}/rest/api/content/{cfg['page_id']}?expand=version,body.storage", auth=(cfg['email'], cfg['api_token']))
data = r.json()
print("Version:", data['version']['number'])
body = data['body']['storage']['value']
print("Row count:", body.count('<tr>') - 1)
print("Contains DEFECT-20261103-01:", 'DEFECT-20261103-01' in body)
print("Contains DEFECT-20261103-02:", 'DEFECT-20261103-02' in body)
print("Contains evidence_18:", 'evidence_18_holiday_calendar_createdby_email_tenantname_empty.jpg' in body)
print("Contains evidence_19:", 'evidence_19_holiday_calendar_tenantname_empty_red_circle.jpg' in body)
