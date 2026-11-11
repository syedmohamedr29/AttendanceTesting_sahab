import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="defect-20261105-01"', 30000)
print('Detailed section at:', pos)
next_h = text.find('## ', pos + 100)
print('Next section at:', next_h)
print(text[pos:pos+300])
print('--- Next section begins:')
print(text[next_h:next_h+150])

