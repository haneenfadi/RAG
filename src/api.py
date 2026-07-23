import os
import chromadb
from fastapi import FastAPI
from sentence_transformers import CrossEncoder, SentenceTransformer
from src.routes.health import health_router
from src.routes.rag_route import rag_router
from groq import AsyncGroq
from src.config.settings import Settings

app = FastAPI(title="Legal RAG API",
              description="API for Legal RAG",
              root_path="/legal/api"
              )


@app.on_event("startup")
async def startup():
    app.state.embedding_model = SentenceTransformer(
        "intfloat/multilingual-e5-base")
    app.state.chromadb = chromadb.PersistentClient(
        path="src/embedding/chroma_db")
    app.state.collection = app.state.chromadb.get_collection("legal_rag")
    app.state.groq_client = AsyncGroq(api_key=Settings.groq_api_key)
    app.state.reranker_model = CrossEncoder(
        "BAAI/bge-reranker-v2-m3",    device="cpu"
        # "BAAI/bge-reranker-base"
    )


app.include_router(health_router)
app.include_router(rag_router)
