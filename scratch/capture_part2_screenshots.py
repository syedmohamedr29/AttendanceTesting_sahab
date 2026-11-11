import asyncio
from playwright.async_api import async_playwright
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token_data = json.load(f)

token = token_data["access_token"]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1400, "height": 1000})
        page = await context.new_page()

        print("1. Navigating to Swagger Attendance 2...")
        await page.goto("https://attendance2.dev.zoolwork.com/swagger/index.html", wait_until="domcontentloaded")
        await page.wait_for_selector(".btn.authorize", timeout=15000)

        # Authorize
        print("2. Authorizing in Swagger...")
        await page.click(".btn.authorize")
        await page.wait_for_selector("input[aria-label='auth-bearer-value']", timeout=5000)
        await page.fill("input[aria-label='auth-bearer-value']", f"Bearer {token}")
        await page.click(".modal-ux-inner .btn-done")
        await page.click(".btn-done")
        print("   Authorized!")

        # Expand POST /api/companies/{companyId}/attpolicies/graceperiod
        print("3. Expanding POST /attpolicies/graceperiod...")
        op_sel = "#operations-AttendancePolicies-post_api_companies__companyId__attpolicies_graceperiod"
        await page.wait_for_selector(op_sel, timeout=10000)
        await page.click(f"{op_sel} .opblock-summary")
        await page.wait_for_selector(f"{op_sel} .try-out__btn", timeout=5000)
        await page.click(f"{op_sel} .try-out__btn")

        # Fill companyId
        await page.fill(f"{op_sel} input[placeholder='companyId']", "3a247435-e31d-ef15-8cc9-62c587f4eb3f")

        # Fill body with negative grace minutes
        neg_grace_body = json.dumps({
            "name": {"en": "Negative Grace Test Policy UI"},
            "lateCheckInGraceMinutes": -15,
            "earlyCheckOutGraceMinutes": -10,
            "deviationPeriod": 1,
            "deviationThreshold": 3,
            "deductLeaveFrom": 1,
            "deductionDays": 1,
            "isActive": True
        }, indent=2)
        await page.fill(f"{op_sel} textarea.body-param__text", neg_grace_body)

        # Click Execute
        print("4. Executing in Swagger...")
        await page.click(f"{op_sel} .execute")
        await page.wait_for_selector(f"{op_sel} .live-responses-table", timeout=15000)
        await page.wait_for_timeout(2000)

        # Scroll opblock into view
        el = await page.query_selector(op_sel)
        if el:
            await el.scroll_into_view_if_needed()
            await page.wait_for_timeout(1000)
            ss_path1 = "defect_evidence/evidence_08_negative_grace_accepted_200.png"
            await el.screenshot(path=ss_path1)
            print(f"Saved screenshot: {ss_path1}")

        await browser.close()
        print("Finished successfully!")

asyncio.run(main())

