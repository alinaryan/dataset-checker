import fitz  # PyMuPDF
import pdfplumber
import re
import json

def count_pages(file_path):
    """Returns the number of pages in the PDF."""
    with fitz.open(file_path) as doc:
        return len(doc)

def has_images(file_path):
    """Checks if the PDF contains images."""
    with fitz.open(file_path) as doc:
        return any(len(page.get_images(full=True)) > 0 for page in doc)

def detect_aspect_ratio_variations(file_path):
    """Checks if the PDF has varying aspect ratios across pages."""
    aspect_ratios = set()
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            aspect_ratios.add(round(page.width / page.height, 2))
    return len(aspect_ratios) > 1

def has_mathematical_notation(file_path):
    """Checks if the PDF contains mathematical notation using common math symbols."""
    math_symbols = r'\d+[xy=]+|∑|∫|π|√|∞'
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text and re.search(math_symbols, text):
                return True
    return False

def detect_embedded_fonts(file_path):
    """Checks if the PDF contains embedded fonts."""
    with fitz.open(file_path) as doc:
        for page in doc:
            for font in page.get_fonts():
                if font[3] == 'embedded':  # Checking if font is embedded
                    return True
    return False

def extract_hyperlinks_and_forms(file_path):
    """Separates hyperlinks and form annotations in the PDF."""
    hyperlinks = False
    forms = False
    with fitz.open(file_path) as doc:
        for page in doc:
            for link in page.links():
                if "uri" in link or "url" in link:
                    hyperlinks = True
                if "annot" in link or "form" in link:
                    forms = True
    return hyperlinks, forms

def detect_tables_and_nested_tables(file_path):
    """Checks if the PDF contains tables and detects nested tables."""
    has_tables = False
    nested_tables = False
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            tables = page.find_tables()
            if tables:
                has_tables = True
                for table in tables:
                    for row in table.rows:
                        for cell in row.cells:
                            if isinstance(cell, pdfplumber.table.Table):  # Nested table check
                                nested_tables = True
    return has_tables, nested_tables

def detect_multi_column_format(file_path):
    """Heuristically detects multi-column layout based on text alignment."""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            words = page.extract_words()
            column_positions = {word["x0"] for word in words}
            if len(column_positions) > 2:
                return True
    return False

def detect_nested_columns(file_path):
    """Checks for nested columns by grouping text blocks by x-coordinates."""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text_blocks = page.extract_text_lines()
            column_clusters = {}
            for block in text_blocks:
                x_pos = round(block["x0"], -1)
                column_clusters.setdefault(x_pos, []).append(block)
            if len(column_clusters) > 2:
                return True
    return False

def generate_summary(results):
    """Generates a structured summary with better clarity and PDF association."""
    for file, data in results.items():
        total_pages = data["page_count"]
        print("\n📂 PDF Report: " + file)
        print("=" * 50)
        print(f"📄 Total Pages: {total_pages}\n")

        # 🚨 Critical Issues (Must Avoid)
        critical_issues = []
        if data.get("contains_images"):
            critical_issues.append(f"❌ Contains Images (Pages: {format_pages(data['contains_images'], total_pages)})")
        if data.get("scanned_pdf"):
            critical_issues.append("❌ Scanned PDFs / OCR Detected: Yes")

        if critical_issues:
            print("🚨 Critical Issues (Must Avoid):")
            for issue in critical_issues:
                print(f"   {issue}")
            print("")  # Space after critical issues

        # ⚠️ Content Prone to Conversion Errors
        error_prone_issues = []
        error_checks = [
            ("multi_column_format", "🔸 Multi-Column Format"),
            ("embedded_fonts", "🔸 Embedded Fonts"),
            ("charts", "🔸 Charts / Tables"),
            ("nested_tables", "🔸 Nested Tables"),
            ("hyperlinks", "🔸 Hyperlinks"),
            ("mathematical_notation", "🔸 Mathematical Notation"),
        ]

        for key, label in error_checks:
            if data.get(key):
                error_prone_issues.append(f"{label} (Pages: {format_pages(data[key], total_pages)})")

        if error_prone_issues:
            print("⚠️ Content Prone to Conversion Errors:")
            for issue in error_prone_issues:
                print(f"   {issue}")

        print("=" * 50 + "\n")  # Clear separator for each PDF


def format_pages(pages, total_pages):
    """Formats page numbers for output."""
    if isinstance(pages, list) and set(pages) == set(range(1, total_pages + 1)):
        return "All pages"
    elif isinstance(pages, list):
        return ", ".join(map(str, pages))
    return "N/A"

def save_results(results, output_file):
    """Saves results to a JSON file with 'All pages' formatting applied."""
    formatted_results = {}

    for file, data in results.items():
        total_pages = data["page_count"]
        formatted_results[file] = {
            issue: ("All pages" if isinstance(pages, list) and set(pages) == set(range(1, total_pages + 1)) else pages)
            for issue, pages in data.items() if issue != "page_count"
        }
        formatted_results[file]["page_count"] = total_pages  # Keep total pages as an integer

    with open(output_file, "w") as f:
        json.dump(formatted_results, f, indent=4)
    
    print(f"📁 Results saved to {output_file}")
