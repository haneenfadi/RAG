from sentence_transformers import CrossEncoder
import time
from loguru import logger


def retrieve_context(
    collection,
    query,
    query_embedding,
    reranker_model: CrossEncoder
) -> str:
    """
    Retrieve documents from ChromaDB, rerank them, and build final context.
    """
    start = time.perf_counter()

    # 1. Retrieve candidate documents from ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )
    t1 = time.perf_counter()

    print(
        f"Chroma retrieval: {t1-start:.2f}s"
    )
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # 2. Prepare query-document pairs for reranker
    pairs = [
        (query, doc)
        for doc in documents
    ]

    logger.info(f"Number of reranker pairs: {len(pairs)}")

    for i, pair in enumerate(pairs):
        logger.info(f"Pair {i} doc length: {len(pair[1])}")
    # 3. Calculate reranker scores
    scores = reranker_model.predict(pairs)
    t2 = time.perf_counter()

    print(
        f"Reranker: {t2-t1:.2f}s"
    )
    # 4. Sort documents by reranker score
    reranked_results = sorted(
        zip(
            documents,
            metadatas,
            scores
        ),
        key=lambda x: x[2],
        reverse=True
    )

    # 5. Take best documents
    top_k = 3
    top_results = reranked_results[:top_k]

    # 6. Build final context for LLM
    context = ""

    for doc, metadata, score in top_results:
        context += f"""
    Source: {metadata['source']}
    {doc}
    ---
    """

    return context
