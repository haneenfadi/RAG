from pydantic import BaseModel


class HTMLScrapeResult(BaseModel):
    source: str
    type: str
    language: str
    text: str


class PDFPage(BaseModel):
    page_num: int
    text: str


class PDFExtractResult(BaseModel):
    source: str
    type: str
    language: str
    pages: list[PDFPage]
