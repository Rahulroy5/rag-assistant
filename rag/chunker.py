import uuid
from models import Chunk


def chunk_text(
    text: str,
    source: str,
    chunk_size: int = 500,
    overlap: int = 50,
    min_chunk_words: int = 20,
) -> list[Chunk]:
    words = text.split()
    chunks = []
    i = 0
    idx = 0

    while i < len(words):
        end = min(i + chunk_size, len(words))
        chunk_words = words[i:end]

        if len(chunk_words) >= min_chunk_words:
            chunks.append(
                Chunk(
                    id=str(uuid.uuid4()),
                    text=" ".join(chunk_words),
                    source=source,
                    chunk_index=idx,
                )
            )
            idx += 1

        i += chunk_size - overlap

    return chunks
