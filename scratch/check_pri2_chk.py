import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('### Priority 2: Audit', 100000)
print('pos of Priority 2 in Checklist:', pos)
if pos != -1:
    print(text[pos:pos+400])

