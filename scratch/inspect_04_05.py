with open("Defects/Attendance2_Master_Defect_Log.md", "r", encoding="utf-8") as f:
    text = f.read()

for d in ["DEFECT-20261106-04", "DEFECT-20261106-05"]:
    anchor = f'### <a id="{d.lower()}"></a>'
    pos = text.find(anchor)
    print("=" * 60)
    print(d, "pos:", pos)
    if pos != -1:
        next_pos = text.find("\n### ", pos + 10)
        print(text[pos:next_pos if next_pos != -1 else pos + 3000])
