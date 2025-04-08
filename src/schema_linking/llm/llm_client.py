import requests
from datetime import datetime
from schema_linking.prompt.prompt_builder import build_llm_wrapper_prompt
from schema_linking.config.config import (
    LLM_API_URL, LLM_API_USER, LLM_API_PASS, VERIFY_SSL,
)

def send_prompt(prompt: str) -> list[str]:
    today = datetime.now().strftime("%d %b %Y")
    formatted_prompt = build_llm_wrapper_prompt(prompt, today)

    headers = {"Content-Type": "application/json"}
    data = {
        "prompt": formatted_prompt,
        "stream": False,
    }

    response = requests.post(
        LLM_API_URL,
        auth=(LLM_API_USER, LLM_API_PASS),
        headers=headers,
        json=data,
        verify=VERIFY_SSL
    )

    if response.status_code != 200:
        raise Exception(f"Failed to fetch response from API. Status code: {response.status_code}")

    response_data = response.json()
    content = response_data.get("content", "")
    
    output_lines = [line.strip() for line in content.splitlines() if line.strip()]

    return output_lines
