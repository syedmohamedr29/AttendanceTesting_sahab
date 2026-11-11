import json
import time
import shutil
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token_info = json.load(f)

token = token_info["access_token"]
att4_id = "3a247436-8669-844a-7d2f-1a209af02d8e"
active_v2_id = "53470658-5f9b-47b4-b254-f96b9501401c"

print("Starting Playwright capture for Attendance 4 evidence...")

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

    # ----------------------------------------------------------------------------------
    # Evidence 13: USER-08 (One Default Rule Cit.Attendance:1010 on Attendance 4)
    # ----------------------------------------------------------------------------------
    print("\n1. Capturing Evidence 13: USER-08 (POST /fixed on Attendance 4 -> 1010)...")
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
            cid_input.fill(att4_id)

        body_textarea = op_fx.locator("textarea.body-param__text")
        if body_textarea.count() > 0:
            fix_json = json.dumps({
                "templateName": {"en": "Second CDWT Attempt"},
                "shortCode": "ATT4FIX2",
                "totalWorkDurationInMinutes": 2400,
                "totalWorkingDays": 5,
                "totalDaysOff": 2,
                "fixedTimeSlots": [
                    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480}]},
                    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480}]},
                    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480}]},
                    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480}]},
                    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480}]},
                    {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0, "timeSlots": []},
                    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0, "timeSlots": []}
                ]
            }, indent=2)
            body_textarea.fill(fix_json)
            time.sleep(0.5)

        execute_btn = op_fx.locator("button.execute")
        if execute_btn.count() > 0:
            execute_btn.click()
            time.sleep(4)

        op_fx.scroll_into_view_if_needed()
        time.sleep(1)
        ss1 = "defect_evidence/evidence_13_att4_one_default_guard_1010.png"
        op_fx.screenshot(path=ss1)
        print(f"   Saved Evidence 13 to {ss1}")
        shutil.copyfile(ss1, r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\evidence_13_att4_one_default_guard_1010.png")

    # ----------------------------------------------------------------------------------
    # Evidence 14: USER-21 (PATCH shortCode Locked Cit.Attendance:1107 on Attendance 4)
    # ----------------------------------------------------------------------------------
    print("\n2. Capturing Evidence 14: USER-21 (PATCH flexi shortCode locked)...")
    op_flx_patch = page.locator("#operations-Work_Templates-patch_api_companies__companyId__worktemplates_flexi__id_")
    if op_flx_patch.count() > 0:
        op_flx_patch.scroll_into_view_if_needed()
        time.sleep(1)
        op_flx_patch.locator(".opblock-summary").click()
        time.sleep(1)

        try_btn = op_flx_patch.locator("button.try-out__btn")
        if try_btn.count() > 0 and "cancel" not in try_btn.inner_text().lower():
            try_btn.click()
            time.sleep(1)

        cid_input = op_flx_patch.locator("input[placeholder='companyId']")
        if cid_input.count() > 0:
            cid_input.fill(att4_id)

        id_input = op_flx_patch.locator("input[placeholder='id']")
        if id_input.count() > 0:
            id_input.fill(active_v2_id)

        body_textarea = op_flx_patch.locator("textarea.body-param__text")
        if body_textarea.count() > 0:
            patch_json = json.dumps({
                "templateName": {"en": "Attendance 4 Flexi Renamed"},
                "shortCode": "HACKCODE",
                "totalWorkDurationInMinutes": 480,
                "totalWorkingDays": 5,
                "totalDaysOff": 2,
                "flexibleType": 1,
                "flexiTimeSlots": [
                    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480},
                    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480},
                    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480},
                    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480},
                    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480},
                    {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0},
                    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0}
                ]
            }, indent=2)
            body_textarea.fill(patch_json)
            time.sleep(0.5)

        execute_btn = op_flx_patch.locator("button.execute")
        if execute_btn.count() > 0:
            execute_btn.click()
            time.sleep(4)

        op_flx_patch.scroll_into_view_if_needed()
        time.sleep(1)
        ss2 = "defect_evidence/evidence_14_att4_patch_shortcode_locked_1107.png"
        op_flx_patch.screenshot(path=ss2)
        print(f"   Saved Evidence 14 to {ss2}")
        shutil.copyfile(ss2, r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\evidence_14_att4_patch_shortcode_locked_1107.png")

    # ----------------------------------------------------------------------------------
    # Evidence 15: USER-22 (PATCH empty payload {} -> HTTP 500 ValidationException)
    # ----------------------------------------------------------------------------------
    print("\n3. Capturing Evidence 15: USER-22 (PATCH empty body {} -> HTTP 500)...")
    if op_flx_patch.count() > 0:
        body_textarea = op_flx_patch.locator("textarea.body-param__text")
        if body_textarea.count() > 0:
            body_textarea.fill("{}")
            time.sleep(0.5)

        execute_btn = op_flx_patch.locator("button.execute")
        if execute_btn.count() > 0:
            execute_btn.click()
            time.sleep(4)

        op_flx_patch.scroll_into_view_if_needed()
        time.sleep(1)
        ss3 = "defect_evidence/evidence_15_att4_patch_empty_payload_500.png"
        op_flx_patch.screenshot(path=ss3)
        print(f"   Saved Evidence 15 to {ss3}")
        shutil.copyfile(ss3, r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\evidence_15_att4_patch_empty_payload_500.png")

    browser.close()
    print("All Attendance 4 Playwright screenshots captured successfully!")

