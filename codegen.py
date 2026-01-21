from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        channel="chrome",   # <-- real Chrome (stealth)
        args=["--disable-blink-features=AutomationControlled"]
    )

    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.swiggy.com")

    print("Inspector starting... perform actions in the browser.")
    page.pause()  # <-- Open full inspector (codegen UI)
