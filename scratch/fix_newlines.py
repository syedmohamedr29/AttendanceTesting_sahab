with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'rb') as f:
    content = f.read()

# Replace \r\r\n or \r\n with \n
content_fixed = content.replace(b'\r\r\n', b'\r\n')
while b'\r\r\n' in content_fixed:
    content_fixed = content_fixed.replace(b'\r\r\n', b'\r\n')

with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'wb') as f:
    f.write(content_fixed)

with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Fixed! Total lines: {len(lines)}")

