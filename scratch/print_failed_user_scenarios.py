import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/failed_user_scenarios.json', encoding='utf-8') as f:
    fails = json.load(f)

for i, f in enumerate(fails, 1):
    print(f"[{i:02d}] {f['id']} (Row {f['row']}) | Pri: {f['pri']} | Scen: {f['scen']}")
    print(f"     Exp: {str(f['exp'])[:80]}")
    print(f"     Act: {str(f['remark'])[:80]}")

