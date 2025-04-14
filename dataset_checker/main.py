# main.py
import argparse
from dataset_checker.utils import get_pdf_files, save_results, generate_summary
from dataset_checker.analysis import analyze_pdf_with_docling

def parse_args():
    parser = argparse.ArgumentParser(description="Docling PDF Checker")
    parser.add_argument("-f", "--file", help="Path to a PDF file")
    parser.add_argument("-d", "--dir", help="Path to a directory of PDFs")
    parser.add_argument("-o", "--output", help="Optional path to save JSON results", default="results.json")
    return parser.parse_args()

def main():
    args = parse_args()
    pdfs = get_pdf_files(args.file, args.dir)
    if not pdfs:
        print("❌ No PDFs found to process.")
        return

    all_results = {}
    for path in pdfs:
        print(f"\n🔍 Converting and analyzing: {path}\n")
        try:
            result = analyze_pdf_with_docling(path)
            all_results[path] = result
        except Exception as e:
            print(f"❌ Failed to process {path}: {e}")

    generate_summary(all_results)
    save_results(all_results, args.output)

if __name__ == "__main__":
    main()
