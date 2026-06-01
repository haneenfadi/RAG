from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

url = "https://www.lob.gov.jo/?v=1&lang=ar#!/DraftDetails?DraftID=10760"


def scrape_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url)

        page.wait_for_selector("p.DraftDetails")

        html = page.content()
        browser.close()

    # parse
    soup = BeautifulSoup(html, "html.parser")
    with open("src/data/raw/scrape_page_html.html", "w", encoding="utf-8") as f:
        f.write(html)
    content = soup.select_one("p.DraftDetails")

    if content:
        text = content.get_text(separator="\n")
    else:
        text = "NOT FOUND"

    return {
        "text": text,
        "metadata": {
            "source": "lob.gov.jo",
            "type": "law",
            "language": "ar"
        }
    }


scraped_data = scrape_page(url)

with open("src/test/outputs/scrape_page_output.txt", "w", encoding="utf-8") as f:
    f.write(str(scraped_data))
