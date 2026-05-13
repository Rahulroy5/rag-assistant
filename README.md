# PDF Q&A Assistant

Upload any PDF and ask questions in plain English. Powered by Gemini — completely free, no installation, works instantly in any browser.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red?style=flat-square&logo=streamlit)
![Gemini](https://img.shields.io/badge/Gemini-1.5%20Flash-blue?style=flat-square&logo=google)
![ChromaDB](https://img.shields.io/badge/ChromaDB-vector%20store-purple?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

---

## How It Works

```
PDF Upload
   │
   ▼
MarkItDown            →  Extracts text from PDF into clean markdown
   │
   ▼
Chunker               →  Splits text into 500-word overlapping chunks
   │
   ▼
bge-small-en-v1.5     →  Embeds each chunk into a 384-dim vector (ONNX, free, no API)
   │
   ▼
ChromaDB              →  Stores vectors, retrieves top-3 by cosine similarity
   │
   ▼
Gemini 1.5 Flash      →  Generates an answer grounded in retrieved context
   │
   ▼
Streamlit UI          →  Displays answer with collapsible source chunks
```

---

## Features

- **Completely free** — Gemini API has a free tier, no credit card needed
- **No installation** — deploy to Streamlit Community Cloud in minutes
- **Free embeddings** — `bge-small-en-v1.5` runs on CPU via ONNX, no cost
- **Source transparency** — every answer shows the exact chunks the model used
- **Chat interface** — persistent Q&A history within a session
- **Clean UI** — dark-themed Streamlit app with sidebar document management

---

## Tech Stack

| Component       | Tool                                      |
|-----------------|-------------------------------------------|
| Frontend        | Streamlit                                 |
| PDF Parser      | MarkItDown (Microsoft)                    |
| Embeddings      | `bge-small-en-v1.5` via fastembed (ONNX)  |
| Vector Store    | ChromaDB (in-memory, cosine similarity)   |
| LLM             | Gemini 1.5 Flash (free tier)              |
| Data Validation | Pydantic v2                               |

---

## Deploy (free, public URL)

**Streamlit Community Cloud:**
1. Fork this repo
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app → select your fork
3. Advanced settings → Secrets → add:
   ```toml
   GOOGLE_API_KEY = "AIza..."
   ```
4. Deploy — get a public URL in ~2 minutes

Get a free Gemini API key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey) — no credit card required.

---

## Run Locally

**Prerequisites:** Python 3.10+

```bash
git clone https://github.com/Rahulroy5/rag-assistant.git
cd rag-assistant
pip install -r requirements.txt
streamlit run app.py
```

Open **http://localhost:8501**, enter your Gemini API key in the sidebar, upload a PDF, and start asking questions.

---

## Project Structure

```
rag-assistant/
├── app.py              # Streamlit UI — upload, chat, API key input, session state
├── models.py           # Pydantic schemas (Chunk, QueryResult)
├── requirements.txt
├── render.yaml         # Render deployment config
├── Dockerfile          # HuggingFace Spaces deployment config
└── rag/
    ├── parser.py       # MarkItDown: PDF → markdown text
    ├── chunker.py      # Split text into overlapping word chunks
    ├── store.py        # ChromaDB: embed, store, and retrieve chunks
    └── llm.py          # Gemini: generate answer from retrieved context
```

---

## Limitations

- Scanned / image-based PDFs are not supported (no OCR)
- In-memory ChromaDB — indexed documents reset on app restart
