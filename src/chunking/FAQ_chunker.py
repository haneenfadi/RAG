
import json
from langchain_core.documents import Document

with open("src/data/extracted/social_security_faq.json", "r", encoding="utf-8") as file:
    ssc_text = json.load(file)

all_chunks = []
n = 0

for item in ssc_text["text"]:
    text = item.strip()
    if not text:
        continue
    n += 1

    all_chunks.append(
        {
            "text": text,
            "metadata": {
                "chunk_id": f"ssc_faq_{n}",
                "source": "المؤسسة العامة للضمان الاجتماعي - الأسئلة الشائعة",
                "type": "FAQ_SSC"
            }
        }
    )
print(f"Total chunks:", all_chunks)
print(f"Total chunks: {len(all_chunks)}")

with open("src/chunking/chunks/faq_chunks.json", "w", encoding="utf-8") as f:
    json.dump(
        all_chunks,
        f,
        ensure_ascii=False,
        indent=4
    )
