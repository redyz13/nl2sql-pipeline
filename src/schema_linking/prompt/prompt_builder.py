def build_table_prompt(question: str, table_texts: list[str]) -> str:
    schema = "\n".join(f"- {tbl}" for tbl in table_texts)
    return (
        f"Hai una domanda e una lista di tabelle dello schema del database.\n"
        f"Domanda: {question}\n\n"
        f"Tabelle disponibili:\n{schema}\n\n"
        f"Seleziona SOLO le tabelle rilevanti. Rispondi con una lista nel formato:\n"
        f"nome_tabella\n\n"
        f"Non aggiungere spiegazioni, commenti o altro testo. Solo la lista."
    )

def build_column_prompt(question: str, column_texts: list[str]) -> str:
    schema = "\n".join(f"- {col}" for col in column_texts)
    return (
        f"Hai una domanda e una lista di colonne dello schema del database.\n"
        f"Domanda: {question}\n\n"
        f"Colonne disponibili:\n{schema}\n\n"
        f"Seleziona SOLO le colonne rilevanti. Rispondi con una lista nel formato:\n"
        f"tabella.colonna\n\n"
        f"Non fornire spiegazioni, non generare codice, non scrivere altro. Solo la lista."
    )

def build_keyword_prompt(question: str) -> str:
    return (
        f"Hai una domanda in linguaggio naturale.\n"
        f"Domanda: \"{question}\"\n\n"
        f"Il tuo compito è estrarre esclusivamente le keyword rilevanti per una traduzione da linguaggio naturale a query SQL\n"
        f"Le keyword sono parole o brevi frasi che rappresentano concetti come:\n"
        f"- entità\n"
        f"- condizioni o vincoli\n"
        f"- funzioni di aggregazione\n"
        f"- concetti chiave necessari per la traduzione della domanda in una query SQL.\n"
        f"Rispondi SOLO con una lista di keyword, una per riga, senza spiegazioni, commenti o punteggiatura aggiuntiva. Usa il seguente formato:\n"
        f"keyword"
    )

def build_column_filtering_prompt(question: str, column_texts: list[str], keywords: list[str]) -> str:
    schema = "\n".join(f"- {col}" for col in column_texts)
    keyword_text = "\n".join(f"- {kw}" for kw in keywords)

    return (
        f"Hai una domanda, una lista di parole chiave e una lista di colonne candidate dello schema del database.\n"
        f"Domanda: {question}\n"
        f"Parole chiave estratte:\n{keyword_text}\n\n"
        f"Colonne candidate:\n{schema}\n\n"
        f"Seleziona SOLO le colonne potenzialmente rilevanti per rispondere alla domanda.\n"
        f"Rispondi con una lista nel formato:\n"
        f"tabella.colonna\n\n"
        f"Non aggiungere spiegazioni, non scrivere commenti, non generare codice. Solo la lista."
    )
