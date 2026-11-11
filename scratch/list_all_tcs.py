import json

with open("scratch/all_user_scenarios_dump.json") as f:
    tcs = json.load(f)

for tc in tcs:
    print(f"{tc['tc_id']} | Row {tc['row']} | {tc['section']} | Title: {tc['scenario'][:50]}")

