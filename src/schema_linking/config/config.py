import os
from dotenv import load_dotenv

load_dotenv()

# Base directory configuration
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# LLaMA API configuration
LLAMA_API_URL = os.getenv("LLAMA_API_URL")
LLAMA_API_USER = os.getenv("LLAMA_API_USER")
LLAMA_API_PASS = os.getenv("LLAMA_API_PASS")
VERIFY_SSL = False

# Schema linking configuration
TOP_K_COLUMNS = 50
EMBEDDING_MODEL = "paraphrase-multilingual-mpnet-base-v2"

COLUMN_INDEX_BIN = os.path.join(DATA_DIR, "faiss_columns.bin")
COLUMN_MAPPING_PKL = os.path.join(DATA_DIR, "faiss_columns.pkl")