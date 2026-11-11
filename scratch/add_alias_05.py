with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('USER-129', 'USER-129 / DEFECT-20261028-05')

with open('Defects/Attendance2_Master_Defect_Log.md', 'w', encoding='utf-8') as f:
    f.write(text)
print('Added DEFECT-20261028-05 alias!')

