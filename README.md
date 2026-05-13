# PDF Q&A Assistant

Upload any PDF and ask questions in plain English. Powered by Claude — no installation, no local models, works instantly in any browser.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red?style=flat-square&logo=streamlit)
![Claude](https://img.shields.io/badge/Claude-Haiku-orange?style=flat-square)
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
bge-small-en-v1.5     →  Embeds each chunk into a 384-dim vector (ONNX, free, fast)
   │
   ▼
ChromaDB              →  Stores vectors, retrieves top-3 by cosine similarity
   │
   ▼
Claude Haiku          →  Generates an answer grounded in retrieved context
   │
   ▼
Streamlit UI          →  Displays answer with collapsible source chunks
```

---

## Features

- **No installation** — works in the browser, deploy to Render in one click
- **One API key** — only needs an Anthropic API key, nothing else
- **Free embeddings** — `all-MiniLM-L6-v2` runs on CPU, no cost, no rate limits
- **Source transparency** — every answer shows the exact chunks the model used
- **Chat interface** — persistent Q&A history within a session
- **Clean UI** — dark-themed Streamlit app with sidebar document management

---

## Tech Stack

| Component      | Tool                                        |
|----------------|---------------------------------------------|
| Frontend       | Streamlit                                   |
| PDF Parser     | MarkItDown (Microsoft)                      |
| Embeddings     | `bge-small-en-v1.5` via fastembed (ONNX)    |
| Vector Store   | ChromaDB (in-memory, cosine similarity)     |
| LLM            | Claude Haiku via Anthropic API              |
| Data Validation| Pydantic v2                                 |

---

## Deploy to Render (free, public URL)

1. Fork this repo on GitHub
2. Go to [render.com](https://render.com) → New → Web Service → connect your fork
3. Render auto-detects `render.yaml` — click Deploy
4. Done. You get a public URL anyone can open.

No API key is hardcoded — users enter their own key in the sidebar.

---

## Run Locally

**Prerequisites:** Python 3.10+

```bash
git clone https://github.com/Rahulroy5/rag-assistant.git
cd rag-assistant
pip install -r requirements.txt
streamlit run app.py
```

Open **http://localhost:8501**, enter your Anthropic API key in the sidebar, upload a PDF, and start asking questions.

---

## Project Structure

```
rag-assistant/
├── app.py              # Streamlit UI — upload, chat, API key input, session state
├── models.py           # Pydantic schemas (Chunk, QueryResult)
├── requirements.txt
├── render.yaml         # One-click Render deployment config
└── rag/
    ├── parser.py       # MarkItDown: PDF → markdown text
    ├── chunker.py      # Split text into overlapping word chunks
    ├── store.py        # ChromaDB: embed, store, and retrieve chunks
    └── llm.py          # Claude: generate answer from retrieved context
```

---

## Limitations

- Scanned / image-based PDFs are not supported (no OCR)
- In-memory ChromaDB — indexed documents reset on app restart
- Requires an Anthropic API key (free tier available at console.anthropic.com)
