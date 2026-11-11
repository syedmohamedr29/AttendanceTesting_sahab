import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_150_cdwt_tcs.json', 'r', encoding='utf-8') as f:
    tcs = json.load(f)

for i, tc in enumerate(tcs):
    if i in [0, 5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 149]:
        print(f"Row {tc['row']:3d} | {tc['id']:<12} | {tc['sec'][:30]:<30} | {tc['scen'][:35]:<35} | Status: {tc['status']}")

