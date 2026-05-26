from typing import List

import chromadb
import ollama
from chromadb import EmbeddingFunction, Embeddings

from models import Chunk

EMBEDDING_MODEL = "qwen3-embedding:0.6b"


class OllamaEmbedder(EmbeddingFunction):
    """Embeds text locally using qwen3-embedding:0.6b served by Ollama.

    Chosen over cloud-hosted embeddings so the full pipeline stays local —
    a hard requirement for any enterprise document Q&A use case.
    """

    def __call__(self, input: List[str]) -> Embeddings:
        return [ollama.embeddings(model=EMBEDDING_MODEL, prompt=text)["embedding"] for text in input]


def get_fresh_collection(client: chromadb.Client, collection_name: str = "rag_docs"):
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass
    return client.create_collection(
        name=collection_name,
        embedding_function=OllamaEmbedder(),
        metadata={"hnsw:space": "cosine"},
    )


def add_chunks(collection, chunks: List[Chunk]) -> None:
    collection.add(
        ids=[c.id for c in chunks],
        documents=[c.text for c in chunks],
        metadatas=[{"source": c.source, "chunk_index": c.chunk_index} for c in chunks],
    )


def retrieve(collection, question: str, n_results: int = 2) -> List[str]:
    """Top-2 cosine retrieval.

    Tested top-5 first — extra chunks introduced noise that distracted the LLM.
    Two highly relevant chunks consistently beat five mixed ones.
    """
    results = collection.query(query_texts=[question], n_results=n_results)
    return results["documents"][0]
