from schema_linking.llm.llm_client import send_prompt
from schema_linking.prompt.prompt_builder import (
    build_table_prompt, build_column_prompt, build_final_prompt
)

def llm_table_linking(question: str, table_texts: list[str]) -> list[str]:
    prompt = build_table_prompt(question, table_texts)
    output = send_prompt(prompt)
    return output

def llm_column_linking(question: str, column_texts: list[str]) -> list[str]:
    prompt = build_column_prompt(question, column_texts)
    output = send_prompt(prompt)
    return output

def llm_filter_columns_by_keywords(question: str, column_texts: list[str], keywords: list[str]) -> list[str]:
    prompt = build_final_prompt(question, column_texts, keywords)
    output = send_prompt(prompt)
    return output