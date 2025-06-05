import gradio as gr
import pandas as pd
import tempfile
from zero_shot.api.executor import call_nl2sql_and_execute
from zero_shot.config.config import APP_ENV
from zero_shot.visualization.plot import generate_plot

def run_query(question):
    sql, df = call_nl2sql_and_execute(question)

    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame([["Invalid DataFrame"]], columns=["Error"])
    elif df.empty:
        df = pd.DataFrame([["No results found."]], columns=["Message"])

    plot_img = generate_plot(df)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, newline="", encoding="utf-8") as f:
        df.to_csv(f.name, index=False)
        csv_path = f.name

    return (
        sql,
        gr.update(value=df, visible=True),
        gr.update(value=plot_img, visible=bool(plot_img)),
        gr.update(value=csv_path, visible=False),
        gr.update(value=csv_path, visible=True),
    )

with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align: center;'>NL2SQL UI</h1>")
    gr.Markdown(f"<p style='text-align: center;'>Environment: <code>{APP_ENV or 'undefined'}</code></p>")

    question = gr.Textbox(label="Natural language question", lines=2)

    with gr.Row():
        clear_btn = gr.Button("Clear", variant="secondary")
        run_btn = gr.Button("Submit", variant="primary")

    sql_output = gr.Textbox(label="Generated SQL query", lines=6)
    df_output = gr.Dataframe(label="Query result (max 50 rows)", visible=False)
    
    download_btn = gr.DownloadButton("📥 Export to CSV", value=None, visible=False)
    img_plot = gr.Image(label="📊 Auto-generated Chart", visible=False, type="pil")
    
    file_output = gr.File(visible=False)

    run_btn.click(
        fn=lambda: (
            gr.update(value=""),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
        ),
        inputs=None,
        outputs=[sql_output, df_output, img_plot, file_output, download_btn],
        queue=False
    )

    run_btn.click(
        fn=run_query,
        inputs=question,
        outputs=[sql_output, df_output, img_plot, file_output, download_btn]
    )

    clear_btn.click(
        fn=lambda: (
            "", "", gr.update(value=None, visible=False), gr.update(visible=False), gr.update(value=None, visible=False)
        ),
        inputs=None,
        outputs=[question, sql_output, df_output, img_plot, download_btn]
    )

demo.launch(server_name="0.0.0.0")
