# python -m src.main
from src.config.settings import settings
import src.utils.fetcher as f
import src.utils.web_scraber as s
import src.utils.pdf_extractor as p


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
