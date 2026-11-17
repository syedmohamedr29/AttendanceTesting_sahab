import requests

hosts = ['https://attendance2.dev.zoolwork.com', 'https://gw8.dev.zoolwork.com', 'https://sp.dev.zoolwork.com', 'https://company8.dev.zoolwork.com']

for h in hosts:
    try:
        r = requests.get(f"{h}/swagger/index.html", timeout=5)
        print(f"{h}: {r.status_code}")
    except Exception as e:
        print(f"{h}: Error: {e}")
