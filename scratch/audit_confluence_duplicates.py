from bs4 import BeautifulSoup
import re
from collections import defaultdict

with open('scratch/current_bug_fixes_page.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

table = soup.find('table')
rows = table.find_all('tr')[1:] # skip header

print(f"Total rows on Confluence: {len(rows)}")

row_data = []
defect_occurrences = defaultdict(list)

for idx, r in enumerate(rows):
    cells = [td.get_text(strip=True) for td in r.find_all(['td', 'th'])]
    sno = cells[0]
    module = cells[1]
    desc = cells[3]
    dev_status = cells[7]
    qa_remarks = cells[8]
    
    # Extract defect IDs mentioned in this row
    d_ids = re.findall(r'DEFECT-\d{8}-\d{2}|USER-\d+|DOC-[A-Z]-\d+|ROOT-[A-Z]-\d+', sno + ' ' + desc + ' ' + qa_remarks)
    
    row_data.append({
        'row_num': idx + 1,
        'sno': sno,
        'module': module,
        'desc': desc[:60],
        'ids': d_ids
    })
    
    for d in d_ids:
        defect_occurrences[d].append(idx + 1)
    
    print(f"Row {idx+1}: S.no={sno} | Module={module} | IDs={d_ids}")

print("\n=== CONFLUENCE DEFECT ID OCCURRENCES ===")
multi_row_defects = {k: v for k, v in defect_occurrences.items() if len(v) > 1}
if multi_row_defects:
    print(f"Defect IDs appearing in multiple rows on Confluence: {len(multi_row_defects)}")
    for k, v in multi_row_defects.items():
        print(f"  {k} appears in Rows: {v}")
else:
    print("No defect ID appears in more than one row on Confluence! Every row is 100% unique.")

