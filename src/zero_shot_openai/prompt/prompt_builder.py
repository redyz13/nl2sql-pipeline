from datetime import date
from zero_shot_openai.config.config import PROMPT_PATHS

def load_prompt(template_path: str) -> str:
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def build_llm_wrapper_prompt(user_prompt: str, today_date: str) -> str:
    template = load_prompt(PROMPT_PATHS["llm_wrapper"])
    return template.format(user_prompt=user_prompt, today_date=today_date)

def build_sql_prompt(question: str) -> str:
    schema_text = load_prompt(PROMPT_PATHS["schema"])
    user_prompt = f"{schema_text}\n---\nDomanda: {question}"
    today = date.today().strftime("%d %b %Y").lstrip("0")
    return build_llm_wrapper_prompt(user_prompt, today)
