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
wp_id = "0dea229a-7c98-4cf2-a819-06279481efac"
template_id = "cf3ef115-b548-436b-afd1-568be4f5ebfa"

# 1. Delete the Work Plan
url_del_wp = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/workplans/{wp_id}/delete?locationId={loc_id}"
res_wp = requests.patch(url_del_wp, headers=headers)
print(f"Delete Work Plan Status: {res_wp.status_code}")
print(f"Delete Work Plan Response: {res_wp.text}")

# 2. Try deleting the template again
url_del_wt = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates/{template_id}/delete?locationId={loc_id}"
res_wt = requests.patch(url_del_wt, headers=headers)
print(f"\nDelete Template After WP Deletion Status: {res_wt.status_code}")
print(f"Delete Template After WP Deletion Response: {res_wt.text}")
