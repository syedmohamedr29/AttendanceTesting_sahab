import json
import time
import shutil
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token_info = json.load(f)

token = token_info["access_token"]
company_id = "3a247435-e31d-ef15-8cc9-62c587f4eb3f"

print("Starting capture for Negative Break Duration (DEFECT-20261027-04)...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1400, "height": 1100})
    page = context.new_page()

    url = "https://attendance2.dev.zoolwork.com/swagger/index.html"
    page.goto(url, wait_until="domcontentloaded")
    time.sleep(3)

    # Click Authorize
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

    op_br = page.locator("#operations-Attendance_Policies-post_api_companies__companyId__attpolicies_break")
    if op_br.count() > 0:
        op_br.scroll_into_view_if_needed()
        time.sleep(1)
        op_br.locator(".opblock-summary").click()
        time.sleep(1)

        try_btn = op_br.locator("button.try-out__btn")
        if try_btn.count() > 0 and "cancel" not in try_btn.inner_text().lower():
            try_btn.click()
            time.sleep(1)

        cid_input = op_br.locator("input[placeholder='companyId']")
        if cid_input.count() > 0:
            cid_input.fill(company_id)

        body_textarea = op_br.locator("textarea.body-param__text")
        if body_textarea.count() > 0:
            neg_break_json = json.dumps({
                "name": {"en": "Negative Break Defect Proof UI"},
                "breakDeduction": 1,
                "breaks": [
                    {"name": "Lunch Break Negative", "type": 1, "durationMinutes": -60}
                ],
                "isActive": True
            }, indent=2)
            body_textarea.fill(neg_break_json)
            time.sleep(0.5)

        execute_btn = op_br.locator("button.execute")
        if execute_btn.count() > 0:
            execute_btn.click()
            time.sleep(4)

        op_br.scroll_into_view_if_needed()
        time.sleep(1)
        ss = "defect_evidence/evidence_10_negative_break_accepted_200.png"
        op_br.screenshot(path=ss)
        print(f"   Saved Evidence to {ss}")
        shutil.copyfile(ss, r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\evidence_10_negative_break_accepted_200.png")

    browser.close()
    print("Done!")

