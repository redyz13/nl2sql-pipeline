import os
from dotenv import load_dotenv

load_dotenv()

# Base directory configuration
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
PROMPTS_DIR = os.path.join(PROJECT_ROOT, "prompts")

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# Metadata schema configuration
TABLE_METADATA = {
    "table": "ba_table_mod",
    "id_col": "dttableid",
    "description_col": "dtdescri"
}

FIELD_METADATA = {
    "table": "ba_table_fields",
    "table_id_col": "fltableid",
    "field_id_col": "flfieldid",
    "description_col": "fldescri"
}

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

ACTIVE_TABLES_PATH = os.path.join(DATA_DIR, "active_tables.parquet")
ACTIVE_FIELDS_PATH = os.path.join(DATA_DIR, "active_fields.parquet")

PROMPT_PATHS = {
    "keyword": os.path.join(PROMPTS_DIR, "keyword_prompt.txt"),
    "column": os.path.join(PROMPTS_DIR, "column_prompt.txt"),
    "table": os.path.join(PROMPTS_DIR, "table_prompt.txt"),
    "column_filtering": os.path.join(PROMPTS_DIR, "column_filtering_prompt.txt")
}