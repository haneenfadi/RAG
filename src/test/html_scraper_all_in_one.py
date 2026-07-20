from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json

url = "https://www.ssc.gov.jo/%D8%A3%D8%B3%D8%A6%D9%84%D8%A9-%D8%B9%D8%A7%D9%85%D8%A9/"


def scrape_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")

        html = page.content()
        browser.close()

        # parse
        soup = BeautifulSoup(html, "html.parser")
        content = soup.select(".elementor-accordion-item")

        if content:

            all_text = []
            for item in content:
                text = item.get_text(separator="\n", strip=True)
                all_text.append(text)

        else:
            text = "NOT FOUND"

        return {
            "text": all_text,
            "metadata": {
                "source": "ssc.gov.jo",
                "type": "law",
                "language": "ar"
            }
        }


scraped_data = scrape_page(url)

with open("src/data/extracted/social_security_faq.json", "w", encoding="utf-8") as f:
    json.dump(scraped_data, f, ensure_ascii=False, indent=4)
