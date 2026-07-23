def preprocess_query(query: str) -> str:
    corrections = {
        "أمومه": "أمومة",
        "امومه": "أمومة",
        "امومة": "أمومة",
    }

    for wrong, correct in corrections.items():
        query = query.replace(wrong, correct)

    return query
