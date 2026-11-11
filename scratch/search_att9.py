import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.md') or f.endswith('.py') or f.endswith('.json'):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as fp:
                    content = fp.read()
                    if 'Attendance 9' in content or 'Attendance9' in content:
                        print(f"Found in {path}")
            except Exception:
                pass

