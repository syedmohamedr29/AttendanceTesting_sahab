import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.py'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                c = fp.read()
                if 'company8.dev.zoolwork.com' in c:
                    print(f"Found in {p}")

