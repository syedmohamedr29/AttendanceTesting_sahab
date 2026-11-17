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

macro_match = re.search(r'<ac:structured-macro ac:name="info".*?</ac:structured-macro>', html, re.DOTALL)
if macro_match:
    print(macro_match.group(0))
