import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

for d in ['DEFECT-20261028-01', 'DEFECT-20261028-03', 'DEFECT-20261028-04', 'DEFECT-20261028-05', 'DEFECT-20261028-06', 'DEFECT-20261028-07']:
    idx = text.find(d)
    print(f"--- {d} at index {idx} ---")
    sub = text[idx:idx+1500]
    next_sep = sub.find('\n---\n')
    if next_sep != -1:
        print(sub[max(0, next_sep-200):next_sep+30])
    else:
        print(sub[:300])

