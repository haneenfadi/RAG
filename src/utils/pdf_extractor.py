# # python -m src.utils.pdf_extractor
# import fitz  # using PyMuPDF
# from src.config.settings import settings
# import json


# def extract_text_from_pdf():
#     pages = []
#     doc = fitz.open(settings.pdf["pdf_1"])
#     text = ""
#     for page_num, page in enumerate(doc, start=1):
#         blocks = page.get_text("blocks")

#         blocks.sort(key=lambda b: (b[1], b[0]))

#         text = "\n".join([b[4] for b in blocks if b[4].strip()])

#         pages.append({
#             "page_number": page_num,
#             "text": text})

#     return {
#         "source": settings.pdf["pdf_1"],
#         "type": "pdf",
#         "pages": pages
#     }


# print(extract_text_from_pdf())

# with open("src/data/extracted/old_pdf_extracted.json", "w", encoding="utf-8") as f:
#     json.dump(extract_text_from_pdf(), f, ensure_ascii=False, indent=4)

import re
import unicodedata
import pypdfium2 as pdfium
from src.config.settings import settings
import json

# تشكيل + تطويل + علامة الدائرة المنقطة (◌)
_STRIP = re.compile(r"[\u0640\u064B-\u065F\u0670\u25CC]")
# رموز اتجاه مخفية
_BIDI = re.compile(r"[\u200E\u200F\u202A-\u202E\u2066-\u2069]")
# أرقام/لاتيني
_LTR = re.compile(r"[0-9A-Za-z]")

LINE_TOL = 5.0    # أقصى فرق ارتفاع لحرفين بنفس السطر
SPACE_TOL = 12.0  # المسافات ارتفاعها مختلف شوي عن الحروف
GAP_MIN = 2.0     # فراغ بين حرفين عربيين بدون مسافة => نحط مسافة


def _is_ar(c: str) -> bool:
    return c.isalpha() and not _LTR.match(c)


def _norm(c: str) -> str:
    return _BIDI.sub("", unicodedata.normalize("NFKC", c))


def _fix_ltr_runs(s: str) -> str:
    out, run = [], []
    for ch in s:
        if _LTR.match(ch):
            run.append(ch)
        else:
            if run:
                out.append("".join(reversed(run)))
                run = []
            out.append(ch)
    if run:
        out.append("".join(reversed(run)))
    return "".join(out)


def _page_text(page) -> str:
    tp = page.get_textpage()
    glyphs, spaces = [], []  # (char, left, right, y_center)

    count = tp.count_chars()
    for i in range(count):
        raw = tp.get_text_range(i, 1)
        if not raw or raw in "\r\n\x00":
            continue

        c = _norm(raw)
        if not c or _STRIP.fullmatch(c):
            continue

        l, b, r, t = tp.get_charbox(i)
        y_center = (b + t) / 2.0
        item = (c, l, r, y_center)

        if c.isspace():
            spaces.append(item)
        else:
            glyphs.append(item)

    if not glyphs:
        return ""

    # 1) ترتيب الأسطر عموديًا (من الأعلى إلى الأسفل)
    glyphs.sort(key=lambda x: -x[3])
    lines = []  # [mean_y, [items]]

    for g in glyphs:
        if lines and abs(g[3] - lines[-1][0]) <= LINE_TOL:
            lines[-1][1].append(g)
            ys = [x[3] for x in lines[-1][1]]
            lines[-1][0] = sum(ys) / len(ys)
        else:
            lines.append([g[3], [g]])

    # 2) ربط المسافات بأقرب سطر
    for s in spaces:
        if not lines:
            break
        best = min(lines, key=lambda ln: abs(ln[0] - s[3]))
        if abs(best[0] - s[3]) <= SPACE_TOL:
            best[1].append(s)

    # 3) ترتيب كل سطر من اليمين إلى اليسار + معالجة الفراغات
    out = []
    for _, items in lines:
        items.sort(key=lambda x: -((x[1] + x[2]) / 2.0))
        buf, prev, seen_space = [], None, False

        for c, l, r, _y in items:
            if c.isspace():
                seen_space = True
                continue
            if seen_space:
                buf.append(" ")
            elif (prev is not None and _is_ar(prev[0]) and _is_ar(c)
                  and (prev[1] - r) > GAP_MIN):
                buf.append(" ")  # مسافة ناقصة بين مقطعين

            buf.append(c)
            prev, seen_space = (c, l), False

        s = _fix_ltr_runs("".join(buf))
        s = re.sub(r"[ \t]+", " ", s).strip()
        if s:
            out.append(s)

    return "\n".join(out)


def extract_text_from_pdf(pdf_path: str) -> dict:
    doc = pdfium.PdfDocument(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        pages.append({
            "page_number": i + 1,
            "text": _page_text(page)
        })
    doc.close()
    return {"source": pdf_path, "pages": pages}


pdf_file = settings.pdf["pdf_1"]


with open("src/data/extracted/pdf_extracted.json", "w", encoding="utf-8") as f:
    json.dump(extract_text_from_pdf(pdf_file), f, ensure_ascii=False, indent=4)
