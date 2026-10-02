import secrets
from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from src.config.schema import AskQuestionRequest, AskQuestionResponse
from src.services.rag_service import RAGService
from src.services.dependencies import get_rag_service
from loguru import logger
import time
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY is not set in .env")

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(key: str | None = Security(api_key_header)):
    # compare_digest avoids timing attacks
    if not key or not secrets.compare_digest(key, API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )

rag_router = APIRouter(
    prefix="/v1",
    tags=["Legal RAG"],
    dependencies=[Depends(verify_api_key)],
)


@rag_router.post("/ask", response_model=AskQuestionResponse)
async def ask_question(
    request: AskQuestionRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Endpoint to ask a question to the Legal RAG system.
    """
    start = time.perf_counter()

    logger.info(
        f"Received question: {request.question}"
    )
    try:
        result = await rag_service.ask_question(
            request.question
        )

        elapsed = time.perf_counter() - start
        logger.info(f"Question processed in {elapsed:.2f}s")

        return AskQuestionResponse(
            question=request.question,
            rag_response=result["answer"],
        )

    except Exception:
        logger.exception("Failed to process question")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
