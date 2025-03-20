import json

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
            formatted_pages = format_pages(data['contains_images'], total_pages)
            if formatted_pages:
                critical_issues.append(f"❌ Contains Images (Pages: {formatted_pages})")
                
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
            ("tables", "🔸 Tables"),
            ("multi_page_tables", "🔸 Multi-Page Tables"),
            ("nested_tables", "🔸 Nested Tables"),
            ("nested_columns", "🔸 Nested Columns"),
            ("hyperlinks", "🔸 Hyperlinks"),
            ("forms", "🔸 Forms"),
            ("mathematical_notation", "🔸 Mathematical Notation")
        ]

        for key, label in error_checks:
            if data.get(key):
                formatted_pages = format_pages(data[key], total_pages)
                if formatted_pages:  # Only add the issue if it's not None
                    error_prone_issues.append(f"{label} (Pages: {formatted_pages})")

        # Handle aspect ratio variations separately
        if data.get("aspect_ratio_variations"):
            for ratio, pages in data["aspect_ratio_variations"].items():
                formatted_pages = format_pages(pages, total_pages)
                if formatted_pages:
                    error_prone_issues.append(f"🔸 Aspect Ratio Variations (Aspect Ratio: {ratio}, Pages: {formatted_pages})")

        if error_prone_issues:
            print("⚠️ Content Prone to Conversion Errors:")
            for issue in error_prone_issues:
                print(f"   {issue}")

        print("=" * 50 + "\n")  # Clear separator for each PDF


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

def format_pages(pages, total_pages):
    """Formats page numbers for output, grouping consecutive pages into ranges."""
    if isinstance(pages, list) and set(pages) == set(range(1, total_pages + 1)):
        return "All pages"
    elif isinstance(pages, list) and len(pages) > 0:
        pages = sorted(pages)
        ranges = []
        start = pages[0]

        for i in range(1, len(pages)):
            if pages[i] != pages[i - 1] + 1:
                # End of a range
                if start == pages[i - 1]:
                    ranges.append(f"{start}")
                else:
                    ranges.append(f"{start}-{pages[i - 1]}")
                start = pages[i]
        
        # Add the last range or page
        if start == pages[-1]:
            ranges.append(f"{start}")
        else:
            ranges.append(f"{start}-{pages[-1]}")
        
        return ", ".join(ranges)
    return None  # Return None if no pages are detected
