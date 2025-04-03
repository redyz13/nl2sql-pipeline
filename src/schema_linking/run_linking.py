import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from schema_linking.schema.extract_schema import extract_column_texts, extract_table_texts
from schema_linking.keywords.keyword_extractor import llama_keyword_extraction
from schema_linking.retrieval.retriever import build_or_load_index, retrieve_top_k
from schema_linking.llm.llama_linker import llama_table_linking, llama_column_linking
from schema_linking.utils.printer import (
    print_header,
    print_keywords,
    pretty_print_list,
    pretty_print_table,
    print_summary
)
from schema_linking.config.config import (
    TOP_K_TABLES, TOP_K_COLUMNS,
)

# Input question
question = "Quali sono le voci contabili registrate nel 2011 con la loro descrizione e codici associati?"
print("\nInput Question:", question)

# Step 1: Extract keywords using the LLM
print_header("Step 1: Extracting keywords using LLM...")
keywords = llama_keyword_extraction(question)
print_keywords(keywords)

# Step 2: Extract all available tables and columns from the schema
print_header("Step 2: Loading schema...")
table_texts = extract_table_texts()
column_texts = extract_column_texts()
print(f"Loaded {len(table_texts)} tables and {len(column_texts)} columns.")

# Step 3: FAISS-based pruning on tables
print_header(f"Step 3: FAISS pruning on tables (top {TOP_K_TABLES})")
table_index, table_map = build_or_load_index(table_texts, is_table=True)
pruned_tables = retrieve_top_k(table_index, table_map, question, TOP_K_TABLES)
pretty_print_table("Pruned Tables (FAISS)", pruned_tables)

# Step 4: FAISS-based pruning on columns
print_header(f"Step 4: FAISS pruning on columns (top {TOP_K_COLUMNS})")
column_index, column_map = build_or_load_index(column_texts, is_table=False)
pruned_columns = retrieve_top_k(column_index, column_map, question, TOP_K_COLUMNS)
pretty_print_list("Pruned Columns (FAISS)", pruned_columns)

# Step 5: Keep only columns that belong to the pruned tables
print_header("Step 5: Filtering columns that belong to pruned tables...")
filtered_columns = [col for col in pruned_columns if any(tbl in col for tbl in pruned_tables)]
pretty_print_list("Columns after filtering (FAISS + tables)", filtered_columns)

# Step 6: Refine table linking using the LLM
print_header("Step 6: LLM-based table linking...")
linked_tables = llama_table_linking(question, pruned_tables)
pretty_print_list("Linked Tables (LLM)", linked_tables)

# Step 7: Keep only columns that belong to the final linked tables
print_header("Step 7: Filtering columns that belong to LLM-linked tables...")
llm_filtered_columns = [col for col in filtered_columns if any(tbl in col for tbl in linked_tables)]
pretty_print_list("Columns after LLM table filtering", llm_filtered_columns)

# Step 8: Final column linking using the LLM
print_header("Step 8: LLM-based column linking...")
linked_columns = llama_column_linking(question, llm_filtered_columns)

# Output
print_summary(question, keywords, linked_tables, linked_columns)
