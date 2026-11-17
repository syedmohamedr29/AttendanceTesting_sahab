import re

filepath = 'Defects/Attendance2_Master_Defect_Log.md'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

for did in ['defect-20261028-04', 'defect-20261028-05', 'defect-20261028-06']:
    matches = [m.start() for m in re.finditer(did, text, re.IGNORECASE)]
    print(f"=== {did}: {len(matches)} matches ===")
    for m in matches:
        print(text[m-20:m+200].replace('\n', ' '))
        print('-'*30)
