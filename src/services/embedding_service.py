from sentence_transformers import SentenceTransformer
from src.utils.query_preprocessing import preprocess_query


def embed_query(model: SentenceTransformer, query: str) -> list[float]:
    """    Convert a user query into an embedding vector."""
    query = preprocess_query(query)
    # embedding the query
    query_embedding = model.encode(
        "query: " + query,
        normalize_embeddings=True
    ).tolist()
    return query_embedding
