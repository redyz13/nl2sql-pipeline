import requests
import json
from schema_linking.config.config import LLAMA_API_URL, LLAMA_API_USER, LLAMA_API_PASS, VERIFY_SSL

def send_prompt(prompt: str) -> list[str]:
    formatted_prompt = (
        "<|begin_of_text|>"
        "<|start_header_id|>system<|end_header_id|>\n\n"
        "Cutting Knowledge Date: December 2023\n"
        "Today Date: 2 Apr 2025\n\n"
        "You are a helpful AI assistant.\n"
        "<|eot_id|>"
        "<|start_header_id|>user<|end_header_id|>\n\n"
        f"{prompt}\n"
        "<|eot_id|>"
        "<|start_header_id|>assistant<|end_header_id|>"
    )

    headers = {"Content-Type": "application/json"}
    data = {
        "prompt": formatted_prompt,
        "stream": False
    }

    response = requests.post(
        LLAMA_API_URL,
        auth=(LLAMA_API_USER, LLAMA_API_PASS),
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
