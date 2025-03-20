import argparse
import os
from dataset_checker.check_pdf import check_pdf
from dataset_checker.utils import generate_summary, save_results


def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Preflight PDF Checker for Open Source File Converters")
    parser.add_argument("-f", "--file", help="Path to a single PDF file")
    parser.add_argument("-d", "--dir", help="Path to a directory containing PDFs")
    parser.add_argument("-o", "--output", help="Save results to a JSON file", default="preflight_results.json")
    return parser.parse_args()

def get_pdf_files(input_path):
    """Returns a list of PDF files based on input type (file or directory)."""
    if os.path.isfile(input_path) and input_path.endswith(".pdf"):
        return [input_path]
    elif os.path.isdir(input_path):
        return [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith(".pdf")]
    else:
        print("❌ Invalid path! Please provide a valid PDF file or directory.")
        return []

def main():
    args = parse_arguments()  # ✅ This is now defined!
    all_results = {}

    pdf_files = get_pdf_files(args.file or args.dir)
    if not pdf_files:
        return  # Exit if no valid PDFs

    for file_path in pdf_files:
        print(f"\n🔍 Checking: {file_path}\n")
        results = check_pdf(file_path)
        all_results[file_path] = results

    generate_summary(all_results)

    if all_results:
        save_results(all_results, args.output)

if __name__ == "__main__":
    main()
