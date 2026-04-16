from playwright.sync_api import sync_playwright

def fill_web_form(data):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://example.com")

        try:
            page.fill("input[name='name']", data.get("name", ""))
            page.fill("input[name='email']", data.get("email", ""))
            page.fill("input[name='age']", data.get("age", ""))
            page.fill("input[name='city']", data.get("city", ""))
        except Exception as e:
            print("Error:", e)

        page.wait_for_timeout(3000)
        browser.close()