def check_mentions(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    print(f"=== {filename} ===")
    print("Mentions of Row 62:", "Row 62" in text)
    print("Mentions of Row 75:", "Row 75" in text)
    print("Mentions of Part 3J:", "Part 3J" in text)
    print("Mentions of Part 3K:", "Part 3K" in text)

check_mentions('Defects/Attendance2_Master_Defect_Log.md')
check_mentions('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md')
