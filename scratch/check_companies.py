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
    'Accept': 'application/json'
}

base_url = "https://attendance2.dev.zoolwork.com"

# Let's check companies from scratch/companies_list.json if it exists
try:
    with open('scratch/companies_list.json', 'r', encoding='utf-8') as f:
        comps = json.load(f)
    print("Found companies_list.json, count:", len(comps))
    for c in comps[:10]:
        print(f"ID: {c.get('id')}, Name: {c.get('companyName') or c.get('name')}")
except Exception as e:
    print("Error reading companies_list.json:", e)

