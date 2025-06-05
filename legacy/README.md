# Legacy Schema Linking Module

This folder contains a previous version of the schema linking component, originally developed to support an NL2SQL pipeline inspired by systems like CHESS and RESDSQL.

It includes modular components for:
- keyword extraction
- retrieval via FAISS
- prompt building
- schema interpretation
- utility functions and configs

## Why is it here?

The current system follows a zero-shot LLM-based approach because the relevant tables were identified only afterward.
- support experiments with hybrid or multi-agent systems
- be reused for fine-tuning or evaluation
- serve as a base for fallback/manual linking

## How to use it

This module is **not active** in the main pipeline. It's stored for future reference and is:
- **excluded from build/deployment**
- **not included in `requirements.txt`**

If you want to use it install dependencies from `requirements-legacy.txt`

---

📁 Status: archived but preserved  
🧠 Maintainer note: don’t delete — this is a good base for schema linking if needed again.
