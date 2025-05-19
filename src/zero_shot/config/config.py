import os
from dotenv import load_dotenv

load_dotenv()

# Base directory configuration
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PROMPTS_DIR = os.path.join(PROJECT_ROOT, "prompts/zero_shot")

PROMPT_PATHS = {
    "schema": os.path.join(PROMPTS_DIR, "schema_llm_prompt.txt"),
    "llm_wrapper": os.path.join(PROMPTS_DIR, "llm_wrapper_prompt.txt")
}

# LLM API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_ID = os.getenv("OPENAI_MODEL_ID", "gpt-4o-mini")

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# Schema configuration
TABLES = ["ba_commes", "ba_keysog", "ba_docume_m"]

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