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
MAX_RESULT_ROWS = 50  # Maximum number of rows to display in result tables

# Maximum data limits for different plot types
MAX_POINTS = {
    "line": 1000,
    "scatter": 500,
    "bar": 20,
    "barh": 20,
    "pie": 4
}

# Valid plot types
VALID_KINDS = set(MAX_POINTS.keys())

# Plot constraints
MIN_PLOT_ROWS = 2           # Min rows required to generate a plot
MIN_PLOT_COLS = 2           # Min columns required to generate a plot
MIN_DISTINCT_Y = 2          # Min distinct numeric Y values
MAX_PIE_CATEGORIES = 4      # Max number of slices for pie charts
LABEL_LENGTH_THRESHOLD = 25 # Switch to horizontal bars if labels are too long

# Plot appearance
PLOT_FIGSIZE = (8, 5)       # Default figure size
PLOT_DPI = 250              # Plot resolution (dots per inch)

# Columns excluded from plotting
PLOT_BLACKLIST = {
    "KSDESCRI", "KSCODFIS", "KSCODIVA", "COCODICE", "DONUMDOC", "DOCODSOG"
}
