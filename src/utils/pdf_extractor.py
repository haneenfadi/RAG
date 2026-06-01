import fitz  # using PyMuPDF
from config.settings import settings


def extract_text_from_pdf():
    doc = fitz.open(settings.pdf["pdf_1"])
    text = ""
    for page in doc:
        blocks = page.get_text("blocks")
        blocks.sort(key=lambda b: (b[1], b[0]))

        text = "\n".join([b[4] for b in blocks if b[4].strip()])

        return text+"\n\n"
