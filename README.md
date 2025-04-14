# 🛠 Preflight PDF Checker

## 📌 Overview
Illuminator is your post-conversion PDF sanity checker. After converting documents with Docling, Illuminator scans the result and flags merged table cells that could cause layout issues or require manual cleanup.

It's a lightweight tool designed for teams working with structured data, helping you catch subtle formatting problems before they snowball.

Illuminator checks for:
- **⚠️ Merged Table Cells**
  - Colspan > 1
  - Rowspan > 1
  - Empty merged cells
- **📄 Accurate Page Mapping**
  - Uses Docling’s provenance metadata (not guesswork!)
  - Associates each merged cell with its correct page number

---

## 🔧 Installation

### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/alinaryan/dataset-checker.git
cd dataset-checker
```

### 2️⃣ Create a Virtual Environment (Optional, Recommended)
```python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### 3️⃣ Install Dependencies
```
pip install -r requirements.txt
```

## 🚀 Usage
### Check a Single PDF
```
python -m dataset_checker.main -f /path/to/pdf/document.pdf
```

### Check an Entire Folder of PDFs
```
python -m dataset_checker.main -d /path/to/pdf/folder/
```

### Save Results to a JSON File
By default, results are saved to preflight_results.json. To specify a different output file:
```
python -m dataset_checker.main -d /path/to/pdf/folder/ -o results.json
```

## 📝 Output Format
### 📄 Terminal Output (Example)

📂 File: /home/user/documents/report.pdf

⚠️ Merged Table Cells Detected on Pages: 2, 4
   - Page 2: "Total Revenue" (colspan=2, rowspan=1)
   - Page 4: "[empty]" (colspan=3, rowspan=1)

📁 Results saved to results.json 


## 📁 JSON Output (preflight_results.json)
```
{
    "/home/user/documents/report.pdf": {
        "page_count": 10,
        "table_count": 3,
        "merged_cell_pages": [2, 4],
        "merged_table_cells": [
            {
                "page": 2,
                "row": 0,
                "column": 1,
                "colspan": 2,
                "rowspan": 1,
                "text": "Total Revenue"
            },
            {
                "page": 4,
                "row": 2,
                "column": 0,
                "colspan": 3,
                "rowspan": 1,
                "text": "[empty]"
            }
        ]
    }
}
```

## 🤝 Acknowledgments
Built by Alina with ❤️ for better PDF conversion workflows!


