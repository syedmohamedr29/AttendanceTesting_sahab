import re

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

for did in ['DEFECT-20261028-04', 'DEFECT-20261028-05', 'DEFECT-20261028-06']:
    matches = [m.start() for m in re.finditer(re.escape(did), text)]
    print(f"*** {did}: {len(matches)} occurrences ***")
    for m in matches:
        line_start = text.rfind('\n', 0, m)
        line_end = text.find('\n', m)
        print(text[line_start:line_end].strip())
        if "####" in text[line_start-5:line_end] or "###" in text[line_start-5:line_end]:
            print("\n--- FULL SECTION PREVIEW ---")
            print(text[line_start:line_start+2000])
            print("----------------------------\n")
