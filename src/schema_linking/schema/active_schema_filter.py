import pandas as pd
from sqlalchemy import text

def get_active_tables(engine, min_rows=1, verbose=False):
    """
    Scans the database and returns a DataFrame of all physical tables 
    that contain at least `min_rows` rows (default: 1).
    
    Parameters:
        engine: SQLAlchemy database engine
        min_rows: Minimum number of rows to consider a table 'active'
        verbose: Whether to print progress and summary

    Returns:
        DataFrame with columns: [table, rows]
    """

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
                else:
                    if verbose:
                        print(f"SKIP   {schema}.{tablename}: empty")
            except Exception as e:
                if verbose:
                    print(f"ERROR  {schema}.{tablename}: {e}")
                conn.rollback()
                continue

    df_active = pd.DataFrame(active_tables).sort_values(by="rows", ascending=False).reset_index(drop=True)
    
    if verbose:
        print(f"\nFound {len(df_active)} active tables out of {len(df_tables)} total.")
    
    return df_active


def get_active_fields(engine, df_active_tables, table_fields_name="ba_table_fields", verbose=True):
    """
    Filters the ba_table_fields table to keep only fields (columns) 
    that belong to active tables.
    
    Parameters:
        engine: SQLAlchemy engine
        df_active_tables: DataFrame with 'table' column in format 'schema.tablename'
        table_fields_name: name of the table containing fields metadata
        verbose: Whether to print stats

    Returns:
        DataFrame with only fields belonging to active tables
    """

    table_names = df_active_tables['table'].str.extract(r'\.(.+)$')[0].tolist()
    
    df_fields = pd.read_sql(f"SELECT * FROM {table_fields_name}", engine)
    
    df_filtered = df_fields[df_fields['fltableid'].isin(table_names)].copy()

    if verbose:
        print(f"Filtered ba_table_fields from {len(df_fields)} to {len(df_filtered)} fields (matching active tables).")

    return df_filtered