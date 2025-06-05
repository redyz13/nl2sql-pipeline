import os
import pandas as pd
from sqlalchemy import text
from schema_linking.config.config import (
    ACTIVE_TABLES_PATH,
    ACTIVE_FIELDS_PATH,
    FIELD_METADATA
)

fields_table = FIELD_METADATA["table"]
field_table_id_col = FIELD_METADATA["table_id_col"]

def get_active_tables(engine, min_rows=1, verbose=False):
    """
    Returns a DataFrame of all physical tables with at least `min_rows` rows.
    Uses cached file if available.
    """
    if os.path.exists(ACTIVE_TABLES_PATH):
        if verbose:
            print(f"Loading active tables from cache: {ACTIVE_TABLES_PATH}")
        return pd.read_parquet(ACTIVE_TABLES_PATH)

    query = """
        SELECT schemaname, tablename
        FROM pg_tables
        WHERE schemaname NOT IN ('pg_catalog', 'information_schema');
    """
    df_tables = pd.read_sql(query, engine)
    active_tables = []

    with engine.connect() as conn:
        for _, row in df_tables.iterrows():
            schema = row['schemaname']
            tablename = row['tablename']
            full_table = f'"{schema}"."{tablename}"'
            try:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {full_table}"))
                count = result.scalar()
                if count and count >= min_rows:
                    active_tables.append({"table": f"{schema}.{tablename}", "rows": count})
                    if verbose:
                        print(f"ACTIVE {schema}.{tablename}: {count} rows")
                elif verbose:
                    print(f"SKIP   {schema}.{tablename}: empty")
            except Exception as e:
                if verbose:
                    print(f"ERROR  {schema}.{tablename}: {e}")
                conn.rollback()
                continue

    df_active = pd.DataFrame(active_tables).sort_values(by="rows", ascending=False).reset_index(drop=True)
    os.makedirs(os.path.dirname(ACTIVE_TABLES_PATH), exist_ok=True)
    df_active.to_parquet(ACTIVE_TABLES_PATH)

    if verbose:
        print(f"\nFound {len(df_active)} active tables out of {len(df_tables)} total.")

    return df_active


def get_active_fields(engine, df_active_tables, verbose=True):
    """
    Filters fields_table to keep only fields that belong to active tables.
    Uses cached file if available.
    """
    if os.path.exists(ACTIVE_FIELDS_PATH):
        if verbose:
            print(f"Loading active fields from cache: {ACTIVE_FIELDS_PATH}")
        return pd.read_parquet(ACTIVE_FIELDS_PATH)

    table_names = df_active_tables['table'].str.extract(r'\.(.+)$')[0].tolist()

    df_fields = pd.read_sql(f"SELECT * FROM {fields_table}", engine)
    df_filtered = df_fields[df_fields[field_table_id_col].isin(table_names)].copy()

    os.makedirs(os.path.dirname(ACTIVE_FIELDS_PATH), exist_ok=True)
    df_filtered.to_parquet(ACTIVE_FIELDS_PATH)

    if verbose:
        print(f"Filtered {fields_table} from {len(df_fields)} to {len(df_filtered)} fields (matching active tables).")

    return df_filtered
