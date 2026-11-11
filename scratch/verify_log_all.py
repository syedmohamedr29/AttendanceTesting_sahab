import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

matches = [m.start() for m in re.finditer('DEFECT-20261105-02', text)]
print('Occurrences in Master Defect Log:', len(matches), matches)
for pos in matches:
    print('--- Match at:', pos)
    print(text[pos-40:pos+150])

