import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="defect-20261105-01"', 30000)
# Look for the next defect or next major section
next_defect = text.find('### <a id="defect-', pos + 100)
print('Next defect at:', next_defect)
if next_defect != -1:
    print(text[next_defect-100:next_defect+300])
else:
    print('No next defect. Look for next major section:')
    # find next ## after pos
    next_sec = text.find('\n## ', pos + 1000)
    print(text[next_sec:next_sec+300])

