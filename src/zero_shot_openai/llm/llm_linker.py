from zero_shot_openai.llm.llm_client import send_prompt
from zero_shot_openai.prompt.prompt_builder import build_sql_prompt

def llm_generate_sql(question: str) -> list[str]:
    prompt = build_sql_prompt(question)
    output = send_prompt(prompt)
    return output
