# 🛠 Preflight PDF Checker

## 📌 Overview
The **Preflight PDF Checker** is a tool designed to evaluate PDFs before converting them using **Docling** or other open-source file converters. It helps identify **critical issues** that should be avoided and **problematic content** that might lead to conversion errors.

This tool scans PDFs for:
- **🚨 Critical Issues (Must Avoid)**
  - Images (including scanned PDFs)
  - Text within images
  - OCR-based PDFs
- **⚠️ Content Prone to Conversion Errors**
  - Multi-column layouts
  - Embedded fonts
  - Charts and tables
  - Hyperlinks and interactive content
  - Mathematical notation

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

📂 **PDF Report:** `/home/user/documents/sample.pdf`  
📄 **Total Pages:** 48  

🚨 Critical Issues (Must Avoid)
- ❌ **Contains Images** (Pages: All pages)  

⚠️ Content Prone to Conversion Errors
- 🔸 **Embedded Fonts** (Pages: All pages)  
- 🔸 **Multi-Column Format** (Pages: 3, 5-7)  
- 🔸 **Charts / Tables** (Pages: 8, 12-14)  
- 🔸 **Hyperlinks** (Pages: 2, 10, 20)  
- 🔸 **Mathematical Notation** (Pages: 15, 21-22)  


## 📁 JSON Output (preflight_results.json)
```
{
    "/home/user/documents/sample.pdf": {
        "page_count": 48,
        "contains_images": "All pages",
        "multi_column_format": [3, 5, 6, 7],
        "embedded_fonts": "All pages",
        "charts": [8, 12, 13, 14],
        "hyperlinks": [2, 10, 20],
        "mathematical_notation": [15, 21, 22]
    }
}
```

## 🤝 Acknowledgments
Built by Alina with ❤️ for better PDF conversion workflows!


