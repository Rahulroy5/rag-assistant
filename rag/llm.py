import google.generativeai as genai


def generate_answer(
    question: str,
    context_chunks: list[str],
    api_key: str,
    model: str = "gemini-1.5-flash",
) -> str:
    context = "\n\n---\n\n".join(context_chunks)

    genai.configure(api_key=api_key)

    client = genai.GenerativeModel(
        model_name=model,
        system_instruction=(
            "You are a precise Q&A assistant. Answer the user's question using ONLY "
            "the provided context. If the answer is not in the context, say: "
            "'I don't have enough information in this document to answer that.' "
            "Be concise and clear."
        ),
    )

    response = client.generate_content(
        f"Context:\n{context}\n\nQuestion: {question}"
    )
    return response.text
