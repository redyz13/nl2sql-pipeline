from schema_linking.llm.llama_client import send_prompt
from schema_linking.prompt.prompt_builder import build_table_prompt, build_column_prompt

def llama_table_linking(question: str, table_texts: list[str]) -> list[str]:
    prompt = build_table_prompt(question, table_texts)
    raw_output = send_prompt(prompt)
    return raw_output

def llama_column_linking(question: str, column_texts: list[str]) -> list[str]:
    prompt = build_column_prompt(question, column_texts)
    raw_output = send_prompt(prompt)
    return raw_output
