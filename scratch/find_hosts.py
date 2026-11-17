import glob
import re

hosts = set()
for f in glob.glob('scratch/*.py'):
    try:
        with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
            c = fp.read()
            m = re.findall(r'https?://[a-zA-Z0-9.-]+\.zoolwork\.com[^\s\'\"]*', c)
            for item in m:
                hosts.add(item.split('/')[2])
    except Exception:
        pass

print("Discovered zoolwork hosts:", sorted(hosts))
