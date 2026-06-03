import ollama

from models import QueryResult, RetrievedContext

LLM_MODEL = "gpt-oss:20b"

SYSTEM_PROMPT = (
    "You are a precise Q&A assistant. Answer the user's question using ONLY "
    "the provided context. If the answer is not in the context, say: "
    "'I don't have enough information in this document to answer that.' "
    "Be concise and clear."
)


def generate_answer(
    context: RetrievedContext,
    model: str = LLM_MODEL,
) -> QueryResult:
    """Generate a grounded answer using gpt-oss:20b served locally via Ollama.

    Open-source, runs fully local, no API keys, no data leaves the machine.
    """
    joined_context = "\n\n---\n\n".join(context.chunks)

    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{joined_context}\n\nQuestion: {context.question}"},
        ],
    )
    return QueryResult(
        question=context.question,
        context_chunks=context.chunks,
        answer=response["message"]["content"],
    )
