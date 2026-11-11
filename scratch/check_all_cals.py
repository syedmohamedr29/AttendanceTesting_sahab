import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/current_token.json') as f:
    token_data = json.load(f)

token = token_data['access_token']
headers = {
    'Authorization': f'Bearer {token}',
    '__tenant': 'Attendance',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

base_url = "https://attendance2.dev.zoolwork.com"
c3 = "3a247435-e31d-ef15-8cc9-62c587f4eb3f"
c8 = "3a249871-7a8d-dec5-2d72-47795dd2662d"

print("--- Attendance 3 Calendars ---")
r3 = requests.get(f"{base_url}/api/companies/{c3}/holidaylist", headers=headers)
for c in r3.json().get('holidayCalendars', []):
    print(f"ID: {c.get('id')} | Year: {c.get('yearlyCalendar', {}).get('year')} | ShortCode: {c.get('shortCode')} | Name: {c.get('name')} | CalType: {c.get('calendarType')}")

print("\n--- Attendance 8 Calendars ---")
r8 = requests.get(f"{base_url}/api/companies/{c8}/holidaylist", headers=headers)
for c in r8.json().get('holidayCalendars', []):
    print(f"ID: {c.get('id')} | Year: {c.get('yearlyCalendar', {}).get('year')} | ShortCode: {c.get('shortCode')} | Name: {c.get('name')} | CalType: {c.get('calendarType')}")

