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


class AskQuestionRequest(BaseModel):
    question: str


class Source(BaseModel):
    source: str
    reference: str


class RagResponse(BaseModel):
    answer: str
    sources: list[Source] = []


class AskQuestionResponse(BaseModel):
    question: str
    rag_response: RagResponse
