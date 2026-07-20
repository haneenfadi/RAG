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

# "هل في إجازة أمومة بالقانون الأردني؟"
# "هل يمكن فصل الموظف بسبب مرضه؟"
# "ما هي مدة الإجازة المرضية للموظف في القانون الأردني؟"
# "هل يجوز ارفض الضمان الاجتماعي؟"

query = "هل يمكن توظيف شخص غير أردني؟"


def ask(question):

    # embedding the query
    query_embedding = model.encode(
        "query: " + query,
        normalize_embeddings=True
    ).tolist()
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

    print("========== CONTEXT  start ==========")
    print(context)
    print("=============================")

    prompt = f"""
    You are a legal assistant specialized in Jordanian labor law and social security regulations.
    
    Rules:
    1. Answer only using the provided context.
    2. Do not make up information that is not in the context.
    3. If the context does not directly answer the question:
    - If the retrieved context contains related information that may help the user understand the topic, briefly summarize that information and clearly state that it does not directly answer the question.
    - If the context contains no relevant information at all, respond that there is not enough information to answer the question.
    Never invent facts that are not supported by the provided context.
    4. If multiple sources are relevant, combine them clearly and mention the difference.
    5. The output must contain Arabic characters only ,Do not mix any other alphabet.
    
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

    return response.choices[0].message.content


result = ask(query)
print(result)


# try to list all models available in the Groq API for testing purposes
models = groq_client.models.list()

for model in models.data:
    print(model.id)
