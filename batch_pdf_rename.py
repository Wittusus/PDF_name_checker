import os
import shutil
from pathlib import Path
import sys
import pdf_name_extractor

PDF_DIR = Path("pdf")
RENAMED_DIR = Path("pdf_renamed")


def main():
    # Create output directory if it doesn't exist
    RENAMED_DIR.mkdir(exist_ok=True)

    if not PDF_DIR.exists() or not PDF_DIR.is_dir():
        print(f"Input directory '{PDF_DIR}' does not exist.")
        sys.exit(1)

    pdf_files = list(PDF_DIR.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in '{PDF_DIR}'.")
        sys.exit(0)

    for pdf_file in pdf_files:
        print(f"\nProcessing: {pdf_file.name}")
        # Extract text and find certification name
        extracted_text = pdf_name_extractor.extract_text_from_pdf(str(pdf_file))
        if not extracted_text:
            print(f"Failed to extract text from {pdf_file.name}")
            continue
        cert_name = pdf_name_extractor.find_certification_name(extracted_text)
        if not cert_name:
            print(f"Could not find certification name in {pdf_file.name}")
            continue
        snake_case_name = pdf_name_extractor.to_snake_case(cert_name)
        new_filename = f"{snake_case_name}.pdf"
        dest_path = RENAMED_DIR / new_filename
        # Avoid overwriting
        counter = 1
        while dest_path.exists():
            new_filename = f"{snake_case_name}_{counter}.pdf"
            dest_path = RENAMED_DIR / new_filename
            counter += 1
        shutil.copy2(pdf_file, dest_path)
        print(f"Copied and renamed to: {dest_path}")

if __name__ == "__main__":
    main()
