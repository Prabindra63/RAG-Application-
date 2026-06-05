from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

INDEX_PATH = DATA_DIR / "index.faiss"
CHUNK_PATH = DATA_DIR / "chunks.pkl"
METADATA_PATH = DATA_DIR / "metadata.json"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

GEMINI_MODEL = "gemini-2.5-flash"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

TOP_K_RETRIEVAL = 5

EMBED_BATCH_SIZE = 32
EMBED_CACHE_SIZE = 5000