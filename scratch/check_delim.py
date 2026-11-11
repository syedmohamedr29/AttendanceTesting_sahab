import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    rep_text = f.read()

# In Report MD, DEFECT-15 starts at:
start_str = "#### Defect `DEFECT-20261110-15`"
end_str = "#### Defect `DEFECT-20261110-10`"

p1 = rep_text.find(start_str)
p2 = rep_text.find(end_str)
print(f"Report MD: p1={p1}, p2={p2}")

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    log_text = f.read()

start_str_log = '### <a id="defect-20261110-15">'
end_str_log = '### <a id="defect-20261110-10">'

lp1 = log_text.find(start_str_log)
lp2 = log_text.find(end_str_log)
print(f"Master Log: lp1={lp1}, lp2={lp2}")
