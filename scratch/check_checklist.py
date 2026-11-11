import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('DEFECT-20261105-01', 100000)
print('Checklist occurrence at:', pos)
print(text[pos-100:pos+400])

