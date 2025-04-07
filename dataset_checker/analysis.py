# analysis.py
from docling.document_converter import DocumentConverter
from docling_core.types.doc.document import TableData
import pdfplumber

def extract_page_info_with_pdfplumber(pdf_path):
    table_pages = {}
    print(f"[DEBUG] Table pages: {table_pages}")
    table_index = 0
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()
            if tables:
                for _ in tables:
                    table_pages[table_index] = page_num
                    table_index += 1
                    print(f"[DEBUG] Table pages: {table_pages}")
    return len(pdf.pages), table_pages

def cell_is_merged(cell):
    return (
        cell.end_col_offset_idx - cell.start_col_offset_idx > 1 or
        cell.end_row_offset_idx - cell.start_row_offset_idx > 1
    )

def analyze_pdf_with_docling(file_path):
    total_pages, table_pages = extract_page_info_with_pdfplumber(file_path)

    converter = DocumentConverter()
    result = converter.convert(file_path)
    doc = result.document

    issues = {
        "merged_table_cells": [],
        "table_count": 0,
        "merged_cell_pages": set(),
        "page_count": total_pages
    }

    for i, table_item in enumerate(doc.tables):
        page_number = table_pages.get(i, "Unknown page")
        table_data = table_item.data
        issues["table_count"] += 1

        print(f"[DEBUG] Inspecting table {i} on page {page_number}")
        print(f"[DEBUG] Table data: {type(table_data)}")
        print(f"[DEBUG] Number of rows: {table_data.num_rows}, Number of cols: {table_data.num_cols}")
        print(f"[DEBUG] Grid type: {type(table_data.grid)}")
        print(f"[DEBUG] Grid content preview: {table_data.grid[:1]}")

        for row_idx, row in enumerate(table_data.grid):
            for col_idx, cell in enumerate(row):
                if cell_is_merged(cell):
                    print(f"[DEBUG] Found merged cell on page {page_number}, table {i}, row {row_idx}, col {col_idx}, text: {cell.text}")

                    issues["merged_table_cells"].append({
                        "page": page_number,
                        "row": row_idx,
                        "column": col_idx,
                        "colspan": cell.end_col_offset_idx - cell.start_col_offset_idx,
                        "rowspan": cell.end_row_offset_idx - cell.start_row_offset_idx,
                        "text": cell.text or "[empty]"
                    })

                    if isinstance(page_number, int):
                        issues["merged_cell_pages"].add(page_number)

    issues["merged_cell_pages"] = sorted(issues["merged_cell_pages"])
    print(f"[DEBUG] Docling table count: {len(doc.tables)}")
    print(f"[DEBUG] Pdfplumber table count: {len(table_pages)}")
    return issues
