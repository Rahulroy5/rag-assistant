# PDF Q&A Assistant — Local RAG Pipeline

A fully local, open-source RAG (Retrieval-Augmented Generation) system for PDF document Q&A. Upload any PDF and ask questions in plain English — no API keys, no cloud, no data leaves your machine.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red?style=flat-square&logo=streamlit)
![Ollama](https://img.shields.io/badge/Ollama-local-black?style=flat-square)
![ChromaDB](https://img.shields.io/badge/ChromaDB-vector%20store-orange?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

---

## How It Works

```
PDF Upload
   │
   ▼
MarkItDown          →  Extracts text from PDF into clean markdown
   │
   ▼
Chunker             →  Splits text into 500-word overlapping chunks
   │
   ▼
nomic-embed-text    →  Embeds each chunk into a 768-dim vector (via Ollama)
   │
   ▼
ChromaDB            →  Stores vectors, retrieves top-2 by cosine similarity
   │
   ▼
qwen2:1.5b-instruct →  Generates an answer grounded in retrieved context
   │
   ▼
Streamlit UI        →  Displays answer with collapsible source chunks
```

---

## Features

- **Fully local** — embeddings and LLM run on your machine via Ollama
- **No paid APIs** — entirely open-source model stack
- **Chat interface** — persistent Q&A history within a session
- **Source transparency** — every answer shows the retrieved context chunks
- **Fast** — `qwen2:1.5b-instruct` runs on Apple Silicon GPU in ~2–4 seconds
- **Clean UI** — dark-themed Streamlit app with sidebar document management

---

## Tech Stack

| Component | Tool |
|---|---|
| Frontend | Streamlit |
| PDF Parser | MarkItDown (Microsoft) |
| Embeddings | `nomic-embed-text` via Ollama |
| Vector Store | ChromaDB (in-memory, cosine similarity) |
| LLM | `qwen2:1.5b-instruct` via Ollama |
| Data Validation | Pydantic v2 |

---

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/Rahulroy5/rag-assistant.git
cd rag-assistant
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
pip install "markitdown[pdf]"
```

**3. Pull the required models**
```bash
ollama pull nomic-embed-text
ollama pull qwen2:1.5b-instruct
```

**4. Run the app**
```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## Project Structure

```
rag-assistant/
├── app.py              # Streamlit UI — upload, chat, session state
├── models.py           # Pydantic schemas (Chunk, QueryResult)
├── requirements.txt
└── rag/
    ├── parser.py       # MarkItDown: PDF → markdown text
    ├── chunker.py      # Split text into overlapping word chunks
    ├── store.py        # ChromaDB: embed, store, and retrieve chunks
    └── llm.py          # Ollama: generate answer from context
```

---

## Usage

1. Upload a PDF using the sidebar
2. Wait for indexing (a few seconds depending on PDF size)
3. Type your question in the chat input
4. The answer appears with a "View source context" expander showing exactly what the model used

---

## Limitations

- Scanned / image-based PDFs are not supported (no OCR)
- Context window limited to top-2 retrieved chunks per query
- In-memory ChromaDB — indexed documents reset on app restart
