with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if '### module 5:' in line.lower():
        for j in range(max(0, idx - 2), min(len(lines), idx + 25)):
            print(f"{j+1}: {lines[j].rstrip()}")
        break

