import re

def inspect_file(filename):
    print(f"=== Inspecting {filename} ===")
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Find all headings with 3J, 3K, Part X, Part XI, etc.
    headings = re.findall(r'(#{1,4}\s+[^\n]+(?:3[JK]|12 November|14 November|Part [IXV]+|Shifts & Rotation)[^\n]*)', text, re.IGNORECASE)
    for h in headings[:25]:
        print("  ", h)

inspect_file('Defects/Attendance2_Master_Defect_Log.md')
inspect_file('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md')
