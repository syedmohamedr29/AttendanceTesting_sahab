import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/add_policies_dto_validations_sheet.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('POL-DTO-58')
print(text[idx:idx+2500])

