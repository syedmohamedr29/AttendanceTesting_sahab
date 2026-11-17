with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

pos_3k = text.find('### 🏢 Part 3K:')
if pos_3k != -1:
    print(text[pos_3k:pos_3k + 2500])
else:
    print("Part 3K not found with that header")
