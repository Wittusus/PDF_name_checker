import os
from pathlib import Path
import sys
import pdf_name_extractor

PDF_DIR = Path("pdf")


def main():
    if not PDF_DIR.exists() or not PDF_DIR.is_dir():
        print(f"Input directory '{PDF_DIR}' does not exist.")
        sys.exit(1)

    pdf_files = list(PDF_DIR.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in '{PDF_DIR}'.")
        sys.exit(0)

    for pdf_file in pdf_files:
        print(f"\nProcessing: {pdf_file.name}")
        extracted_text = pdf_name_extractor.extract_text_from_pdf(str(pdf_file))
        if not extracted_text:
            print(f"Failed to extract text from {pdf_file.name}")
            continue
        print("Extracted text:")
        print("-" * 40)
        print(extracted_text)
        print("-" * 40)

if __name__ == "__main__":
    main()
