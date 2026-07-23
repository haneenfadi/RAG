from loguru import logger
from groq import AsyncGroq
from src.services.prompts.legal_prompt import legal_prompt
import json


async def generate_answer(context, query, groq_client: AsyncGroq) -> str:
    print(f"Context: {context}")
    print(30 * "-")

    prompt = legal_prompt.format(
        context=context,
        query=query
    )

    response = await groq_client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        reasoning_effort="none"
    )
    logger.info(f"Context length: {len(context)} characters")
    response = response.choices[0].message.content
    response = response.replace("\n", " ").replace("\r", " ")
    response = json.loads(response)
    return response
