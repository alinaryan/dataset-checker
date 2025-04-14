from docling.document_converter import DocumentConverter

def cell_is_merged(cell):
    return (
        cell.col_span > 1 or
        cell.row_span > 1
    )

def summarize_tables(doc):
    tables = doc.tables
    num_tables = len(tables)
    pages = []

    for table in tables:
        for prov in table.prov:
            pages.append(prov.page_no)

    return num_tables, pages


def analyze_pdf_with_docling(file_path):
    converter = DocumentConverter()
    result = converter.convert(file_path)
    doc = result.document

    table_count, table_pages_list = summarize_tables(doc)
    total_pages = len(set(table_pages_list)) or "Unknown"

    table_pages = {i: page for i, page in enumerate(table_pages_list)}  # optional anping

    issues = {
        "merged_table_cells": [],
        "table_count": table_count,
        "merged_cell_pages": set(),
        "page_count": total_pages
    }

    for i, table_item in enumerate(doc.tables):
        page_number = table_pages.get(i, "Unknown page")
        table_data = table_item.data

        for row_idx, row in enumerate(table_data.grid):
            for col_idx, cell in enumerate(row):
                if cell_is_merged(cell):
                    issues["merged_table_cells"].append({
                        "page": page_number,
                        "row": row_idx,
                        "column": col_idx,
                        "colspan": cell.col_span,
                        "rowspan": cell.row_span,
                        "text": cell.text or "[empty]"
                    })

                    if isinstance(page_number, int):
                        issues["merged_cell_pages"].add(page_number)

    issues["merged_cell_pages"] = sorted(issues["merged_cell_pages"])
    return issues

