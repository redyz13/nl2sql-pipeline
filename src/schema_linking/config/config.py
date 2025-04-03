import os
from dotenv import load_dotenv

load_dotenv()

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

TABLE_INDEX_BIN = "faiss_tables.bin"
TABLE_MAPPING_PKL = "faiss_tables.pkl"

COLUMN_INDEX_BIN = "faiss_columns.bin"
COLUMN_MAPPING_PKL = "faiss_columns.pkl"
