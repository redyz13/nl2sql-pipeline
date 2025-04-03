import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from schema_linking.schema.extract_schema import extract_column_texts
from schema_linking.keywords.keyword_extractor import llama_keyword_extraction
from schema_linking.retrieval.retriever import build_or_load_index, retrieve_top_k
from schema_linking.llm.llama_linker import llama_table_linking, llama_column_linking, llama_filter_columns_by_keywords
from schema_linking.utils.printer import (
    print_header,
    print_keywords,
    pretty_print_list,
    pretty_print_table,
    print_summary
)
from schema_linking.config.config import (
    TOP_K_COLUMNS,
)

print_header("Input")
question = "Quali sono le descrizioni di rigo delle voci contabili del 2011?"

print_header("Step 1: Extracting keywords using LLM...")
keywords = llama_keyword_extraction(question)
print_keywords(keywords)
keyword_string = " ".join(keywords)

print_header("Step 2: Loading schema...")
column_texts = extract_column_texts()

print_header(f"Step 3: FAISS column pruning (top {TOP_K_COLUMNS}) using keywords...")
column_index, column_map = build_or_load_index(column_texts)
pruned_columns = retrieve_top_k(column_index, column_map, keyword_string, TOP_K_COLUMNS)

if not pruned_columns:
    print("\nNo columns retrieved by FAISS pruning.")
    exit()

pretty_print_list("Pruned Columns (FAISS)", pruned_columns)

print_header("Step 4: LLM filtering on pruned columns...")
llm_filtered_columns = llama_filter_columns_by_keywords(keyword_string, pruned_columns, keywords)

if not llm_filtered_columns:
    print("\nNo columns passed the LLM filtering.")
    exit()

pretty_print_list("Filtered Columns (LLM)", llm_filtered_columns)

print_header("Step 5: LLM-based table linking (using filtered columns)...")
candidate_tables = list(set([col.split('.')[0] for col in llm_filtered_columns]))
pretty_print_list("Candidate Tables", candidate_tables)

linked_tables = llama_table_linking(question, candidate_tables)

if not linked_tables:
    print("\nNo tables linked by LLM.")
    exit()

pretty_print_list("Linked Tables (LLM)", linked_tables)

print_header("Step 6: LLM-based final column linking...")
final_columns = [col for col in llm_filtered_columns if col.split('.')[0] in linked_tables]
linked_columns = llama_column_linking(keyword_string, final_columns)

if not linked_columns:
    print("\nNo columns linked by LLM.")
    exit()

print_summary(question, keywords, linked_tables, linked_columns)