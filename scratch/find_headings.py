import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'###\s*<a\s*id=[^>]+></a>.*DEFECT-2026110[56]-.*', text):
    print(m.group()[:120])
