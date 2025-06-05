import os
from dotenv import load_dotenv

load_dotenv()

# Base directory configuration
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
PROMPTS_DIR = os.path.join(PROJECT_ROOT, "prompts/schema_linking")

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

# LLM API configuration
LLM_API_URL = os.getenv("LLM_API_URL")
LLM_API_USER = os.getenv("LLM_API_USER")
LLM_API_PASS = os.getenv("LLM_API_PASS")
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
    "final": os.path.join(PROMPTS_DIR, "final_prompt.txt"),
    "llm_wrapper": os.path.join(PROMPTS_DIR, "llm_wrapper_prompt.txt")
}