from playwright.sync_api import sync_playwright

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print("Playwright Chromium launched successfully!")
        browser.close()
except Exception as e:
    print("Playwright launch error:", str(e))

