import fitz  # PyMuPDF
import pdfplumber
import re

def check_pdf(file_path):
    results = {
        "page_count": 0,
        "contains_images": [],
        "multi_column_format": [],
        "aspect_ratio_variations": [],
        "mathematical_notation": [],
        "embedded_fonts": [],
        "hyperlinks": [],
        "forms": [],
        "charts": [],
        "tables": [],
        "multi_page_tables": [],
        "nested_tables": [],
        "nested_columns": [],
        "scanned_pdf": False,
    }

    aspect_ratios = {}
    table_found = False
    multi_page_tables = False

    # Check using PyMuPDF (fitz)
    with fitz.open(file_path) as doc:
        results["page_count"] = len(doc)

        for page_num, page in enumerate(doc, start=1):
            # Check for images
            if page.get_images(full=True):
                results["contains_images"].append(page_num)
            
            # Check for hyperlinks and forms
            links = page.get_links()
            if links:
                for link in links:
                    if link.get("uri") or link.get("url"):
                        results["hyperlinks"].append(page_num)
                    if link.get("type") == 2:  # Type 2 is for form annotations
                        results["forms"].append(page_num)
            
            # Check for embedded fonts
            if page.get_text("dict").get("blocks"):
                results["embedded_fonts"].append(page_num)
            else:
                results["scanned_pdf"] = True  # If text extraction fails, it's likely scanned

    # Check using pdfplumber
    with pdfplumber.open(file_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            aspect_ratio = round(page.width / page.height, 2)
            if aspect_ratio not in aspect_ratios:
                aspect_ratios[aspect_ratio] = []
            aspect_ratios[aspect_ratio].append(page_num)

            text = page.extract_text()
            text
            if text:
                # Check for mathematical notation
                if re.search(r'[0-9]+[xy=]+|∑|∫|π|√|∞', text):
                    results["mathematical_notation"].append(page_num)
                
                # Check for multi-column format
                words = page.extract_words()
                column_positions = {word["x0"] for word in words}
                if len(column_positions) > 2:  # More than 2 vertical positions suggests multi-columns
                    results["multi_column_format"].append(page_num)
            
            # Check for tables
            tables = page.extract_tables()
            if tables:
                results["tables"].append(page_num)
                
                if table_found:
                    multi_page_tables = True
                table_found = True

                # Check for nested tables
                for table in tables:
                    for row in table:
                        for cell in row:
                            if isinstance(cell, list):
                                results["nested_tables"].append(page_num)
            
            # Check for charts (If there are images but not marked as 'contains_images')
            if len(page.images) > 0 and page_num not in results["contains_images"]:
                results["charts"].append(page_num)

            # Check for nested columns
            text_blocks = page.extract_text_lines()
            if text_blocks:
                column_clusters = {}
                for block in text_blocks:
                    x_pos = round(block["x0"], -1)
                    column_clusters.setdefault(x_pos, []).append(block)
                if len(column_clusters) > 2:
                    results["nested_columns"].append(page_num)

    # Store aspect ratio variations if there are multiple distinct ratios
    results["aspect_ratio_variations"] = {ratio: pages for ratio, pages in aspect_ratios.items() if len(pages) > 1}
    results["multi_page_tables"] = multi_page_tables

    return results
