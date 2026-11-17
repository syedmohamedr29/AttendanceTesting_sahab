# -*- coding: utf-8 -*-
with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('Part 4: Standardized Bug Lifecycle Procedure')
print(text[idx:idx+2000])
