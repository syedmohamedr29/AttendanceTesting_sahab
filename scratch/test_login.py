import requests
import json

token_url = "https://auth8.dev.zoolwork.com/connect/token"
username = "syed.mohamed@comm-it.in"
password = "Admin@123"
tenant = "Attendance"

clients_to_test = ["Web", "WebGateway_Swagger", "SPA", "Attendance_Swagger"]

for client_id in clients_to_test:
    print(f"\n--- Testing client_id: {client_id} ---")
    
    # Attempt 1: Header __tenant
    data = {
        "grant_type": "password",
        "username": username,
        "password": password,
        "client_id": client_id,
        "scope": "openid profile email phone AttendanceSvc CompanySvc"
    }
    headers = {
        "__tenant": tenant,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        r = requests.post(token_url, data=data, headers=headers, timeout=10)
        print(f"Header __tenant -> Status: {r.status_code}")
        print("Response:", r.text[:300])
        if r.status_code == 200:
            print("SUCCESS! Token received!")
            token_json = r.json()
            with open("scratch/token.json", "w") as f:
                json.dump(token_json, f, indent=2)
            break
    except Exception as e:
        print("Error:", e)

    # Attempt 2: acr_values tenant:Attendance
    data["acr_values"] = f"tenant:{tenant}"
    try:
        r = requests.post(token_url, data=data, timeout=10)
        print(f"acr_values -> Status: {r.status_code}")
        print("Response:", r.text[:300])
        if r.status_code == 200:
            print("SUCCESS with acr_values! Token received!")
            with open("scratch/token.json", "w") as f:
                json.dump(r.json(), f, indent=2)
            break
    except Exception as e:
        print("Error:", e)
