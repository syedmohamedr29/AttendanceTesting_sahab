with open("Defects/Attendance2_Master_Defect_Log.md", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("### 📊 Part 3G:")
print("Part 3G pos:", pos)
if pos != -1:
    pos_end = text.find("### 📊 Part 3H:", pos)
    print(text[pos:pos_end])
