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

print("Starting Playwright capture for remaining Part 2 evidence...")

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
        print("   Authorized in Swagger!")

    # 1. Capture DEFECT-20261027-01: Missing locationId in POST /workplans -> HTTP 400
    print("\n1. Executing & Capturing DEFECT-20261027-01 (WorkPlans missing locationId)...")
    op_wp = page.locator("#operations-Work_Plans-post_api_companies__companyId__workplans")
    if op_wp.count() > 0:
        op_wp.scroll_into_view_if_needed()
        time.sleep(1)
        op_wp.locator(".opblock-summary").click()
        time.sleep(1)

        try_btn = op_wp.locator("button.try-out__btn")
        if try_btn.count() > 0 and "cancel" not in try_btn.inner_text().lower():
            try_btn.click()
            time.sleep(1)

        cid_input = op_wp.locator("input[placeholder='companyId']")
        if cid_input.count() > 0:
            cid_input.fill(company_id)

        # Leave locationId parameter empty!
        body_textarea = op_wp.locator("textarea.body-param__text")
        if body_textarea.count() > 0:
            wp_json = json.dumps({
                "workPlanName": {"en": "Test Plan Missing Loc"},
                "year": 2026
            }, indent=2)
            body_textarea.fill(wp_json)
            time.sleep(0.5)

        execute_btn = op_wp.locator("button.execute")
        if execute_btn.count() > 0:
            execute_btn.click()
            time.sleep(4)

        op_wp.scroll_into_view_if_needed()
        time.sleep(1)
        ss1 = "defect_evidence/evidence_11_workplan_missing_locationid_400.png"
        op_wp.screenshot(path=ss1)
        print(f"   Saved Evidence 11 to {ss1}")
        shutil.copyfile(ss1, r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\evidence_11_workplan_missing_locationid_400.png")

    # 2. Capture DEFECT-20261027-07: Calendar days sum != 7 -> HTTP 500
    print("\n2. Executing & Capturing DEFECT-20261027-07 (Calendar Invariant 6+2=8)...")
    op_fx = page.locator("#operations-Work_Templates-post_api_companies__companyId__worktemplates_fixed")
    if op_fx.count() > 0:
        op_fx.scroll_into_view_if_needed()
        time.sleep(1)
        op_fx.locator(".opblock-summary").click()
        time.sleep(1)

        try_btn = op_fx.locator("button.try-out__btn")
        if try_btn.count() > 0 and "cancel" not in try_btn.inner_text().lower():
            try_btn.click()
            time.sleep(1)

        cid_input = op_fx.locator("input[placeholder='companyId']")
        if cid_input.count() > 0:
            cid_input.fill(company_id)

        body_textarea = op_fx.locator("textarea.body-param__text")
        if body_textarea.count() > 0:
            cal_json = json.dumps({
                "templateName": {"en": "Invariant 8 Days Proof"},
                "shortCode": "INV8D",
                "totalWorkDurationInMinutes": 2880,
                "totalWorkingDays": 6,
                "totalDaysOff": 2,
                "fixedTimeSlots": [
                    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480}]},
                    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480}]},
                    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480}]},
                    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480}]},
                    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480}]},
                    {"dayEnum": 6, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480}]},
                    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0, "timeSlots": []}
                ]
            }, indent=2)
            body_textarea.fill(cal_json)
            time.sleep(0.5)

        execute_btn = op_fx.locator("button.execute")
        if execute_btn.count() > 0:
            execute_btn.click()
            time.sleep(4)

        op_fx.scroll_into_view_if_needed()
        time.sleep(1)
        ss2 = "defect_evidence/evidence_12_calendar_sum_not_7_500_validation_exception.png"
        op_fx.screenshot(path=ss2)
        print(f"   Saved Evidence 12 to {ss2}")
        shutil.copyfile(ss2, r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\evidence_12_calendar_sum_not_7_500_validation_exception.png")

    browser.close()
    print("Done capturing remaining evidence!")

