import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/build_complete_excel_file.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('if "INDEX" in master_wb.sheetnames:')
print(text[idx:idx+1200])

