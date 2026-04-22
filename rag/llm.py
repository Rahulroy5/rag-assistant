import re

import ollama


def _strip_thinking(text: str) -> str:
    # qwen3 models output <think>...</think> blocks — remove them
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def generate_answer(
    question: str,
    context_chunks: list[str],
    model: str = "qwen2:1.5b-instruct",
) -> str:
    context = "\n\n---\n\n".join(context_chunks)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a precise Q&A assistant. Answer the user's question using ONLY "
                "the provided context. If the answer is not in the context, say: "
                "'I don't have enough information in this document to answer that.' "
                "Be concise."
            ),
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}",
        },
    ]

    response = ollama.chat(model=model, messages=messages)
    return _strip_thinking(response.message.content)
