import textwrap
from tabulate import tabulate

def print_header(title):
    # Prints a formatted header with the title
    line = "=" * 60
    print(f"\n{line}\n{title}\n{line}")

def pretty_print_list(title, items):
    # Prints a list with items
    print(f"\n{title}:")
    if not items:
        print("- (empty)")
        return
    for i, item in enumerate(items, 1):
        print(f"{i}. {item}")

def pretty_print_table(title, items, max_width=80):
    print(f"\n{title}:")
    if not items:
        print("- (empty)")
        return

    table_data = []
    for item in items:
        # Split the text into table description and columns
        parts = item.split(" - contiene colonne:")
        
        if len(parts) > 1:
            table_description = parts[0].strip()
            columns_part = parts[1].strip()

            # Split columns by commas, clean extra spaces
            columns = [col.strip() for col in columns_part.split(",")]

            # Wrapping the columns to ensure proper visibility
            wrapped_columns = "\n".join(textwrap.fill(col, width=max_width) for col in columns)

        else:
            table_description = parts[0].strip()
            wrapped_columns = "(no columns found)"  # A default value if no columns exist
        
        # Wrapping the table description
        wrapped_table_description = textwrap.fill(table_description, width=max_width)

        # Append the table and its columns to the table_data
        table_data.append([wrapped_table_description, wrapped_columns])

    # Using tabulate to display the data in a well-structured table format
    print(tabulate(table_data, headers=["Table", "Columns"], tablefmt="fancy_grid", numalign="left"))

def print_keywords(keywords):
    # Prints the list of keywords
    pretty_print_list("Keywords", keywords)

def print_summary(question, keywords, linked_tables, linked_columns):
    # Prints the final summary with all results
    print_header("Final Result")
    print("Question:", question)
    print_keywords(keywords)
    pretty_print_list("Linked Tables (LLM)", linked_tables)
    pretty_print_list("Linked Columns (LLM)", linked_columns)
