import gradio as gr
import pandas as pd
import tempfile
from zero_shot.api.executor import call_nl2sql_and_execute
from zero_shot.visualization.plot import generate_plot, get_plot_type, get_supported_kinds
from zero_shot.config.config import APP_ENV, MAX_RESULT_ROWS

def run_query(question, selected_kind=""):
    sql, df = call_nl2sql_and_execute(question)

    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame([["Invalid DataFrame"]], columns=["Error"])
    elif df.empty:
        df = pd.DataFrame([["No results found."]], columns=["Message"])

    kind = None if selected_kind in (None, "", "auto") else selected_kind
    plot_img, _ = generate_plot(df.copy(), kind=kind)
    df_display = df.head(MAX_RESULT_ROWS)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, newline="", encoding="utf-8") as f:
        df.to_csv(f.name, index=False)
        csv_path = f.name

    return (
        sql,
        gr.update(value=df_display, visible=True),
        gr.update(value=plot_img, visible=bool(plot_img)),
        gr.update(value=csv_path, visible=False),
        gr.update(value=csv_path, visible=True),
    )

def update_preview_and_dropdown(question: str):
    try:
        sql, df = call_nl2sql_and_execute(question)

        msg = "⚠️ No data returned."
        dropdown = gr.update(choices=[""], value="", interactive=False)

        if isinstance(df, pd.DataFrame) and not df.empty:
            df_preview = df.iloc[:20, :10]
            kind = get_plot_type(df_preview)
            msg = f"📊 Expected chart type: {kind.capitalize()}" if kind else "⚠️ No valid chart type detected."

            kinds = ["auto"] + get_supported_kinds(df)
            dropdown = gr.update(choices=kinds, value="auto", interactive=True)

        return msg, dropdown

    except Exception:
        return "⚠️ Error during preview.", gr.update(choices=["auto"], value="auto", interactive=True)

with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align: center;'>NL2SQL</h1>")
    gr.Markdown(f"<p style='text-align: center;'>Environment: <code>{APP_ENV or 'undefined'}</code></p>")

    question = gr.Textbox(label="✏️ Natural Language Question", lines=2)
    kind_preview = gr.Textbox(label="🔎 Predicted Chart Type", visible=True, interactive=False)

    chart_kind = gr.Dropdown(
        label="📂 Select Chart Type",
        choices=[""],
        value="",
        interactive=False
    )

    with gr.Row():
        clear_btn = gr.Button("Clear", variant="secondary")
        run_btn = gr.Button("Submit", variant="primary")

    sql_output = gr.Textbox(label="🧠 Generated SQL Query", lines=2)
    df_output = gr.Dataframe(label=f"Query result (max {MAX_RESULT_ROWS} rows)", visible=False)
    download_btn = gr.DownloadButton("📥 Export to CSV", value=None, visible=False)
    img_plot = gr.Image(label="📊 Chart", visible=False, type="pil")
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
        inputs=[question, chart_kind],
        outputs=[sql_output, df_output, img_plot, file_output, download_btn]
    )

    clear_btn.click(
        fn=lambda: (
            "", "", gr.update(value=None, visible=False), gr.update(visible=False),
            gr.update(value=None, visible=False), ""
        ),
        inputs=None,
        outputs=[question, sql_output, df_output, img_plot, download_btn, kind_preview]
    )

    question.change(
        fn=update_preview_and_dropdown,
        inputs=question,
        outputs=[kind_preview, chart_kind],
        show_progress=False
    )

demo.launch(server_name="0.0.0.0")
