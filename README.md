# 📊 FinReport AI - Financial Report Analysis with RAG

Upload financial reports (PDF) and ask natural language questions to get accurate, grounded answers with source citations.

## 🎯 Features

- **📄 PDF Upload** - Extract text from financial reports
- **🔍 Smart Retrieval** - Find relevant chunks using semantic search
- **🤖 AI Answers** - Generate responses using Google Gemini
- **📖 Source Citations** - Every answer shows page numbers and relevant excerpts
- **💬 Chat Interface** - Simple Streamlit UI

## ⚙️ Setup (5 minutes)

### 1. Prerequisites
- Python 3.10+ 
- Google Gemini API key (free): https://makersuite.google.com/app/apikeys

### 2. Clone & Install
```bash
git clone <repo-url>
cd finreport-ai
python -m venv venv

# On Windows: venv\Scripts\activate
# On Linux/Mac: source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure API Key
```bash
cp .env .env
### 4. Run
```bash
streamlit run app.py
```

Open http://localhost:8501

## 🏗️ RAG Pipeline

```
PDF → Extract Text → Chunk → Embed → Index (FAISS)
                                         ↓
                                    Query (Embed)
                                         ↓
                                    Retrieve Top-5
                                         ↓
                                    Generate Answer (Gemini)
                                         ↓
                                    Answer + Citations
```

## 📁 Project Structure

```
finreport-ai/
## 📂 Project Structure

```text
FINREPORT-AI/
│
├── app.py
├── requirements.txt
├── README.md
├── setup.md
├── .env
├── .gitignore
│
├── backend/
│   ├── chunker.py
│   ├── config.py
│   ├── embeddings.py
│   ├── pdf_loader.py
│   ├── rag_pipeline.py
│   ├── retriever.py
│   ├── service.py
│   └── vector_store.py
│
├── uploads/
│   └── (uploaded PDF reports)
│
├── vector_db/
│   ├── chunks.pkl
│   ├── index.faiss
│   └── metadata.json
│
└── venv/
    └── (virtual environment files)
```

## 🎓 How It Works

1. **Upload PDF** → Text extraction using PyMuPDF
2. **Chunk Text** → Split into 15-line chunks with 3-line overlap
3. **Generate Embeddings** → Use Sentence-Transformers (all-MiniLM-L6-v2)
4. **Store Vectors** → Index in FAISS for fast similarity search
5. **Answer Questions** → Retrieve top-5 chunks + generate answer via Gemini

## 🔧 Configuration

Edit `backend/config.py` to customize:

```python
CHUNK_LINE_LIMIT = 15      # Lines per chunk
CHUNK_OVERLAP_LINES = 3    # Overlap
TOP_K_RETRIEVAL = 5        # Results per query
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
GEMINI_MODEL = "gemini-2.0-flash"
```

## 🎯 Example Questions

```
"What was the total revenue this quarter?"
"What are the key risk factors?"
"Who are the board members?"
"What is the dividend policy?"
```

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| streamlit | Web UI |
| google-generativeai | Gemini API |
| sentence-transformers | Embeddings |
| faiss-cpu | Vector search |
| PyMuPDF | PDF extraction |

## 🐛 Troubleshooting

| Issue | Fix |
|-------|-----|
| API key error | Check .env file has GOOGLE_API_KEY |
| Index not found | Upload and process a PDF first |
| Port in use | Run `streamlit run app.py --server.port 8502` |

## 📚 Resources

- [RAG Documentation](https://docs.anthropic.com/en/docs/build-a-research-assistant)
- [FAISS Docs](https://faiss.ai/)
- [Gemini API](https://ai.google.dev/)
- [Streamlit Docs](https://docs.streamlit.io/)

---

**Built for intelligent financial document analysis**

