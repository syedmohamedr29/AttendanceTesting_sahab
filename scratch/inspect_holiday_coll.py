import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('HolidayCalendars')
print(text[idx-50:idx+2500])

