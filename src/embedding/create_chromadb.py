from sentence_transformers import SentenceTransformer
import chromadb
import json


model = SentenceTransformer("intfloat/multilingual-e5-base")


client = chromadb.PersistentClient(
    path="src/embedding/chroma_db"
)

collection = client.get_or_create_collection(
    name="legal_rag",
    metadata={"hnsw:space": "cosine"}
)


documents = []
embeddings = []
metadatas = []
ids = []


# الملفات التي تريد إضافتها
chunk_files = [
    "src/chunking/chunks/article_based_chunks.json",
    "src/chunking/chunks/faq_chunks.json"
]


for file_path in chunk_files:

    with open(file_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    for chunk in chunks:

        text = chunk["text"]

        documents.append(text)

        embeddings.append(
            model.encode(
                "passage: " + text,
                normalize_embeddings=True
            )
        )

        metadatas.append(chunk["metadata"])

        ids.append(
            chunk["metadata"]["chunk_id"]
        )


collection.add(
    ids=ids,
    documents=documents,
    metadatas=metadatas,
    embeddings=embeddings
)


print("Stored:", collection.count())
print(collection.get(include=["metadatas",
      "documents", "embeddings"], limit=5))
