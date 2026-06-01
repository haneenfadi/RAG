from playwright.sync_api import sync_playwright


def fetch_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url)

        page.wait_for_selector("p.DraftDetails")

        html = page.content()
        browser.close()

    return html
