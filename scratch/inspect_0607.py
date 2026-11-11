import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('### <a id="defect-20261106-07">')
print(text[idx:idx+1200])
