import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

s1 = text.find('### <a id="defect-20261106-03">')
e1 = text.find('### <a id="defect-20261106-02">', s1)
print("=== DEFECT-20261106-03 ===")
print(text[s1:e1])

s2 = text.find('### <a id="defect-20261105-04">')
e2 = text.find('### <a id="defect-20261102-01">', s2)
print("=== DEFECT-20261105-04 ===")
print(text[s2:e2])
