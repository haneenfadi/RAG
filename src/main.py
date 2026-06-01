import utils.fetcher as f
import utils.web_scraber as s
from config.settings import settings
import utils.pdf_extractor as p


def parse_pdf():
    text = p.extract_text_from_pdf()
    print(text)


def scrape_web():
    html = f.fetch_page(settings.url["lob"])
    result = s.parse_lob(html)
    print(result)


def main():
    parse_pdf()
    scrape_web()


main()
