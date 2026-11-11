import json

with open("scratch/all_user_scenarios_dump.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for row in data:
    txt = row.get("scenario", "") + " " + row.get("input_pre", "") + " " + row.get("remarks", "")
    if any(k in txt.lower() for k in ["shortcode", "templatename", "duration", "dayenum", "starttime", "endtime"]):
        print(f"{row['tc_id']} | {row.get('scenario')} | Status: {row.get('status')}")

