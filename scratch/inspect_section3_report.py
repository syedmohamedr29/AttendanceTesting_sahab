# -*- coding: utf-8 -*-
with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('## 3. Module 1: Holiday Calendar Module')
print("Section 3 index:", idx)
print(text[idx:idx+1500])
