import json, requests, sys

sys.stdout.reconfigure(encoding='utf-8')

token_data = json.load(open('scratch/current_token.json', encoding='utf-8'))
token = token_data.get('access_token')

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

company_id = "3a249871-7a8d-dec5-2d72-47795dd2662d"
loc_id = "3a24d646-b3cf-b1d4-61bb-1adf094b52fc"
deleted_template_id = "cf3ef115-b548-436b-afd1-568be4f5ebfa"

payload = {
    "workPlanName": {
        "en": "Work Plan with Deleted Template",
        "ar": "خطة عمل مع قالب محذوف"
    },
    "description": "Attempting to create a work plan referencing a soft-deleted work template",
    "workTemplateId": deleted_template_id,
    "policyIds": []
}

url = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/workplans?locationId={loc_id}"
res = requests.post(url, headers=headers, json=payload)
print(f"Create WP with Deleted Template Status: {res.status_code}")
print(f"Response: {res.text}")
