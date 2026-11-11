import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('defects/WORK_TEMPLATE_DEFECTS.md', 'r', encoding='utf-8') as f:
    wt_text = f.read()

idx14 = wt_text.rfind('DEFECT-20261110-14')
print(wt_text[idx14:])
