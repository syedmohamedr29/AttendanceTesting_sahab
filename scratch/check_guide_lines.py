with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("Total lines:", len(lines))
for i in range(800, min(850, len(lines))):
    if 'holidaylist' in lines[i].lower():
        print(f"{i}: {lines[i].strip()}")

