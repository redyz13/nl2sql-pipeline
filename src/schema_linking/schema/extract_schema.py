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
        f"La colonna '{row['field_name']}' rappresenta {row['field_description'].rstrip('.') if pd.notnull(row['field_description']) else 'una informazione'} "
        f"nella tabella '{row['table_id']}', che contiene {row['table_description'].rstrip('.') if pd.notnull(row['table_description']) else 'dati specifici'}."
        for _, row in df_merged.iterrows()
    ]

    return column_texts

def extract_table_texts():
    engine = create_engine(DATABASE_URL)
    df_tables = pd.read_sql("SELECT dttableid, dtdescri FROM public.ba_table_mod", engine)
    df_fields = pd.read_sql("SELECT fltableid, flfieldid, fldescri FROM public.ba_table_fields", engine)

    df_tables = df_tables.rename(columns={"dttableid": "table_id", "dtdescri": "table_description"})
    df_fields = df_fields.rename(columns={"fltableid": "table_id", "flfieldid": "field_name", "fldescri": "field_description"})

    grouped_fields = df_fields.groupby("table_id").apply(
        lambda g: "; ".join(
            f"{row['field_name']} ({row['field_description']})"
            for _, row in g.iterrows() if pd.notnull(row['field_description'])
        )
    ).reset_index(name="column_descriptions")

    df_tables = df_tables.merge(grouped_fields, on="table_id", how="left")

    table_texts = [
        f"La tabella '{row['table_id']}' rappresenta {row['table_description'].rstrip('.')}. "
        f"Include colonne come: {row['column_descriptions']}."
        for _, row in df_tables.iterrows()
        if pd.notnull(row['table_description'])
    ]

    return table_texts