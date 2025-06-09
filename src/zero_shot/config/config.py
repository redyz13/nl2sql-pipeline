import os
from dotenv import load_dotenv

load_dotenv()

# Environment configuration
APP_ENV = os.getenv("APP_ENV")
ALLOWED_ORIGINS = (
    ["https://localhost:3000"] if APP_ENV == "production" else ["*"]
)
API_HOST = os.getenv("API_HOST");
API_PORT = int(os.getenv("API_PORT"));
API_URL = f"http://{API_HOST}:{API_PORT}/query"

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

# Table and plot configuration
MAX_RESULT_ROWS = 50
MAX_BAR_ITEMS = 20
MAX_LINE_POINTS = 1000
MAX_SCATTER_POINTS = 500
MIN_PLOT_ROWS = 2
MIN_PLOT_COLS = 2
MIN_DISTINCT_Y = 2
MAX_PIE_UNIQUE = 4
MAX_PIE_ROWS = 10
LABEL_LENGTH_THRESHOLD = 25
PLOT_FIGSIZE = (8, 5)
PLOT_DPI = 250
PLOT_BLACKLIST = {
    "KSDESCRI", "KSCODFIS", "KSCODIVA", "COCODICE", "DONUMDOC", "DOCODSOG"
}
