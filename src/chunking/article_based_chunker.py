from unicodedata import normalize
from langchain_core.documents import Document
import json
import re


# ==========================
# Load and merge pages
# ==========================

full_text = ""

with open(
    "src/data/extracted/pypdfium2_output_extracted.json",
    "r",
    encoding="utf-8"
) as r:
    data = json.load(r)

    for page in data["pages"]:
        full_text += normalize("NFKC", page["text"]) + "\n"


print("Text length:", len(full_text))


# ==========================
# Split by article
# ==========================

# Matches:
# المادة )1(
# المادة )2(
# المادة )32(
ARTICLE_PATTERN = re.compile(
    r"(?=المادة\s*\)\s*\d+\s*\()"
)

article_texts = ARTICLE_PATTERN.split(full_text)

print("=" * 60)
print("Number of parts:", len(article_texts))
print("=" * 60)


# ==========================
# Article Size Statistics
# ==========================

article_sizes = []

for article_text in article_texts:

    article_text = article_text.strip()

    if not article_text:
        continue

    # Extract article number
    num_match = re.search(
        r"المادة\s*\)\s*(\d+)\s*\(",
        article_text
    )

    if not num_match:
        continue

    article_num = num_match.group(1)

    word_count = len(article_text.split())
    article_sizes.append(word_count)

    print(
        f"Article {article_num:>3}: "
        f"{word_count:>5} words"
    )


# ==========================
# Summary
# ==========================

print("\nSummary")

if article_sizes:
    print(f"Total articles: {len(article_sizes)}")
    print(f"Smallest article: {min(article_sizes)} words")
    print(f"Largest article: {max(article_sizes)} words")
    print(
        f"Average article size: "
        f"{sum(article_sizes) / len(article_sizes):.1f} words"
    )


# ==========================
# Create Documents
# ==========================

all_chunks = []

for article_text in article_texts:

    article_text = article_text.strip()

    if not article_text:
        continue

    # Extract article number
    num_match = re.search(
        r"المادة\s*\)\s*(\d+)\s*\(",
        article_text
    )

    if not num_match:
        continue

    article_num = num_match.group(1)

    all_chunks.append(
        Document(
            page_content=article_text,
            metadata={
                "chunk_id": f"law_article_{article_num}",
                "type": "law_article",
                "source": "قانون العمل الأردني"
            }
        )
    )


# ==========================
# Chunk Details
# ==========================

print("\nChunk Details")
print("-" * 60)

for doc in all_chunks:

    words = len(doc.page_content.split())
    chunk_id = doc.metadata["chunk_id"]

    print(
        f"Chunk ID: {chunk_id} "
        f"| Length: {words} words"
    )


# ==========================
# Save
# ==========================

output_path = (
    "src/chunking/chunks/article_based_chunks.json"
)

with open(output_path, "w", encoding="utf-8") as f:

    json.dump(
        [
            {
                "text": d.page_content,
                "metadata": d.metadata
            }
            for d in all_chunks
        ],
        f,
        ensure_ascii=False,
        indent=4
    )


print("\nTotal chunks:", len(all_chunks))
print(f"Saved to: {output_path}")
