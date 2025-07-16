import pandas as pd
import matplotlib.pyplot as plt
import io
from PIL import Image
from zero_shot.config.config import (
    MAX_POINTS, PLOT_BLACKLIST, MIN_PLOT_ROWS, MIN_PLOT_COLS,
    MIN_DISTINCT_Y, LABEL_LENGTH_THRESHOLD, PLOT_FIGSIZE, PLOT_DPI,
    VALID_KINDS, MAX_PIE_CATEGORIES
)

def try_parse_datetime_column(df: pd.DataFrame, col: str) -> pd.DataFrame:
    if not pd.api.types.is_numeric_dtype(df[col]):
        try:
            df[col] = pd.to_datetime(df[col])
        except Exception:
            pass
    return df

def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame | None:
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
    df_plot = df_plot[df_plot[y_col].notna()]
    if (df_plot[y_col] > 0).sum() >= MIN_PLOT_ROWS:
        df_plot = df_plot[df_plot[y_col] > 0]

    if df_plot.shape[0] < MIN_PLOT_ROWS or df_plot[y_col].nunique() < MIN_DISTINCT_Y:
        return None

    return df_plot

def determine_kind(df_plot: pd.DataFrame) -> str | None:
    x_col, y_col = df_plot.columns[0], df_plot.columns[1]

    is_x_date = False
    if not pd.api.types.is_numeric_dtype(df_plot[x_col]):
        try:
            df_plot[x_col] = pd.to_datetime(df_plot[x_col])
            is_x_date = True
        except Exception:
            pass

    if is_x_date:
        return "line"
    if pd.api.types.is_numeric_dtype(df_plot[x_col]) and pd.api.types.is_numeric_dtype(df_plot[y_col]):
        return "scatter"
    if df_plot[x_col].nunique() <= MAX_PIE_CATEGORIES:
        return "pie"
    if df_plot[x_col].astype(str).str.len().max() > LABEL_LENGTH_THRESHOLD:
        return "barh"
    return "bar"

def get_plot_type(df: pd.DataFrame) -> str | None:
    df_plot = preprocess_dataframe(df)
    if df_plot is None:
        return None
    return determine_kind(df_plot)

def is_kind_supported(df_plot: pd.DataFrame, kind: str) -> bool:
    if kind not in VALID_KINDS:
        return False

    x_col, y_col = df_plot.columns[0], df_plot.columns[1]

    if kind == "pie":
        return df_plot[x_col].nunique() <= MAX_PIE_CATEGORIES

    if kind == "bar":
        return df_plot[x_col].astype(str).str.len().max() <= LABEL_LENGTH_THRESHOLD

    if kind == "scatter":
        return (
            pd.api.types.is_numeric_dtype(df_plot[x_col]) and
            pd.api.types.is_numeric_dtype(df_plot[y_col])
        )

    return True

def generate_plot(df: pd.DataFrame, kind: str | None = None) -> tuple[Image.Image | None, str | None]:
    df_plot = preprocess_dataframe(df)
    if df_plot is None:
        return None, None

    if kind is None:
        kind = determine_kind(df_plot)
    elif kind not in VALID_KINDS:
        return None, None

    x_col, y_col = df_plot.columns[0], df_plot.columns[1]

    if kind == "line":
        df_plot = try_parse_datetime_column(df_plot, x_col)
        df_plot = df_plot.sort_values(by=x_col)
    else:
        df_plot = df_plot.sort_values(by=y_col, ascending=False)

    df_plot = df_plot.head(MAX_POINTS.get(kind, 20))

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

    return Image.open(buf), kind

def get_supported_kinds(df: pd.DataFrame) -> list[str]:
    kinds = []
    df_plot = preprocess_dataframe(df)
    if df_plot is None:
        return kinds

    for kind in VALID_KINDS:
        if not is_kind_supported(df_plot, kind):
            continue
        try:
            img, _ = generate_plot(df.copy(), kind=kind)
            if img:
                kinds.append(kind)
        except:
            continue
    return kinds
