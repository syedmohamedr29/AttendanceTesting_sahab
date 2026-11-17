# -*- coding: utf-8 -*-
import requests

urls = [
    "https://gw8.dev.zoolwork.com",
    "https://sp.dev.zoolwork.com",
    "https://auth8.dev.zoolwork.com",
    "https://company8.dev.zoolwork.com"
]

for u in urls:
    try:
        r = requests.get(u, timeout=5, verify=False)
        print(f"{u}: status {r.status_code}")
    except Exception as e:
        print(f"{u}: failed - {type(e).__name__}: {e}")
