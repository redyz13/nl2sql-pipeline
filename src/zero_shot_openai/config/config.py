import os
from dotenv import load_dotenv

load_dotenv()

# Base directory configuration
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PROMPTS_DIR = os.path.join(PROJECT_ROOT, "prompts/zero_shot_openai")

PROMPT_PATHS = {
    "schema": os.path.join(PROMPTS_DIR, "schema_llm_prompt.txt"),
    "llm_wrapper": os.path.join(PROMPTS_DIR, "llm_wrapper_prompt.txt")
}

# LLM API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_ID = os.getenv("OPENAI_MODEL_ID", "gpt-4o-mini")