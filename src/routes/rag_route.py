from fastapi import APIRouter, Depends, HTTPException
from src.config.schema import AskQuestionRequest
from src.services.rag_service import RAGService
from src.services.dependencies import get_rag_service
from loguru import logger
import time

rag_router = APIRouter(
    prefix="/v1",
    tags=["Legal RAG"]
)


@rag_router.post("/ask")
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
        answer = await rag_service.ask_question(
            request.question
        )

        elapsed = time.perf_counter() - start
        logger.info(f"Question processed in {elapsed:.2f}s")

        return {
            "question": request.question,
            "rag_response": answer["answer"]
        }

    except Exception:
        logger.exception("Failed to process question")
    raise HTTPException(
        status_code=500,
        detail="Internal server error"
    )
