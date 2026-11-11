import requests
import json
import base64
import time
from playwright.sync_api import sync_playwright

# 1. Get Auth Token
token_url = "https://auth8.dev.zoolwork.com/connect/token"
data = {
    "grant_type": "password",
    "username": "syed.mohamed@comm-it.in",
    "password": "Admin@123",
    "client_id": "Web",
    "scope": "offline_access openid profile email phone AccountService IdentityService AdministrationService CompanySvc AttendanceSvc"
}
headers = {
    "__tenant": "Attendance",
    "Content-Type": "application/x-www-form-urlencoded"
}

print("1. Requesting auth token from auth8.dev.zoolwork.com...")
r = requests.post(token_url, data=data, headers=headers, timeout=15)
if r.status_code != 200:
    print(f"Failed to get token: {r.status_code} - {r.text}")
    exit(1)

token_data = r.json()
access_token = token_data["access_token"]
print("Auth token obtained successfully!")

# Decode JWT payload (without verify for inspection)
jwt_parts = access_token.split(".")
if len(jwt_parts) > 1:
    payload_b64 = jwt_parts[1] + "=="
    payload_json = json.loads(base64.urlsafe_b64decode(payload_b64.encode()))
    print(f"Token Sub: {payload_json.get('sub')}")
    print(f"Token TenantId: {payload_json.get('tenantid')}")
    print(f"Token Email: {payload_json.get('email')}")

# Save token to scratch
with open("scratch/current_token.json", "w") as f:
    json.dump({
        "access_token": access_token,
        "tenant_id": payload_json.get("tenantid"),
        "user_id": payload_json.get("sub"),
        "email": payload_json.get("email")
    }, f, indent=2)

# 2. Find Company "Attendance2" from Company Service
print("\n2. Querying Company Service for company 'Attendance2'...")
company_api_headers = {
    "Authorization": f"Bearer {access_token}",
    "__tenant": "Attendance",
    "Accept": "application/json"
}

company_id = None
company_name = None

# Try different company endpoints
for comp_endpoint in [
    "https://company8.dev.zoolwork.com/api/company/companies",
    "https://company8.dev.zoolwork.com/api/company/companies/lookup",
    "https://company8.dev.zoolwork.com/api/app/company"
]:
    try:
        r_comp = requests.get(comp_endpoint, headers=company_api_headers, timeout=10)
        print(f"Endpoint {comp_endpoint} -> Status: {r_comp.status_code}")
        if r_comp.status_code == 200:
            comp_res = r_comp.json()
            items = comp_res.get("items", comp_res) if isinstance(comp_res, dict) else comp_res
            if isinstance(items, list):
                print(f"Found {len(items)} companies:")
                for c in items:
                    c_id = c.get("id") or c.get("companyId")
                    c_name = c.get("name") or c.get("companyName")
                    print(f"  - Company: '{c_name}' (ID: {c_id})")
                    if c_name and "attendance2" in str(c_name).lower():
                        company_id = c_id
                        company_name = c_name
            if company_id:
                break
    except Exception as e:
        print(f"Error querying {comp_endpoint}: {e}")

if not company_id:
    # Try searching companies
    try:
        r_search = requests.get("https://company8.dev.zoolwork.com/api/company/companies?filter=Attendance2", headers=company_api_headers, timeout=10)
        print("Search status:", r_search.status_code, r_search.text[:200])
    except Exception as e:
        pass

print(f"\nTarget Company Selected: '{company_name}' -> ID: {company_id}")

with open("scratch/target_company.json", "w") as f:
    json.dump({
        "company_id": str(company_id),
        "company_name": str(company_name),
        "tenant": "Attendance",
        "tenant_id": payload_json.get("tenantid")
    }, f, indent=2)

# 3. Connect to Swagger using Playwright
print("\n3. Launching Playwright to connect to Swagger...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1400, "height": 900})
    page = context.new_page()

    # --- Attendance2 Swagger ---
    att_swagger_url = "https://attendance2.dev.zoolwork.com/swagger/index.html"
    print(f"Navigating to {att_swagger_url}...")
    page.goto(att_swagger_url, wait_until="networkidle", timeout=30000)
    time.sleep(2)

    # Click Authorize button
    auth_btn = page.locator("button.btn.authorize")
    if auth_btn.count() > 0:
        print("Clicking Authorize button in Attendance2 Swagger...")
        auth_btn.first.click()
        time.sleep(1)

        # Enter token
        # In Swagger UI, input field has value or placeholder
        token_input = page.locator("div.modal-ux input[type='text']")
        if token_input.count() > 0:
            print("Entering Bearer token in Swagger modal...")
            token_input.first.fill(f"Bearer {access_token}")
            time.sleep(0.5)

            # Click Authorize inside modal
            modal_auth_btn = page.locator("div.modal-ux button.btn.modal-btn.auth")
            if modal_auth_btn.count() > 0:
                modal_auth_btn.first.click()
                print("Clicked Authorize inside modal.")
                time.sleep(1)

            # Click Close
            close_btn = page.locator("div.modal-ux button.btn.modal-btn.btn-done")
            if close_btn.count() > 0:
                close_btn.first.click()
                print("Clicked Close modal.")
                time.sleep(1)

    screenshot_path = "scratch/swagger_attendance2_authorized.png"
    page.screenshot(path=screenshot_path, full_page=False)
    print(f"Screenshot saved to {screenshot_path}")

    # --- Company8 Swagger ---
    comp_swagger_url = "https://company8.dev.zoolwork.com/swagger/index.html"
    print(f"\nNavigating to {comp_swagger_url}...")
    page.goto(comp_swagger_url, wait_until="networkidle", timeout=30000)
    time.sleep(2)

    auth_btn = page.locator("button.btn.authorize")
    if auth_btn.count() > 0:
        print("Clicking Authorize button in Company8 Swagger...")
        auth_btn.first.click()
        time.sleep(1)

        token_input = page.locator("div.modal-ux input[type='text']")
        if token_input.count() > 0:
            token_input.first.fill(f"Bearer {access_token}")
            time.sleep(0.5)

            modal_auth_btn = page.locator("div.modal-ux button.btn.modal-btn.auth")
            if modal_auth_btn.count() > 0:
                modal_auth_btn.first.click()
                time.sleep(1)

            close_btn = page.locator("div.modal-ux button.btn.modal-btn.btn-done")
            if close_btn.count() > 0:
                close_btn.first.click()
                time.sleep(1)

    screenshot_comp_path = "scratch/swagger_company8_authorized.png"
    page.screenshot(path=screenshot_comp_path, full_page=False)
    print(f"Screenshot saved to {screenshot_comp_path}")

    browser.close()
    print("\nPlaywright Swagger connection setup complete!")

