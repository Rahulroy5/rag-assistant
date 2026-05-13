from typing import List

import chromadb
from chromadb import EmbeddingFunction, Embeddings
from fastembed import TextEmbedding

from models import Chunk

_embedder: TextEmbedding | None = None


def _get_embedder() -> TextEmbedding:
    global _embedder
    if _embedder is None:
        _embedder = TextEmbedding("BAAI/bge-small-en-v1.5")
    return _embedder


class LocalEmbedder(EmbeddingFunction):
    def __call__(self, input: List[str]) -> Embeddings:
        model = _get_embedder()
        return [v.tolist() for v in model.embed(input)]


def get_fresh_collection(client: chromadb.Client, collection_name: str = "rag_docs"):
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass
    return client.create_collection(
        name=collection_name,
        embedding_function=LocalEmbedder(),
        metadata={"hnsw:space": "cosine"},
    )


def add_chunks(collection, chunks: List[Chunk]) -> None:
    collection.add(
        ids=[c.id for c in chunks],
        documents=[c.text for c in chunks],
        metadatas=[{"source": c.source, "chunk_index": c.chunk_index} for c in chunks],
    )


def retrieve(collection, question: str, n_results: int = 3) -> List[str]:
    results = collection.query(query_texts=[question], n_results=n_results)
    return results["documents"][0]
