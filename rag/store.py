from typing import List

import chromadb
import ollama
from chromadb import EmbeddingFunction, Embeddings

from models import Chunk


class OllamaEmbedder(EmbeddingFunction):
    def __init__(self, model: str = "nomic-embed-text"):
        self.model = model

    def __call__(self, input: List[str]) -> Embeddings:
        response = ollama.embed(model=self.model, input=input)
        return response.embeddings


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
    results = collection.query(query_texts=[question], n_results=n_results)
    return results["documents"][0]
