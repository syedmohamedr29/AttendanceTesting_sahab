import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Check DEFECT-20261026-01 block
start1 = text.find('#### Defect `DEFECT-20261026-01`')
end1 = text.find('#### Defect `DEFECT-20261026-02`')
print("=== DEFECT-20261026-01 ===")
print(text[start1:end1])

# Check DEFECT-20261026-02 block
start2 = end1
end2 = text.find('#### Defect `DEFECT-20261026-03`')
print("=== DEFECT-20261026-02 ===")
print(text[start2:end2])

# Check DEFECT-20261026-03 block
start3 = end2
end3 = text.find('#### Defect `DEFECT-20261026-04`')
print("=== DEFECT-20261026-03 ===")
print(text[start3:end3])

