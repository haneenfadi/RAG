from loguru import logger
from groq import AsyncGroq
from src.services.prompts.legal_prompt import legal_prompt
import json
import re


async def generate_answer(context, query, groq_client: AsyncGroq) -> str:
    # Use logger.debug to record context length and a short preview instead.
    preview = (context[:500] +
               '...') if context and len(context) > 500 else context
    logger.debug(f"Context preview: {preview}")

    prompt = legal_prompt.format(
        context=context,
        query=query
    )

    response = await groq_client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=800,
        reasoning_effort="none"
    )

    logger.info(f"Context length: {len(context) if context else 0} characters")

    # Extract the assistant text safely
    raw_text = None
    try:
        raw_text = response.choices[0].message.content
    except Exception:
        # If the response shape is unexpected, serialize the whole response object
        try:
            raw_text = json.dumps(response, ensure_ascii=False)
        except Exception:
            raw_text = str(response)

    # Normalize whitespace but keep the text intact (avoid losing unicode characters)
    if isinstance(raw_text, str):
        normalized = raw_text.replace("\r\n", "\n").replace("\r", "\n")
        normalized = re.sub(r"\n+", "\n", normalized).strip()
    else:
        normalized = str(raw_text)

    # Try to parse JSON if the model returned a JSON string; fall back to raw text
    try:
        parsed = json.loads(normalized)
        return parsed
    except Exception:
        # Return the normalized text (string) when JSON parsing fails
        return normalized
