import pandas as pd
import matplotlib.pyplot as plt
import io
from PIL import Image
from zero_shot.config.config import (
    MAX_PLOT_POINTS, PLOT_BLACKLIST,
    MIN_PLOT_ROWS, MIN_PLOT_COLS,
    MIN_DISTINCT_Y, MAX_PIE_UNIQUE,
    MAX_PIE_ROWS, LABEL_LENGTH_THRESHOLD,
    PLOT_FIGSIZE, PLOT_DPI
)

def generate_plot(df: pd.DataFrame) -> Image.Image | None:
    if df.shape[1] < MIN_PLOT_COLS or df.shape[0] < MIN_PLOT_ROWS:
        return None

    x_col = df.columns[0]

    y_col = next((col for col in df.columns[1:] if pd.api.types.is_numeric_dtype(df[col])), None)
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

    if x_col.upper() in PLOT_BLACKLIST or y_col.upper() in PLOT_BLACKLIST:
        return None

    df_plot = df[[x_col, y_col]].copy()
    df_plot = df_plot[(df_plot[y_col].notna()) & (df_plot[y_col] > 0)]
    if df_plot.shape[0] < MIN_PLOT_ROWS or df_plot[y_col].nunique() < MIN_DISTINCT_Y:
        return None

    is_x_date = pd.api.types.is_datetime64_any_dtype(df_plot[x_col])
    if is_x_date:
        df_plot = df_plot.sort_values(by=x_col)
    else:
        df_plot = df_plot.sort_values(by=y_col, ascending=False).head(MAX_PLOT_POINTS)

    if is_x_date:
        kind = "line"
    elif pd.api.types.is_numeric_dtype(df_plot[x_col]) and pd.api.types.is_numeric_dtype(df_plot[y_col]):
        kind = "scatter"
    elif df_plot[x_col].nunique() <= MAX_PIE_UNIQUE and df_plot.shape[0] <= MAX_PIE_ROWS:
        kind = "pie"
    else:
        kind = "barh" if df_plot[x_col].astype(str).str.len().max() > LABEL_LENGTH_THRESHOLD else "bar"

    fig, ax = plt.subplots(figsize=PLOT_FIGSIZE, dpi=PLOT_DPI)

    if kind == "pie":
        pie_data = df_plot.dropna()
        ax.pie(pie_data[y_col], labels=pie_data[x_col], autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
    elif kind == "scatter":
        ax.scatter(df_plot[x_col], df_plot[y_col])
    else:
        df_plot.plot(kind=kind, x=x_col, y=y_col, ax=ax)

    ax.set_title(f"{kind.capitalize()} plot: {y_col} vs {x_col}", fontsize=14)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    return Image.open(buf)
