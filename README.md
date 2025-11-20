# 🧾 OCR Receipt Parser

A robust Python tool for extracting structured data (Merchant, Date, Total Amount, Card Info) from scanned receipts and invoices (PDF/Images). 

Built with **PaddleOCR** for text detection and **Regex** for intelligent parsing.

## 🚀 Features

- **PDF to Image Conversion**: Handles multi-page PDF documents using `PyMuPDF`.
- **Advanced OCR**: Uses `PaddleOCR` with optimized parameters for receipts (angle classification, unclip ratio for faint text).
- **Smart Parsing**:
  - Extracts **Merchant Name**, **Date**, **Time**, and **Total Amount**.
  - Identifies **Card Type** (Visa, Mastercard, etc.) and last 4 digits.
  - Includes fallback logic to detect totals even when the layout is unstructured or OCR is imperfect.
- **Multi-format Support**: Tested on US receipts (e.g., Zion Market) and European receipts.

## 🛠️ Tech Stack

- **Python 3.9+**
- **PaddleOCR** (Deep Learning based OCR)
- **PyMuPDF (fitz)** (PDF processing)
- **Pillow (PIL)** (Image manipulation)
- **NumPy**
- **Regex** (Pattern matching)

## 📂 Project Structure

```bash
.
├── src/
│   ├── preOCR.py           # OCR Engine configuration (PaddleOCR wrapper)
│   ├── receipt_parser.py   # Regex logic and data extraction patterns
│   └── main_ocr.py         # Main script to run the pipeline
├── inputs/                 # Place your PDF receipts here
├── requirements.txt        # Python dependencies
└── README.md
1) Clone the repository
git clone https://github.com/mohammed-adachi/cr-factures-pdf.git
cd cr-factures-pdf
2) Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate 
3) Install dependencies
pip install -r requirements.txt
4)Run the script
python src/main_ocr.py

