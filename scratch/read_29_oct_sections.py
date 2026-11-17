with open("Defects/Attendance2_Master_Defect_Log.md", "r", encoding="utf-8") as f:
    text = f.read()

for title in ["Part 3B: Live Execution", "Part 3C: Defects Identified on 29 October 2026"]:
    pos = text.find(title)
    print("=" * 60)
    print(title)
    if pos != -1:
        start = text.rfind("\n### ", 0, pos)
        next_sec = text.find("\n### ", pos + 30)
        print(text[start:next_sec if next_sec != -1 else pos + 2500])
