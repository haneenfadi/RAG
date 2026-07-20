from sentence_transformers import SentenceTransformer
import chromadb

# Load the model itself that you used for storage
model = SentenceTransformer("intfloat/multilingual-e5-base")

# connect to Chroma
client = chromadb.PersistentClient(path="src/embedding/chroma_db")

collection = client.get_collection("legal_rag")

#  "ما هو عقد التدريب"
#  "العمل الموسمي"
#  "ما واجبات مفتش العمل"
#  "انواع تصاريح العمل"
#  "ما حكم المخالف؟"
# "من هم المستثنون من القانون؟"
# "العمل الموسمي"

query = "هل يوجد تأمين لإصابات العمل؟"  # "هل يجوز استقدام عامل غير اردني؟"

# embedding the query
query_embedding = model.encode(
    "query: " + query,
    normalize_embeddings=True
).tolist()
# search
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

# print the results  add(metadata)
for doc, metadata, distance in zip(
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0]
):
    print(f"Distance: {distance}")
    print(f"Metadata: {metadata}")
    print(doc)
    print("-" * 50)
