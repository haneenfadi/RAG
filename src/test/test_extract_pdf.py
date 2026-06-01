import fitz  # using PyMuPDF
from src.config.settings import settings

doc = fitz.open(settings.pdf["pdf_1"])

with open("src/test/outputs/pymupdf_output_TEXT_PRESERVE_LIGATURES.txt", "w", encoding="utf-8") as f:
    for page in doc:
        text = page.get_text(
            "text", flags=fitz.TEXT_PRESERVE_LIGATURES, sort=True)
        f.write(text + "\n\n")


with open("src/test/outputs/pymupdf_output_just_sort.txt", "w", encoding="utf-8") as f:
    for page in doc:
        text = page.get_text("text", sort=True)
        f.write(text + "\n\n")

with open("src/test/outputs/pymupdf_output_without_anything.txt", "w", encoding="utf-8") as f:
    for page in doc:
        text = page.get_text("text", sort=True)
        f.write(text + "\n\n")

with open("src/test/outputs/pymupdf_output_blocks.txt", "w", encoding="utf-8") as f:
    for page in doc:
        blocks = page.get_text("blocks")
        blocks.sort(key=lambda b: (b[1], b[0]))

        text = "\n".join([b[4] for b in blocks if b[4].strip()])
        f.write(text + "\n\n")
