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

target_rows = [10, 11, 12, 13, 14, 27, 28]

for idx, tr in enumerate(tr_pattern.finditer(html)):
    if idx in target_rows:
        tds = td_pattern.findall(tr.group(1))
        print(f'=== ROW {idx} ===')
        print('Remarks HTML:', tds[8])
