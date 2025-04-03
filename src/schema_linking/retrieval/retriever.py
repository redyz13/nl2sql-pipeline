import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from schema_linking.config.config import (
    EMBEDDING_MODEL,
    TABLE_INDEX_BIN, TABLE_MAPPING_PKL,
    COLUMN_INDEX_BIN, COLUMN_MAPPING_PKL
)

embedder = SentenceTransformer(EMBEDDING_MODEL)

def build_faiss_index(schema_texts, index_bin, mapping_pkl):
    print(f"Building FAISS index → {index_bin}")
    
    embeddings = embedder.encode(
        schema_texts,
        convert_to_numpy=True,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    mapping = {i: text for i, text in enumerate(schema_texts)}
    
    faiss.write_index(index, index_bin)
    with open(mapping_pkl, "wb") as f:
        pickle.dump(mapping, f)

    return index, mapping

def load_faiss_index(index_bin, mapping_pkl):
    print(f"Loading FAISS index from disk → {index_bin}")
    index = faiss.read_index(index_bin)
    with open(mapping_pkl, "rb") as f:
        mapping = pickle.load(f)
    return index, mapping

def build_or_load_index(schema_texts, is_table):
    if is_table:
        index_bin = TABLE_INDEX_BIN
        mapping_pkl = TABLE_MAPPING_PKL
    else:
        index_bin = COLUMN_INDEX_BIN
        mapping_pkl = COLUMN_MAPPING_PKL

    if os.path.exists(index_bin) and os.path.exists(mapping_pkl):
        return load_faiss_index(index_bin, mapping_pkl)
    else:
        return build_faiss_index(schema_texts, index_bin, mapping_pkl)

def retrieve_top_k(index, mapping, query, top_k):
    query_embedding = embedder.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    distances, indices = index.search(query_embedding, top_k)
    for i, (idx, dist) in enumerate(zip(indices[0], distances[0])):
        raw_text = mapping[idx]
        truncated = raw_text.split("Include colonne")[0].strip()
        print(f"{i+1}. {truncated} → distanza: {dist:.4f}")

    distances, indices = index.search(query_embedding, top_k)
    results = [mapping[i] for i in indices[0] if i in mapping]

    return results
