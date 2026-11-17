import re

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
for i, line in enumerate(lines):
    if line.startswith('#'):
        # Check if following line has <a id="...">
        anchor = ""
        if i + 1 < len(lines) and lines[i+1].startswith('<a id='):
            anchor = lines[i+1].strip()
        elif i + 2 < len(lines) and lines[i+2].startswith('<a id='):
            anchor = lines[i+2].strip()
        print(f"L{i+1}: {line[:70]} | Anchor: {anchor}")
