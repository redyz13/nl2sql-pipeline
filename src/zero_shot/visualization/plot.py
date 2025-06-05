import pandas as pd
import matplotlib.pyplot as plt
import io
from PIL import Image

def generate_plot(df: pd.DataFrame) -> Image.Image | None:
    if df.shape[1] < 2 or df.shape[0] < 2:
        return None

    x_col = df.columns[0]
    y_col = None

    for col in df.columns[1:]:
        if pd.api.types.is_numeric_dtype(df[col]):
            y_col = col
            break
    if y_col is None:
        for col in df.columns[1:]:
            try:
                df[col] = pd.to_numeric(df[col])
                y_col = col
                break
            except Exception:
                continue
        if y_col is None:
            return None

    fig, ax = plt.subplots(figsize=(7, 4), dpi=300)
    df_plot = df.head(50)

    if pd.api.types.is_datetime64_any_dtype(df[x_col]):
        df_plot.plot(kind="line", x=x_col, y=y_col, ax=ax)
        plt.title("Auto-generated Line Chart")
    elif df_plot[x_col].nunique() <= 4 and df_plot.shape[0] <= 10:
        pie_data = df_plot[[x_col, y_col]].dropna()
        pie_data = pie_data[pie_data[y_col] > 0]
        if pie_data.empty:
            return None
        ax.pie(pie_data[y_col], labels=pie_data[x_col], autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        plt.title("Auto-generated Pie Chart")
    else:
        df_plot.plot(kind="bar", x=x_col, y=y_col, ax=ax)
        plt.title("Auto-generated Barplot")

    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    return Image.open(buf)
