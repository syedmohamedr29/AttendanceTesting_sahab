import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('### <a id="defect-20261103-16">')
print('pos:', pos)
print(text[pos-200:pos+150])

