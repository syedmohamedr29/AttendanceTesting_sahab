import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

defects = [
    'DEFECT-20261028-01',
    'DEFECT-20261028-03',
    'DEFECT-20261028-04',
    'DEFECT-20261028-05',
    'DEFECT-20261028-06',
    'DEFECT-20261028-07'
]

for d in defects:
    h = f"#### Defect `{d}`"
    idx = text.find(h)
    if idx == -1:
        # try without backticks or with extra words
        for line in text.splitlines():
            if d in line and line.startswith('#### Defect'):
                print("Found alternate line:", line)
                idx = text.find(line)
                break
    print(f"\n==================== {d} at index {idx} ====================")
    sub = text[idx:idx+2500]
    next_sep = sub.find('\n---\n')
    if next_sep != -1:
        print(sub[max(0, next_sep-350):next_sep])
    else:
        print(sub[:300])

