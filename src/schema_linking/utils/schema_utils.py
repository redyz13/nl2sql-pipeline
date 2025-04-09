def build_table_description_map(pruned_columns: list[str]) -> dict[str, str]:
    """
    Extracts a mapping from table_id to table description
    based on the 'pruned_columns' strings of the form:
    'table.column: column description (tabella: table description)'
    """
    table_desc_map = {}
    for col in pruned_columns:
        if "(tabella:" in col:
            try:
                table_col, desc = col.split(": ", 1)
                table_id = table_col.split(".")[0]
                table_description = desc.split("(tabella:")[1].strip(" )")
                table_desc_map[table_id] = table_description
            except Exception:
                continue
    return table_desc_map


def build_column_description_map(pruned_columns: list[str]) -> dict[str, str]:
    """
    Extracts a mapping from table.column to its full description line.
    Useful for passing rich context to LLM during final column linking.
    """
    return {
        col.split(":")[0].strip(): col.strip()
        for col in pruned_columns
        if ": " in col
    }
