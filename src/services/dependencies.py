from fastapi import Request
from src.services.rag_service import RAGService


def get_rag_service(request: Request):

    return RAGService(
        embedding_model=request.app.state.embedding_model,
        collection=request.app.state.collection,
        groq_client=request.app.state.groq_client,
        reranker_model=request.app.state.reranker_model
    )
