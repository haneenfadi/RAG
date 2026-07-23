from src.services.llm_service import generate_answer
from src.services.retrieval_service import retrieve_context
from src.services.embedding_service import embed_query
import time
from loguru import logger


class RAGService:

    def __init__(
        self,
        embedding_model,
        collection,
        groq_client,
        reranker_model,
    ):
        self.embedding_model = embedding_model
        self.collection = collection
        self.groq_client = groq_client
        self.reranker_model = reranker_model

    async def ask_question(self, question: str):
        start = time.perf_counter()

        # embedding
        t1 = time.perf_counter()

        embedding = embed_query(
            self.embedding_model,
            question
        )

        # retrieval
        t2 = time.perf_counter()

        context = retrieve_context(
            self.collection,
            question,
            embedding,
            self.reranker_model
        )
        # answer generation
        t3 = time.perf_counter()

        answer = await generate_answer(
            context,
            question,
            self.groq_client
        )

        t4 = time.perf_counter()

        logger.info(f"Embedding: {t1-start:.2f}s")
        logger.info(f"Retrieval + Reranker: {t3-t2:.2f}s")
        logger.info(f"LLM: {t4-t3:.2f}s")

        return {
            "answer": answer,
            "sources": context
        }
