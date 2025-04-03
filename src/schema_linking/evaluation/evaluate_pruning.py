from schema_linking.retrieval.retriever import build_or_load_index, retrieve_top_k
from schema_linking.schema.extract_schema import extract_table_texts
from schema_linking.config.config import TOP_K_TABLES

test_set = [
    {
        "question": "query: Quali sono le voci contabili registrate nel 2011 con la loro descrizione e codici associati?",
        "expected_tables": ["ap_compdic"]
    }
]

table_texts = extract_table_texts()
table_index, table_map = build_or_load_index(table_texts, is_table=True)

all_recalls = []

for example in test_set:
    question = example["question"]
    expected_tables = example["expected_tables"]

    result = retrieve_top_k(table_index, table_map, question, TOP_K_TABLES)
    pruned_tables = result[0] if isinstance(result, tuple) else result

    matched = sum(1 for t in expected_tables if any(t in pt for pt in pruned_tables))
    recall = matched / len(expected_tables)
    all_recalls.append(recall)

    print(f"Input Question: {question}")
    print(f"Recall@{TOP_K_TABLES}: {recall:.2f}")

    if recall == 1.0 and len(expected_tables) == 1:
        print("Exact match found!")

mean_recall = sum(all_recalls) / len(all_recalls)
print(f"Mean Recall@{TOP_K_TABLES}: {mean_recall:.2f}")
