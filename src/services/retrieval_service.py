from starlette.concurrency import run_in_threadpool
import time
from loguru import logger


def rerank_documents(
    query,
    documents,
    tokenizer,
    reranker_model
):

    pairs = [
        [query, doc]
        for doc in documents
    ]

    inputs = tokenizer(
        pairs,
        padding=True,
        truncation=True,
        max_length=512,
        return_tensors="pt"
    )

    outputs = reranker_model(
        **inputs,
        return_dict=True
    )
    scores = outputs.logits.view(-1).float().tolist()

    return scores


async def retrieve_context(
    collection,
    query,
    query_embedding,
    reranker_model,
    tokenizer,
    debug: bool = False,
) -> str:
    """
    Retrieve documents from ChromaDB, rerank them, and build final context.

    When debug=True, return a structured dict with retrieval internals:
      {
        "chroma_results": results,
        "chroma_top5_sources": [...],
        "chroma_top5_documents": [...],
        "reranker_scores": [...],
        "reranked_results": [(doc, metadata, score), ...],
        "reranker_top3": [(doc, metadata, score), ...],
        "context": "..."  # the same context string normally returned
      }

    When debug=False (default) preserve existing behavior and return the
    context string only (backwards-compatible).
    """
    start = time.perf_counter()

    # 1. Retrieve candidate documents from ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    print("ChromaDB results retrieved (omitted for brevity)")
    t1 = time.perf_counter()

    print(
        f"Chroma retrieval: {t1-start:.2f}s"
    )
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # 2. Prepare query-document pairs for reranker

    # If a reranker model is not available (e.g., missing optimum/onnx runtime in this environment),
    # fall back to using the Chroma order with neutral scores so evaluation can proceed.
    if reranker_model is None:
        # Create neutral zero scores preserving Chroma order
        scores = [0.0 for _ in documents]
        t2 = time.perf_counter()
        print(f"Reranker: skipped (no model provided), {t2-t1:.2f}s")
        # Keep original chroma order
        reranked_results = list(zip(documents, metadatas, scores))
    else:
        scores = await run_in_threadpool(
            rerank_documents,
            query,
            documents,
            tokenizer,
            reranker_model
        )

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

    if not debug:
        # Backwards-compatible: return context string only
        return context

    # Build structured debug output
    chroma_top5_sources = [m.get("source") if isinstance(
        m, dict) else None for m in metadatas]
    chroma_top5_documents = documents

    reranker_top3 = [
        {"document": d, "metadata": m, "score": s}
        for d, m, s in top_results
    ]

    structured = {
        "chroma_results": results,
        "chroma_top5_sources": chroma_top5_sources,
        "chroma_top5_documents": chroma_top5_documents,
        "reranker_scores": scores,
        "reranked_results": [
            {"document": d, "metadata": m, "score": s}
            for d, m, s in reranked_results
        ],
        "reranker_top3": reranker_top3,
        "context": context
    }

    return structured
