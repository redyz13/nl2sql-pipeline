import os
import pandas as pd
from sqlalchemy import create_engine
from zero_shot_openai.config.config import (
    DATABASE_URL,
    TABLES,
    TABLE_METADATA,
    FIELD_METADATA,
    PROMPT_PATHS,
)

def generate_schema_prompt(force: bool = False):
    output_path = PROMPT_PATHS["schema"]

    if os.path.exists(output_path) and not force:
        print(f"The file '{output_path}' already exists. Skipping generation.")
        return

    engine = create_engine(DATABASE_URL)

    fields_df = pd.read_sql(f"SELECT * FROM {FIELD_METADATA['table']}", engine)
    tables_df = pd.read_sql(f"SELECT * FROM {TABLE_METADATA['table']}", engine)

    output_lines = []

    for logical_table in TABLES:
        physical_table = f"{logical_table}001"

        table_row = tables_df.loc[tables_df[TABLE_METADATA["id_col"]] == logical_table]
        table_descr = table_row[TABLE_METADATA["description_col"]].squeeze() if not table_row.empty else ""
        table_descr = table_descr.strip() if table_descr else "no description available"

        output_lines.append(f"### Tabella: {physical_table}")

        fields = fields_df[fields_df[FIELD_METADATA["table_id_col"]] == logical_table]
        for _, row in fields.iterrows():
            col_name = row[FIELD_METADATA["field_id_col"]]
            col_descr = row[FIELD_METADATA["description_col"]] or "no description available"
            output_lines.append(f"- {col_name}: {col_descr.strip()}")

        output_lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    print(f"File '{output_path}' successfully generated.")
