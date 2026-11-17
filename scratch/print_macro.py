import json, requests
with open('scratch/confluence_config.json', 'r') as f:
    cfg = json.load(f)
r = requests.get(f"{cfg['confluence_url'].rstrip('/')}/rest/api/content/1567653890?expand=body.storage", auth=(cfg['email'], cfg['api_token']))
body = r.json()['body']['storage']['value']
idx = body.find('</ac:rich-text-body>')
print(body[:idx+25])
