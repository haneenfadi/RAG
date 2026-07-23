
from sentence_transformers import CrossEncoder
from sentence_transformers import SentenceTransformer
import chromadb


# =========================
# 1. Load Embedding Model
# =========================

embedding_model = SentenceTransformer(
    "intfloat/multilingual-e5-base"
)


# =========================
# 2. Connect to ChromaDB
# =========================

client = chromadb.PersistentClient(
    path="src/embedding/chroma_db"
)

collection = client.get_collection(
    "legal_rag"
)


# =========================
# 3. User Query
# =========================

query = ""


# =========================
# 4. Create Query Embedding
# =========================

query_embedding = embedding_model.encode(
    "query: " + query,
    normalize_embeddings=True
).tolist()


# =========================
# 5. Retrieve Documents
# =========================


results = collection.query(
    query_embeddings=[query_embedding],
    n_results=10
)


documents = results["documents"][0]
metadatas = results["metadatas"][0]
distances = results["distances"][0]


print("========== Chroma Results ==========")

for doc, metadata, distance in zip(
    documents,
    metadatas,
    distances
):
    print(f"Distance: {distance}")
    print(f"Metadata: {metadata}")
    print(doc[:300])
    print("-" * 50)


# =========================
# 6. Load Reranker Model
# =========================

reranker_model = CrossEncoder(
    "BAAI/bge-reranker-v2-m3"
)


# =========================
# 7. Prepare Query-Document Pairs
# =========================

pairs = [
    (query, doc)
    for doc in documents
]


# =========================
# 8. Calculate Reranker Scores
# =========================

scores = reranker_model.predict(pairs)


# =========================
# 9. Sort Documents by Reranker Score
# =========================

reranked_results = sorted(
    zip(
        documents,
        metadatas,
        scores
    ),
    key=lambda x: x[2],
    reverse=True
)


# =========================
# 10. Final Top Results
# =========================

top_k = 3

print("\n========== Reranked Results ==========")


for doc, metadata, score in reranked_results[:top_k]:

    print(f"Reranker Score: {score}")
    print(f"Metadata: {metadata}")
    print(doc[:500])
    print("-" * 50)
