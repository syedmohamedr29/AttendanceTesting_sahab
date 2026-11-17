# -*- coding: utf-8 -*-
import json
import requests

CONFIG_FILE = 'scratch/confluence_config.json'

with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    cfg = json.load(f)

auth = (cfg['email'], cfg['api_token'])
base_url = cfg['confluence_url']
page_id = cfg['page_id']

r = requests.get(f"{base_url}/rest/api/content/{page_id}?expand=version,body.storage", auth=auth)
data = r.json()
ver = data['version']['number']
body = data['body']['storage']['value']

link_macro = (
    '<p><strong>Dedicated Module Report:</strong> '
    '<ac:link><ri:page ri:content-title="Holiday Calendar &amp; Senior QA Defect Audit (17 November 2026)" />'
    '<ac:link-body>Holiday Calendar &amp; Senior QA Defect Audit (17 November 2026 &mdash; Page ID: 1570308098)</ac:link-body></ac:link></p>'
)

if "Dedicated Module Report:" not in body:
    new_body = body.replace('</ac:rich-text-body>', link_macro + '\n</ac:rich-text-body>', 1)
    put_data = {
        'id': page_id,
        'type': 'page',
        'title': data['title'],
        'space': {'key': 'Testing'},
        'version': {'number': ver + 1},
        'body': {'storage': {'value': new_body, 'representation': 'storage'}}
    }
    r_put = requests.put(f"{base_url}/rest/api/content/{page_id}", auth=auth, json=put_data)
    print("Updated master page status:", r_put.status_code, "New version:", ver + 1)
else:
    print("Already cross-linked!")
