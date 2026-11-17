with open("Defects/Attendance2_Master_Defect_Log.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(5720, 5780):
    print(f"{i+1}: {lines[i].rstrip()}")
