# python -m src.utils.pdf_extractor
import fitz  # using PyMuPDF
from src.config.settings import settings
import json


def extract_text_from_pdf():
    pages = []
    doc = fitz.open(settings.pdf["pdf_1"])
    text = ""
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("blocks")

        blocks.sort(key=lambda b: (b[1], b[0]))

        text = "\n".join([b[4] for b in blocks if b[4].strip()])

        pages.append({
            "page_number": page_num,
            "text": text})

    return {
        "source": settings.pdf["pdf_1"],
        "type": "pdf",
        "pages": pages
    }


print(extract_text_from_pdf())

with open("src/data/extracted/pdf_extracted.json", "w", encoding="utf-8") as f:
    json.dump(extract_text_from_pdf(), f, ensure_ascii=False, indent=4)
