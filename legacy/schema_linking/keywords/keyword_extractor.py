from schema_linking.llm.llm_client import send_prompt
from schema_linking.prompt.prompt_builder import build_keyword_prompt

def llm_keyword_extraction(question: str) -> list[str]:
    prompt = build_keyword_prompt(question)
    raw_output = send_prompt(prompt)
    return raw_output