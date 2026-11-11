import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Check DEFECT-20261028-01
t1 = '    .WithMessage("Daily flexible work duration cannot exceed 1440 minutes (24 hours).");\n```\n\n---\n\n#### Defect `DEFECT-20261028-02`:'
print("DEFECT-20261028-01 match:", t1 in text)

# Check DEFECT-20261028-03
t3 = '    throw new BusinessException("Cit.Attendance:1202", "Active Company Default Work Template cannot be archived or deleted.");\n}\n```\n\n---\n\n#### Defect `DEFECT-20261028-04`:'
print("DEFECT-20261028-03 match:", t3 in text)

# Check DEFECT-20261028-04
t4_search = "#### Defect `DEFECT-20261028-04`"
idx4 = text.find(t4_search)
if idx4 != -1:
    print("DEFECT-20261028-04 snippet:\n", text[idx4:idx4+500])

# Check DEFECT-20261028-07
t7_search = "#### Defect `DEFECT-20261028-07`"
idx7 = text.find(t7_search)
if idx7 != -1:
    print("DEFECT-20261028-07 snippet:\n", text[idx7:idx7+600])

