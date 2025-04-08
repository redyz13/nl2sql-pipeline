from schema_linking.config.config import PROMPT_PATHS

def load_prompt(template_path: str) -> str:
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def build_llm_wrapper_prompt(user_prompt: str, today_date: str) -> str:
    template = load_prompt(PROMPT_PATHS["llm_wrapper"])
    return template.format(user_prompt=user_prompt, today_date=today_date)

def build_table_prompt(question: str, table_texts: list[str]) -> str:
    tables = "\n".join(f"- {tbl}" for tbl in table_texts)
    template = load_prompt(PROMPT_PATHS["table"])
    return template.format(question=question, tables=tables)

def build_column_prompt(question: str, column_texts: list[str]) -> str:
    columns = "\n".join(f"- {col}" for col in column_texts)
    template = load_prompt(PROMPT_PATHS["column"])
    return template.format(question=question, columns=columns)

def build_keyword_prompt(question: str) -> str:
    template = load_prompt(PROMPT_PATHS["keyword"])
    return template.format(question=question)

def build_final_prompt(question: str, column_texts: list[str], keyword_list: list[str]) -> str:
    columns = "\n".join(f"- {col}" for col in column_texts)
    keywords = "\n".join(f"- {kw}" for kw in keyword_list)
    template = load_prompt(PROMPT_PATHS["final"])
    return template.format(question=question, columns=columns, keywords=keywords)
