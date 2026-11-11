import json, requests, sys

sys.stdout.reconfigure(encoding='utf-8')

token_data = json.load(open('scratch/current_token.json', encoding='utf-8'))
token = token_data.get('access_token')

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

company_id = "3a249871-7a8d-dec5-2d72-47795dd2662d"
loc_id = "3a24d646-b3cf-b1d4-61bb-1adf094b52fc" # Location 2
template_id = "7ecfbe95-8d3c-4612-a0cc-1454e9093a53" # FXD0001

payload = {
    "workPlanName": {
        "en": "Test Plan for Deletion Check",
        "ar": "خطة اختبار فحص الحذف"
    },
    "description": "Work plan created for deletion dependency verification",
    "workTemplateId": template_id,
    "policyIds": []
}

url = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/workplans?locationId={loc_id}"
res = requests.post(url, headers=headers, json=payload)
print(f"Create WorkPlan Status: {res.status_code}")
print(f"Response: {res.text}")
