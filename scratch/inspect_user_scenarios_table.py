import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

start_marker = "### Full Sheet Execution Results for `User Scenarios (Add Here)` (138 Test Cases)"
end_marker = "### Full Sheet Execution Results for `WT - Company Default` (150 Test Cases)"

idx1 = text.find(start_marker)
idx2 = text.find(end_marker)

print(f"Table start: {idx1}, end: {idx2}")
print(text[idx1:idx2])

