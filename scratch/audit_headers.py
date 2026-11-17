# -*- coding: utf-8 -*-
import re

def check_anchors(filepath):
    print(f"=== Checking {filepath} ===")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all Markdown headers
    headers = re.findall(r'^(#{1,4})\s+(.+)$', content, re.MULTILINE)
    print(f"Total headers: {len(headers)}")
    
    # Search for specific sections
    keywords = [
        "Part 3I", "Attendance 12", "Part 3J", "Part 3K", "Part 3L", "Part 3M", 
        "Part 3N", "Location Shifts", "PART 12", "Overall Consolidated Test Execution Dashboard",
        "Master Re-Verification", "Latest Defect Update"
    ]
    for kw in keywords:
        found = [(h[0], h[1]) for h in headers if kw.lower() in h[1].lower()]
        print(f"Keyword '{kw}': {len(found)} matches -> {found[:2]}")

check_anchors("Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md")
check_anchors("Defects/Attendance2_Master_Defect_Log.md")
