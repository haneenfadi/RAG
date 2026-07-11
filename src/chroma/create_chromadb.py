from sentence_transformers import SentenceTransformer
import chromadb
import json
# from torch import embedding

# 1) Load the model
model = SentenceTransformer("intfloat/multilingual-e5-base")

client = chromadb.PersistentClient(path="src/chroma/chroma_db")

collection = client.get_or_create_collection(
    name="labor_law",  metadata={"hnsw:space": "cosine"}

)

# 3) load the chunks and create the embeddings
documents = []
embeddings = []
metadatas = []
ids = []

with open("src/chunking/chunks/article_based_chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

for i, chunk in enumerate(chunks):

    text = chunk["text"]

    documents.append(text)

    embeddings.append(model.encode(
        "passage: " + text,
        normalize_embeddings=True
    ))

    metadatas.append({
        "article_number": chunk["metadata"]["article_number"]
    })
    ids.append(str(i))

# 4) store in Chroma
collection.add(
    ids=ids,
    documents=documents,
    metadatas=metadatas,
    embeddings=embeddings
)

print("Stored:", collection.count())
