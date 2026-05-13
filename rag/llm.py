import anthropic


def generate_answer(
    question: str,
    context_chunks: list[str],
    api_key: str,
    model: str = "claude-haiku-4-5-20251001",
) -> str:
    context = "\n\n---\n\n".join(context_chunks)

    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model=model,
        max_tokens=1024,
        system=(
            "You are a precise Q&A assistant. Answer the user's question using ONLY "
            "the provided context. If the answer is not in the context, say: "
            "'I don't have enough information in this document to answer that.' "
            "Be concise and clear."
        ),
        messages=[
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}",
            }
        ],
    )
    return message.content[0].text
