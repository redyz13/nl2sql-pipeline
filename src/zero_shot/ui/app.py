import gradio as gr
import requests
from zero_shot.config.config import APP_ENV, API_URL

def call_nl2sql_api(question):
    try:
        response = requests.post(API_URL, json={"question": question})
        response.raise_for_status()
        return response.json().get("sql", "[No SQL returned]")
    except Exception as e:
        return f"[ERROR] {str(e)}"

gr.Interface(
    fn=call_nl2sql_api,
    inputs=gr.Textbox(label="Natural language question", lines=2),
    outputs=gr.Textbox(label="Generated SQL query", lines=6),
    title="NL2SQL UI",
    description=f"Environment: {APP_ENV or 'undefined'}",
    flagging_mode="never"
).launch(server_name="0.0.0.0")
