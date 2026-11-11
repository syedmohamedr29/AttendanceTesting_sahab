import os, sys
sys.stdout.reconfigure(encoding='utf-8')

for root, dirs, files in os.walk('.'):
    for f in files:
        path = os.path.join(root, f)
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                for idx, line in enumerate(fp, 1):
                    if any(k in line.lower() for k in ['checklist', 'companymaster', 'workschedulescreated', 'companychecklist']):
                        print(f"{path}:{idx} -> {line.strip()[:140]}")
        except Exception:
            pass

