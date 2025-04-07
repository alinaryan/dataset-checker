# utils.py
import json
import os

def get_pdf_files(file_path=None, dir_path=None):
    if file_path:
        return [file_path] if file_path.endswith(".pdf") else []
    elif dir_path:
        return [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith(".pdf")]
    return []

def save_results(results, output_file):
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)
    print(f"\n📁 Results saved to {output_file}")

def generate_summary(results):
    print("📊 Summary Report")
    print("=" * 50)
    for file, data in results.items():
        if data.get("merged_cell_pages"):
            print(f"\n📂 File: {file}")
            pages = format_pages(data["merged_cell_pages"])
            print(f"⚠️ Merged Table Cells Detected on Pages: {pages}")
            for cell in data.get("merged_table_cells", []):
                page = cell.get("page")
                text = cell.get("text", "").strip()
                if len(text) > 30:
                    text = text[:30] + "..."
                print(f"   - Page {page}: \"{text}\" (colspan={cell['colspan']}, rowspan={cell['rowspan']})")

def format_pages(pages):
    """Format page numbers into compressed ranges."""
    if not pages:
        return ""
    pages = sorted(set(pages))
    ranges = []
    start = pages[0]
    for i in range(1, len(pages)):
        if pages[i] != pages[i - 1] + 1:
            if start == pages[i - 1]:
                ranges.append(f"{start}")
            else:
                ranges.append(f"{start}-{pages[i - 1]}")
            start = pages[i]
    if start == pages[-1]:
        ranges.append(f"{start}")
    else:
        ranges.append(f"{start}-{pages[-1]}")
    return ", ".join(ranges)
