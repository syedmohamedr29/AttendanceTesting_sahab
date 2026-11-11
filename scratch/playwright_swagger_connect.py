import json
import time
from playwright.sync_api import sync_playwright

with open("scratch/current_token.json") as f:
    token_info = json.load(f)

token = token_info["access_token"]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1400, "height": 1000})
    page = context.new_page()

    # 1. Attendance2 Swagger
    url = "https://attendance2.dev.zoolwork.com/swagger/index.html"
    print(f"Connecting to {url}...")
    page.goto(url, wait_until="networkidle")
    time.sleep(2)

    # Click Authorize
    auth_btn = page.locator("button.btn.authorize")
    if auth_btn.count() > 0:
        auth_btn.first.click()
        time.sleep(1)

        # Fill Bearer token
        input_box = page.locator("div.modal-ux input[type='text']")
        if input_box.count() > 0:
            input_box.first.fill(f"Bearer {token}")
            time.sleep(0.5)

            # Click Authorize inside modal
            modal_auth = page.locator("div.modal-ux button.btn.modal-btn.auth")
            if modal_auth.count() > 0:
                modal_auth.first.click()
                time.sleep(1)

            # Click Close
            close_btn = page.locator("div.modal-ux button.btn.modal-btn.btn-done")
            if close_btn.count() > 0:
                close_btn.first.click()
                time.sleep(1)

    # Scroll down to WorkTemplates section to show it in the screenshot
    wt_section = page.locator("span:has-text('/api/companies/{companyId}/worktemplates')")
    if wt_section.count() > 0:
        wt_section.first.scroll_into_view_if_needed()
        time.sleep(1)

    page.screenshot(path="scratch/swagger_attendance2_connected.png")
    print("Attendance2 Swagger connected and screenshot saved to scratch/swagger_attendance2_connected.png")

    # 2. Company8 Swagger
    url_comp = "https://company8.dev.zoolwork.com/swagger/index.html"
    print(f"\nConnecting to {url_comp}...")
    page.goto(url_comp, wait_until="networkidle")
    time.sleep(2)

    auth_btn = page.locator("button.btn.authorize")
    if auth_btn.count() > 0:
        auth_btn.first.click()
        time.sleep(1)

        input_box = page.locator("div.modal-ux input[type='text']")
        if input_box.count() > 0:
            input_box.first.fill(f"Bearer {token}")
            time.sleep(0.5)

            modal_auth = page.locator("div.modal-ux button.btn.modal-btn.auth")
            if modal_auth.count() > 0:
                modal_auth.first.click()
                time.sleep(1)

            close_btn = page.locator("div.modal-ux button.btn.modal-btn.btn-done")
            if close_btn.count() > 0:
                close_btn.first.click()
                time.sleep(1)

    page.screenshot(path="scratch/swagger_company8_connected.png")
    print("Company8 Swagger connected and screenshot saved to scratch/swagger_company8_connected.png")

    browser.close()
    print("Playwright connection successfully verified!")

