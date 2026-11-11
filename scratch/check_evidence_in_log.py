import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

print('evidence_39 in log?', 'evidence_39' in text)
print('evidence_40 in log?', 'evidence_40' in text)
pos_ev = text.find('evidence_39')
if pos_ev != -1:
    print(text[pos_ev-100:pos_ev+400])

