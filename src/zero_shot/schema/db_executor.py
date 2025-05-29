import pandas as pd
from sqlalchemy import create_engine, text
from zero_shot.config.config import DATABASE_URL

def is_safe_sql(sql: str) -> bool:
    return sql.strip().lower().startswith("select")

def run_sql_query(sql: str) -> pd.DataFrame:
    engine = create_engine(DATABASE_URL)
    try:
        return pd.read_sql_query(sql, engine)
    except Exception as e:
        print(f"[Fallback] read_sql_query failed: {e}")
        with engine.connect() as connection:
            result = connection.execute(text(sql))
            rows = result.mappings().all()
            return pd.DataFrame(rows)
