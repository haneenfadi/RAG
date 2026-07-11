import fitz  # using PyMuPDF
from src.config.settings import settings


def extract_text_from_pdf():
    pages = []
    doc = fitz.open(settings.pdf["pdf_1"])
    text = ""
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("blocks")
        for i, b in enumerate(blocks):
            print("BLOCK", i)
            print("x0:", b[0])
            print("y0:", b[1])
            print("x1:", b[2])
            print("y1:", b[3])
            print("text:", repr(b[4]))
            print("block_no:", b[5])
            print("type:", b[6])
            print("-" * 40)

        blocks.sort(key=lambda b: (b[1], b[0]))

        text = "\n".join([b[4] for b in blocks if b[4].strip()])

        pages.append({
            "page_number": page_num,
            "text": text})

    return {
        "source": settings.pdf["pdf_1"],
        "pages": pages
    }


print(extract_text_from_pdf())
