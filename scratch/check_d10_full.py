import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('### <a id="defect-20261110-10">')
idx_next = text.find('### <a id="defect-20261110-11">')
print(text[idx:idx_next])
