from itertools import count

from playwright.sync_api import sync_playwright


def fetch_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")

        html = page.content()
        browser.close()

    return html
