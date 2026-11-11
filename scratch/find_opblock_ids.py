import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://attendance2.dev.zoolwork.com/swagger/index.html", wait_until="domcontentloaded")
    time.sleep(3)
    
    # find all opblocks
    opblock_ids = page.eval_on_selector_all(".opblock", "elements => elements.map(e => e.id)")
    print(f"Total opblocks found: {len(opblock_ids)}")
    for op_id in opblock_ids:
        if "grace" in op_id.lower() or "split" in op_id.lower():
            print("MATCH:", op_id)
            
    browser.close()

