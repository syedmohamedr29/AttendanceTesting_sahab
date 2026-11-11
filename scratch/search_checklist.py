import os, sys
sys.stdout.reconfigure(encoding='utf-8')

keywords = ['checklist', 'workschedulescreated', 'companymaster', 'companycheck', 'schedulecreated', 'workschedule']

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith(('.md', '.xlsx', '.py', '.txt', '.json', '.pdf')):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                    for line_num, line in enumerate(fp, 1):
                        lower = line.lower()
                        for kw in keywords:
                            if kw in lower and ('check' in lower or 'master' in lower or 'company' in lower):
                                if any(x in lower for x in ['checklist', 'workschedulescreated', 'workschedules', 'checklist']):
                                    print(f"{f}:{line_num} [{kw}] -> {line.strip()[:140]}")
            except Exception:
                pass
