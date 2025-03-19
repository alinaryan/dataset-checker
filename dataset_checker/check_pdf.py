import fitz  # PyMuPDF
import pdfplumber

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
    }

    with fitz.open(file_path) as doc:
        results["page_count"] = len(doc)

        for page_num, page in enumerate(doc, start=1):
            # Check for images
            if page.get_images():
                results["contains_images"].append(page_num)

            # Check for hyperlinks
            links = page.get_links()
            if links:
                results["hyperlinks"].append(page_num)

            # Check for embedded fonts
            fonts = page.get_fonts()
            if fonts:
                results["embedded_fonts"].append(page_num)

    with pdfplumber.open(file_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                # Check for mathematical notation
                if any(char in text for char in ["∑", "∫", "√", "≈", "∞"]):
                    results["mathematical_notation"].append(page_num)

                # Check for tables
                if page.extract_tables():
                    results["tables"].append(page_num)

    return results
