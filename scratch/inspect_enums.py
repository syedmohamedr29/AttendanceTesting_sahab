import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/attendance_swagger.json", "r", encoding="utf-8") as f:
    swagger = json.load(f)

schemas = swagger.get("components", {}).get("schemas", {})
for key in [
    "BreakItem", "BreakType",
    "GracePeriodDeviationPeriod", "GracePeriodLeaveDeductionType",
    "OvertimeRule", "OvertimeRate", "OvertimeDayRate"
]:
    print(f"=== {key} ===")
    print(json.dumps(schemas.get(key, {}), indent=2))

