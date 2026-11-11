with open('scratch/audit_both_markdown_files.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("'DEFECT-20261106-04'", "'DEFECT-20261106-04', 'DEFECT-20261106-05', 'DEFECT-20261106-06'")
text = text.replace("'evidence_45'", "'evidence_45', 'evidence_46'")
text = text.replace("Evidence 40 to 45", "Evidence 40 to 46")

with open('scratch/audit_both_markdown_files.py', 'w', encoding='utf-8') as f:
    f.write(text)
print('Updated audit_both_markdown_files.py')
