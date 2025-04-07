import pandas as pd
from sqlalchemy import create_engine
from schema_linking.schema.active_schema_filter import get_active_tables, get_active_fields
from schema_linking.config.config import (
    DATABASE_URL,
    TABLE_METADATA,
    FIELD_METADATA
)

engine = create_engine(DATABASE_URL)

tables_table = TABLE_METADATA["table"]
table_id_col = TABLE_METADATA["id_col"]
table_descr_col = TABLE_METADATA["description_col"]

fields_table = FIELD_METADATA["table"]
field_table_col = FIELD_METADATA["table_id_col"]
field_id_col = FIELD_METADATA["field_id_col"]
field_descr_col = FIELD_METADATA["description_col"]


def extract_column_texts() -> list[str]:
    df_tables = pd.read_sql(f"SELECT {table_id_col}, {table_descr_col} FROM {tables_table}", engine)
    df_fields = pd.read_sql(f"SELECT {field_table_col}, {field_id_col}, {field_descr_col} FROM {fields_table}", engine)

    df_tables = df_tables.rename(columns={table_id_col: "table_id", table_descr_col: "table_description"})
    df_fields = df_fields.rename(columns={
        field_table_col: "table_id",
        field_id_col: "field_name",
        field_descr_col: "field_description"
    })

    df_merged = df_fields.merge(df_tables, on="table_id", how="left")

    column_texts = [
        f"{row['table_id']}.{row['field_name']}: {row['field_description'] or 'nessuna descrizione'} (tabella: {row['table_description'] or 'nessuna descrizione'})"
        for _, row in df_merged.iterrows()
    ]

    return column_texts


def extract_active_column_texts() -> list[str]:
    df_active_tables = get_active_tables(engine, min_rows=1)
    df_active_fields = get_active_fields(engine, df_active_tables)

    df_tables = pd.read_sql(f"SELECT {table_id_col}, {table_descr_col} FROM {tables_table}", engine)
    df_tables = df_tables.rename(columns={table_id_col: "table_id", table_descr_col: "table_description"})

    df_fields = df_active_fields.rename(columns={
        field_table_col: "table_id",
        field_id_col: "field_name",
        field_descr_col: "field_description"
    })

    df_merged = df_fields.merge(df_tables, on="table_id", how="left")

    column_texts = [
        f"{row['table_id']}.{row['field_name']}: {row['field_description'] or 'nessuna descrizione'} (tabella: {row['table_description'] or 'nessuna descrizione'})"
        for _, row in df_merged.iterrows()
    ]

    return column_texts