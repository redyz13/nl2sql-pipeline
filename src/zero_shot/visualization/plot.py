import pandas as pd
import matplotlib.pyplot as plt
import io
from PIL import Image

def generate_plot(df: pd.DataFrame) -> Image.Image | None:
    if df.shape[1] < 2 or df.shape[0] < 2:
        return None

    for col in df.columns[1:]:
        if pd.api.types.is_numeric_dtype(df[col]):
            x_col = df.columns[0]
            y_col = col
            break
    else:
        for col in df.columns[1:]:
            try:
                df[col] = pd.to_numeric(df[col])
                x_col = df.columns[0]
                y_col = col
                break
            except Exception:
                continue
        else:
            return None

    fig, ax = plt.subplots(figsize=(7, 4), dpi=300)
    df.head(50).plot(kind="bar", x=x_col, y=y_col, ax=ax)
    plt.title("Auto-generated Barplot", fontsize=14)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    return Image.open(buf)
