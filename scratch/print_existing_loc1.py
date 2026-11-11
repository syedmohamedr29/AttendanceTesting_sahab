import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/loc1_templates_live.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

templates = d.get('templates', [])
print(f"Total templates in Location 1: {len(templates)}")
for t in templates:
    name_obj = t.get('workTemplateName', {})
    print(f"- ID: {t.get('id')} | ShortCode: {t.get('shortCode')} | Type: {t.get('templateType')} | Duration: {t.get('totalWorkDurationInMinutes')} | Name: {name_obj.get('en')} / {name_obj.get('ar')}")
