from sentence_transformers import SentenceTransformer
import chromadb
from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=groq_api_key)

model = SentenceTransformer("intfloat/multilingual-e5-base")
client = chromadb.PersistentClient(path="src/embedding/chroma_db")

collection = client.get_collection("legal_rag")


def embed_query(query: str):
    # embedding the query
    query_embedding = model.encode(
        "query: " + query,
        normalize_embeddings=True
    ).tolist()
    return query_embedding


def ask(query_embedding, query):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    context = ""

    for doc, metadata in zip(
        results["documents"][0],
        results["metadatas"][0]
    ):
        context += f"""
    Source: {metadata['source']} 
    {doc}
    ---
    """

    prompt = f"""
    You are a legal assistant specialized in Jordanian labor law and social security regulations.
    Rules:
    1. Answer only using the provided context.
    2. Do not invent information that is not supported by the context.
    3. If the context partially answers the question:
    - Provide the available information.
    - Clearly state which part of the question is not covered by the context.
    - Do not claim that no information exists about the topic if related information is available.
    - Only state that there is not enough information when the context contains no relevant information.
    4. If multiple sources are relevant, combine them clearly and mention the difference.
    5. The answer text must be in Arabic only. Keep JSON keys unchanged.
    6. If the user's question is ambiguous and could refer to multiple legal concepts, state the assumption based on the retrieved context before answering. Do not present the assumption as certain.
        
    
        {{
            "answer": "<Arabic answer>",
            "sources": [
                {{
                        "source": "<source name>",
                "reference": "<article number or FAQ number>"
                }}
            ]
        }}
    Context:
    {context}

    Question:
    {query}

    Answer:
    """
    response = groq_client.chat.completions.create(
        model="qwen/qwen3.6-27b",  # openai/gpt-oss-20b # llama-3.3-70b-versatile
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        reasoning_effort="none"
    )

    print("========== CONTEXT ==========")
    print(context)
    return response.choices[0].message.content


result = ask(
    embed_query("ما هي حقوق العامل في الأردن؟"),
    "ما هي حقوق العامل في الأردن؟"
)

print(result)
