import pandas as pd
import requests
from zero_shot.config.config import API_URL, MAX_RESULT_ROWS
from zero_shot.schema.db_executor import is_safe_sql, run_sql_query

def call_nl2sql_and_execute(question: str):
    try:
        response = requests.post(API_URL, json={"question": question})
        response.raise_for_status()
        raw_sql = response.json().get("sql", "[No SQL returned]")
        sql = raw_sql.strip().removeprefix("```sql").removesuffix("```").strip()

        if not is_safe_sql(sql):
            return sql, pd.DataFrame([["Only SELECT queries are allowed."]], columns=["Error"])

        df = run_sql_query(sql)
        return sql, df.head(MAX_RESULT_ROWS) if not df.empty else pd.DataFrame([["No results found."]], columns=["Message"])

    except Exception as e:
        return "[ERROR]", pd.DataFrame([[str(e)]], columns=["Error"])
