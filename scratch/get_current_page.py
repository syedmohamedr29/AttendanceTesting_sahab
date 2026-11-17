import json
import requests

with open('scratch/confluence_config.json', 'r') as f:
    cfg = json.load(f)

page_id = cfg['page_id']
url = f"https://zoolworks.atlassian.net/wiki/rest/api/content/{page_id}?expand=body.storage,version"
res = requests.get(url, auth=(cfg['email'], cfg['api_token']))
if res.status_code == 200:
    data = res.json()
    print('Title:', data.get('title'))
    print('Version:', data.get('version', {}).get('number'))
    body = data.get('body', {}).get('storage', {}).get('value', '')
    print('Body length:', len(body))
    with open('scratch/current_bug_fixes_page.html', 'w', encoding='utf-8') as out:
        out.write(body)
    print("Saved to scratch/current_bug_fixes_page.html")
else:
    print('Error:', res.status_code, res.text)
