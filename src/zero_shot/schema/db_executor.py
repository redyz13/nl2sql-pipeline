import pandas as pd
from sqlalchemy import create_engine
from zero_shot.config.config import DATABASE_URL

def is_safe_sql(sql: str) -> bool:
    return sql.strip().lower().startswith("select")

def run_sql_query(sql: str) -> pd.DataFrame:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        return pd.read_sql_query(sql, connection)
