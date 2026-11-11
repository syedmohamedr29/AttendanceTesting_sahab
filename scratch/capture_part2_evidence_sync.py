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

print("Starting Playwright capture for Part 2 defect evidence...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1400, "height": 1100})
    page = context.new_page()

    url = "https://attendance2.dev.zoolwork.com/swagger/index.html"
    print(f"1. Navigating to {url}...")
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

    # ----------------------------------------------------------------------------------
    # Capture Evidence 1: Negative Grace Period Accepted with 200 OK
    # ----------------------------------------------------------------------------------
    print("\n2. Executing & Capturing DEFECT-20261027-03 (Negative Grace Minutes)...")
    op_gp = page.locator("#operations-Attendance_Policies-post_api_companies__companyId__attpolicies_graceperiod")
    if op_gp.count() > 0:
        op_gp.scroll_into_view_if_needed()
        time.sleep(1)
        op_gp.locator(".opblock-summary").click()
        time.sleep(1)

        try_btn = op_gp.locator("button.try-out__btn")
        if try_btn.count() > 0 and "cancel" not in try_btn.inner_text().lower():
            try_btn.click()
            time.sleep(1)

        cid_input = op_gp.locator("input[placeholder='companyId']")
        if cid_input.count() > 0:
            cid_input.fill(company_id)

        body_textarea = op_gp.locator("textarea.body-param__text")
        if body_textarea.count() > 0:
            neg_grace_json = json.dumps({
                "name": {"en": "Negative Grace Defect Proof UI"},
                "lateCheckInGraceMinutes": -15,
                "earlyCheckOutGraceMinutes": -10,
                "deviationPeriod": 1,
                "deviationThreshold": 3,
                "deductLeaveFrom": 1,
                "deductionDays": 1,
                "isActive": True
            }, indent=2)
            body_textarea.fill(neg_grace_json)
            time.sleep(0.5)

        execute_btn = op_gp.locator("button.execute")
        if execute_btn.count() > 0:
            execute_btn.click()
            time.sleep(4)

        op_gp.scroll_into_view_if_needed()
        time.sleep(1)
        ss1 = "defect_evidence/evidence_08_negative_grace_accepted_200.png"
        op_gp.screenshot(path=ss1)
        print(f"   Saved Evidence 1 to {ss1}")
        shutil.copyfile(ss1, r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\evidence_08_negative_grace_accepted_200.png")

    # ----------------------------------------------------------------------------------
    # Capture Evidence 2: Split Overlap HTTP 500 ValidationException
    # ----------------------------------------------------------------------------------
    print("\n3. Executing & Capturing DEFECT-20261027-06 (Split Overlap HTTP 500)...")
    op_split = page.locator("#operations-Work_Templates-post_api_companies__companyId__worktemplates_split")
    if op_split.count() > 0:
        op_split.scroll_into_view_if_needed()
        time.sleep(1)
        op_split.locator(".opblock-summary").click()
        time.sleep(1)

        try_btn = op_split.locator("button.try-out__btn")
        if try_btn.count() > 0 and "cancel" not in try_btn.inner_text().lower():
            try_btn.click()
            time.sleep(1)

        cid_input = op_split.locator("input[placeholder='companyId']")
        if cid_input.count() > 0:
            cid_input.fill(company_id)

        body_textarea = op_split.locator("textarea.body-param__text")
        if body_textarea.count() > 0:
            overlap_json = json.dumps({
                "templateName": {"en": "Split Overlap Proof UI"},
                "shortCode": "SPLOV3",
                "totalWorkDurationInMinutes": 480,
                "totalWorkingDays": 5,
                "totalDaysOff": 2,
                "splitTimeSlots": [
                    {
                        "dayEnum": 1,
                        "isWorkingDay": True,
                        "recurrenceOfMonth": [1,2,3,4,5],
                        "workDurationInMinutes": 480,
                        "noOfInterval": 2,
                        "timeSlots": [
                            {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
                            {"startTime": "11:00", "endTime": "15:00", "workDurationInMinutes": 240}
                        ]
                    },
                    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "13:00", "endTime": "17:00", "workDurationInMinutes": 240}]},
                    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "13:00", "endTime": "17:00", "workDurationInMinutes": 240}]},
                    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "13:00", "endTime": "17:00", "workDurationInMinutes": 240}]},
                    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "13:00", "endTime": "17:00", "workDurationInMinutes": 240}]},
                    {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0, "noOfInterval": 0, "timeSlots": []},
                    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0, "noOfInterval": 0, "timeSlots": []}
                ]
            }, indent=2)
            body_textarea.fill(overlap_json)
            time.sleep(0.5)

        execute_btn = op_split.locator("button.execute")
        if execute_btn.count() > 0:
            execute_btn.click()
            time.sleep(4)

        op_split.scroll_into_view_if_needed()
        time.sleep(1)
        ss2 = "defect_evidence/evidence_09_split_overlap_500_validation_exception.png"
        op_split.screenshot(path=ss2)
        print(f"   Saved Evidence 2 to {ss2}")
        shutil.copyfile(ss2, r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\evidence_09_split_overlap_500_validation_exception.png")

    browser.close()
    print("All Playwright evidence captured successfully!")

