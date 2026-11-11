import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('defects/WORK_TEMPLATE_DEFECTS.md', 'r', encoding='utf-8') as f:
    wt_text = f.read()

idx14 = wt_text.find('DEFECT-20261110-14')
print("In WORK_TEMPLATE_DEFECTS.md, DEFECT-14 is at:", idx14)
print(wt_text[idx14:idx14+2500])
