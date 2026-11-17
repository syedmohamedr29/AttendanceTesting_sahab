import json, requests, re

with open('scratch/confluence_config.json', 'r') as cfg_f:
    cfg = json.load(cfg_f)

base_url = cfg['confluence_url']
auth = (cfg['email'], cfg['api_token'])
page_id = cfg['page_id']

r = requests.get(f'{base_url}/rest/api/content/{page_id}?expand=body.storage,version', auth=auth)
html = r.json()['body']['storage']['value']

tr_pattern = re.compile(r'<tr>(.*?)</tr>', re.DOTALL)
td_pattern = re.compile(r'<td[^>]*>(.*?)</td>', re.DOTALL)

for idx, tr in enumerate(tr_pattern.finditer(html)):
    tds = td_pattern.findall(tr.group(1))
    if tds:
        clean = [re.sub(r'<[^>]+>', ' ', td).strip() for td in tds]
        first = clean[0] if len(clean) > 0 else ''
        module = clean[1] if len(clean) > 1 else ''
        remarks = clean[8] if len(clean) > 8 else ''
        if 'holiday' in first.lower() or 'holiday' in module.lower() or '20261103' in first:
            print(f'Row {idx:2d} | Col0: {first[:40]} | Col1: {module[:35]} | Remarks: {remarks[:60]}')
