from flask_cors import cross_origin
from zero_shot.config.config import ALLOWED_ORIGINS
from zero_shot.llm.llm_linker import llm_generate_sql

@cross_origin(origins=ALLOWED_ORIGINS)
def query_post(body):
    question = body["question"]
    sql_lines = llm_generate_sql(question)
    return {"sql": "\n".join(sql_lines)}
