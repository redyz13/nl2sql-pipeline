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

    df_plot = df.copy()
    df_plot = df_plot[(df_plot[y_col].notna()) & (df_plot[y_col] > 0)]
    if df_plot.shape[0] < 2:
        return None

    df_plot = df_plot.sort_values(by=y_col, ascending=False).head(20)

    if pd.api.types.is_datetime64_any_dtype(df_plot[x_col]):
        kind = "line"
    elif pd.api.types.is_numeric_dtype(df_plot[x_col]) and pd.api.types.is_numeric_dtype(df_plot[y_col]):
        kind = "scatter"
    elif df_plot[x_col].nunique() <= 4 and df_plot.shape[0] <= 10:
        kind = "pie"
    else:
        kind = "barh" if df_plot[x_col].astype(str).str.len().max() > 25 else "bar"

    fig, ax = plt.subplots(figsize=(8, 5), dpi=250)

    if kind == "pie":
        pie_data = df_plot[[x_col, y_col]].dropna()
        pie_data = pie_data[pie_data[y_col] > 0]
        if pie_data.empty:
            return None
        ax.pie(pie_data[y_col], labels=pie_data[x_col], autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
    else:
        df_plot.plot(kind=kind, x=x_col, y=y_col, ax=ax)

    plt.title(f"{kind.capitalize()} plot: {y_col} vs {x_col}", fontsize=14)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    return Image.open(buf)
