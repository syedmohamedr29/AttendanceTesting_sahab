import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('evidence_39', 50000)
print('evidence_39 in Section 7 at:', pos)
print(text[pos-100:pos+500])

