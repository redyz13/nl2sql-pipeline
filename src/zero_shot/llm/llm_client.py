from openai import OpenAI
from zero_shot.config.config import OPENAI_API_KEY, OPENAI_MODEL_ID

client = OpenAI(api_key=OPENAI_API_KEY)

def send_prompt(prompt: str) -> list[str]:
    response = client.chat.completions.create(
        model=OPENAI_MODEL_ID,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    content = response.choices[0].message.content
    return content.strip().split("\n")
