
from unicodedata import normalize
from langchain_core.documents import Document
import json
import re

# ==========================
# Load and merge pages
# ==========================

full_text = ""

with open("src/data/extracted/pdf_extracted.json", "r", encoding="utf-8") as r:
    data = json.load(r)

    for page in data["pages"]:
        full_text += normalize("NFKC", page["text"]) + "\n"


# ==========================
# Split by article
# ==========================

ARTICLE_PATTERN = re.compile(r'(?=\)\s*المادة\s*\d+\s*\()')
article_texts = ARTICLE_PATTERN.split(full_text)
print("=" * 60)
print("Article Size Statistics")
print("=" * 60)

article_sizes = []

for article_text in article_texts:
    article_text = article_text.strip()

    if not article_text:
        continue

    num_match = re.search(r'المادة\s*(\d+)', article_text)
    article_num = num_match.group(1) if num_match else "title"

    word_count = len(article_text.split())
    article_sizes.append(word_count)

    print(f"Article {article_num:>3}: {word_count:>5} words")

print("\nSummary")
print(f"Total articles: {len(article_sizes)}")
print(f"Smallest article: {min(article_sizes)} words")
print(f"Largest article: {max(article_sizes)} words")
print(
    f"Average article size: {sum(article_sizes)/len(article_sizes):.1f} words")

all_chunks = []

for article_text in article_texts:

    article_text = article_text.strip()
    if not article_text:
        continue

    num_match = re.search(r'المادة\s*(\d+)', article_text)
    if not num_match:
        continue
    article_num = num_match.group(1)

    all_chunks.append(
        Document(
            page_content=article_text,
            metadata={
                "chunk_id": f"law_article_{article_num}", "type": "law_article", "source": "قانون العمل الأردني"
            }
        )
    )

print("\nChunk Details")
print("-" * 60)

for doc in all_chunks:
    words = len(doc.page_content.split())
    chunk_id = doc.metadata["chunk_id"]
    chunk = doc.metadata.get("chunk_index", 0)

    print(
        f"Chunk ID: {chunk_id} "
        f"Chunk {chunk} "
        f"Length: {words} words"
    )
# ==========================
# Save
# ==========================

with open("src/chunking/chunks/article_based_chunks.json", "w", encoding="utf-8") as f:
    json.dump([
        {
            "text": d.page_content,
            "metadata": d.metadata
        }
        for d in all_chunks
    ], f, ensure_ascii=False, indent=4)


print("Total chunks:", len(all_chunks))
