import json
import requests

with open('scratch/confluence_config.json', 'r') as f:
    cfg = json.load(f)

url = "https://zoolworks.atlassian.net/wiki/rest/api/content/1567752194/child/page"
r = requests.get(url, auth=(cfg['email'], cfg['api_token']))
if r.status_code == 200:
    results = r.json().get('results', [])
    print(f"Pages inside folder 1567752194: {len(results)}")
    for p in results:
        print(f"  ID: {p.get('id')} | Title: {p.get('title')}")
else:
    print('Error:', r.status_code, r.text)
