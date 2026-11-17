import requests, json

with open('scratch/confluence_config.json', 'r') as f:
    cfg = json.load(f)

base_url = cfg['confluence_url'].rstrip('/')
auth = (cfg['email'], cfg['api_token'])

url = f"{base_url}/rest/api/content/1567653890?expand=version,body.storage"
r = requests.get(url, auth=auth)
data = r.json()
print("Master Page 1567653890 Version:", data['version']['number'])
body = data['body']['storage']['value']
print("Master Has DEFECT-20261117-07:", "DEFECT-20261117-07" in body)
print("Master Has DEFECT-20261117-11:", "DEFECT-20261117-11" in body)

url2 = f"{base_url}/rest/api/content/1570308098?expand=version,body.storage"
r2 = requests.get(url2, auth=auth)
data2 = r2.json()
print("Dedicated Page 1570308098 Version:", data2['version']['number'])
body2 = data2['body']['storage']['value']
print("Dedicated Has DEFECT-20261117-07:", "DEFECT-20261117-07" in body2)
print("Dedicated Has DEFECT-20261117-11:", "DEFECT-20261117-11" in body2)
