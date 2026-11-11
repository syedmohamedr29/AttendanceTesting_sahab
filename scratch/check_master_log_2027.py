import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    content = f.read()

for i in range(1, 8):
    d_id = f"DEFECT-20261027-{i:02d}"
    idx = content.find(d_id)
    print(f"\nSearching {d_id}:")
    while idx != -1:
        line_start = content.rfind('\n', 0, idx) + 1
        line_end = content.find('\n', idx)
        print(f"  Line: {content[line_start:line_end]}")
        idx = content.find(d_id, idx + len(d_id))

