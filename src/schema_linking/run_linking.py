import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from schema_linking.config.config import TOP_K_COLUMNS
from schema_linking.schema.extract_schema import extract_active_column_texts
from schema_linking.keywords.keyword_extractor import llm_keyword_extraction
from schema_linking.retrieval.retriever import build_or_load_index, retrieve_top_k
from schema_linking.llm.llm_linker import llm_table_linking, llm_column_linking, llm_filter_columns_by_keywords
from schema_linking.utils.printer import (
    print_header,
    print_keywords,
    pretty_print_list,
    print_summary
)
from schema_linking.utils.schema_utils import (
    build_table_description_map,
    build_column_description_map
)

print_header("Input")
question = "Qual è l'indirizzo e la località delle banche con codice CAB 12345?"
print(f"Question: {question}")

print_header("Step 1: Extracting keywords using LLM...")
keywords = llm_keyword_extraction(question)
print_keywords(keywords)

print_header("Step 2: Loading schema...")
column_texts = extract_active_column_texts()
print(f"Loaded {len(column_texts)} columns")

print_header(f"Step 3: FAISS column pruning (top {TOP_K_COLUMNS}) using keywords...")
column_index, column_map = build_or_load_index(column_texts)
pruned_columns = retrieve_top_k(column_index, column_map, question, TOP_K_COLUMNS)

if not pruned_columns:
    print("\nNo columns retrieved by FAISS pruning.")
    exit()

pretty_print_list("Pruned Columns (FAISS)", pruned_columns)

print_header("Step 4: LLM filtering on pruned columns...")
llm_filtered_columns = llm_filter_columns_by_keywords(question, pruned_columns, keywords)

if not llm_filtered_columns:
    print("\nNo columns passed the LLM filtering.")
    exit()

pretty_print_list("Filtered Columns (LLM)", llm_filtered_columns)

print_header("Step 5: LLM-based table linking (using filtered columns)...")
table_desc_map = build_table_description_map(pruned_columns)
candidate_tables = list(set(col.split('.')[0] for col in llm_filtered_columns))
tables_with_desc = [f"{table}: {table_desc_map.get(table, 'nessuna descrizione')}" for table in candidate_tables]

linked_tables = llm_table_linking(question, tables_with_desc)

if not linked_tables:
    print("\nNo tables linked by LLM.")
    exit()

pretty_print_list("Linked Tables (LLM)", linked_tables)

print_header("Step 6: LLM-based final column linking...")
final_columns = [col for col in llm_filtered_columns if col.split('.')[0] in linked_tables]
column_full_map = build_column_description_map(pruned_columns)
final_column_descriptions = [column_full_map[c] for c in final_columns if c in column_full_map]

linked_columns = llm_column_linking(question, final_column_descriptions)

if not linked_columns:
    print("\nNo columns linked by LLM.")
    exit()

print_summary(question, keywords, linked_tables, linked_columns)