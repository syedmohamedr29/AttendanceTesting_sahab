import re

files = [
    "Defects/Attendance2_Master_Defect_Log.md",
    "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"
]

for fpath in files:
    with open(fpath, "r", encoding="utf-8") as f:
        text = f.read()
    print("=" * 60)
    print(f"File: {fpath} (Length: {len(text)} chars)")
    pos = text.find("### 📊 Master Re-Verification & Deduplication Summary (Rows 1 to 40 — Confluence Version 17)")
    print("Master Summary Header pos:", pos)
    # Count occurrences of Row 29 DEFECT-20261105-01
    count_row29 = text.count("Row 29 | `DEFECT-20261105-01`") + text.count("Row 29 | DEFECT-20261105-01") + text.count("✅ Row 29 | DEFECT-20261105-01")
    print("Occurrences of duplicate Row 29 for DEFECT-20261105-01:", count_row29)
    # Check what Row 29 is now
    pos_r29 = text.find("**29** |")
    if pos_r29 != -1:
        line_start = text.rfind("\n", 0, pos_r29) + 1
        line_end = text.find("\n", pos_r29)
        print("Row 29 definition:", text[line_start:line_end].strip()[:90])
