import re

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find Part 3J
pos_3j = text.find('Part 3J:')
pos_3k = text.find('Part 3K:')
pos_3l = text.find('Part 3L:')

print(f"Pos 3J: {pos_3j}, Pos 3K: {pos_3k}, Pos 3L: {pos_3l}")

if pos_3j != -1 and pos_3k != -1:
    section_3j = text[pos_3j:pos_3k]
    print(f"Section 3J length: {len(section_3j)}")
    # Find all defect headings in 3J
    d_3j = re.findall(r'####\s+Defect\s+`([^`]+)`:\s+([^\n]+)', section_3j)
    for d, title in d_3j:
        print(f"  3J Defect: {d} -> {title[:80]}")

if pos_3k != -1:
    end_3k = pos_3l if pos_3l != -1 else len(text)
    section_3k = text[pos_3k:end_3k]
    print(f"Section 3K length: {len(section_3k)}")
    d_3k = re.findall(r'####\s+Defect\s+`([^`]+)`:\s+([^\n]+)', section_3k)
    for d, title in d_3k:
        print(f"  3K Defect: {d} -> {title[:80]}")
