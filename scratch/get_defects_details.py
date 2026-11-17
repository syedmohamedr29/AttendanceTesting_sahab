import re

with open("Defects/Attendance2_Master_Defect_Log.md", "r", encoding="utf-8") as f:
    text = f.read()

defects = [
    "DEFECT-20261105-01",
    "DEFECT-20261105-02",
    "DEFECT-20261105-03",
    "DEFECT-20261105-04",
    "DEFECT-20261106-01",
    "DEFECT-20261106-02",
    "DEFECT-20261106-03",
    "DEFECT-20261106-04",
    "DEFECT-20261106-05",
    "DEFECT-20261106-06",
    "DEFECT-20261106-07"
]

for d in defects:
    print("=" * 60)
    print("DEFECT:", d)
    # Search for header
    pos = text.find(d)
    while pos != -1:
        # Check if line looks like header
        line_start = text.rfind("\n", 0, pos) + 1
        line_end = text.find("\n", pos)
        line = text[line_start:line_end]
        if line.startswith("#"):
            print("Found Header:", line)
            # print up to next header
            next_header = text.find("\n### ", pos)
            if next_header == -1:
                next_header = pos + 2000
            print(text[line_start:min(line_start + 1200, next_header)])
            break
        pos = text.find(d, pos + len(d))
    else:
        print("No heading line found, printing first occurrence context:")
        pos = text.find(d)
        if pos != -1:
            print(text[max(0, pos-100):min(len(text), pos+600)])
