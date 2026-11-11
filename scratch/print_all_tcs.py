import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/all_150_cdwt_tcs.json", "r", encoding="utf-8") as f:
    tcs = json.load(f)

for tc in tcs:
    print(f"R{tc['row']:03d} | {tc['id']:<11} | {tc['sec'][:22]:<22} | {tc['scen'][:30]:<30} | {str(tc['exp'])[:40]}")

