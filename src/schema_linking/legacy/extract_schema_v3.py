import pandas as pd
from sqlalchemy import create_engine
from schema_linking.config.config import DATABASE_URL

def extract_column_texts():
    engine = create_engine(DATABASE_URL)
    df_tables = pd.read_sql("SELECT dttableid, dtdescri FROM public.ba_table_mod", engine)
    df_fields = pd.read_sql("SELECT fltableid, flfieldid, fldescri FROM public.ba_table_fields", engine)

    df_tables = df_tables.rename(columns={"dttableid": "table_id", "dtdescri": "table_description"})
    df_fields = df_fields.rename(columns={"fltableid": "table_id", "flfieldid": "field_name", "fldescri": "field_description"})

    df_merged = df_fields.merge(df_tables, on="table_id", how="left")

    column_texts = [
        f"{row['table_id']}.{row['field_name']}: {row['field_description'] or 'nessuna descrizione'}"
        for _, row in df_merged.iterrows()
    ]

    return column_texts
