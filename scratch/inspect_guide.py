import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for idx, line in enumerate(lines):
    if 'holiday' in line.lower() or 'publish' in line.lower():
        print(f"Line {idx+1}: {line.strip()[:100]}")

