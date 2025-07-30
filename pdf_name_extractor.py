#!/usr/bin/env python3
"""
PDF Name Extractor

This script extracts text from PDF files (including image-based PDFs) using OCR,
finds the line after "This is to certify that", and renames the file using that
text in snake_case format.

Requirements:
- pytesseract
- Pillow (PIL)
- pdf2image
- poppler-utils (for pdf2image)

Usage:
    python pdf_name_extractor.py <pdf_file_path>
"""

import os
import sys
import re
import io
from pathlib import Path
import argparse

try:
    import pytesseract
    from PIL import Image
    import fitz  # PyMuPDF
    
    # Try to load local Tesseract configuration if it exists
    try:
        import tesseract_config
        print("Loaded local Tesseract configuration")
    except ImportError:
        pass  # No local config file, that's fine
        
except ImportError as e:
    print(f"Missing required library: {e}")
    print("Please install required libraries:")
    print("pip install pytesseract Pillow PyMuPDF")
    sys.exit(1)


def to_snake_case(text):
    """Convert text to snake_case format."""
    # Remove special characters and replace with spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    # Strip and convert to lowercase
    text = text.strip().lower()
    # Replace spaces with underscores
    text = text.replace(' ', '_')
    # Remove multiple underscores
    text = re.sub(r'_+', '_', text)
    # Remove leading/trailing underscores
    text = text.strip('_')
    return text


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using PyMuPDF and OCR as fallback."""
    try:
        # First, try to extract text directly from PDF
        print(f"Opening PDF: {pdf_path}")
        doc = fitz.open(pdf_path)
        extracted_text = ""
        
        # Try direct text extraction first
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            page_text = page.get_text()
            if page_text.strip():
                extracted_text += page_text + "\n"
        
        # If we got meaningful text, return it
        if extracted_text.strip() and len(extracted_text.strip()) > 50:
            print(f"Successfully extracted text directly from PDF ({len(extracted_text)} characters)")
            doc.close()
            return extracted_text
        
        # If direct text extraction failed or gave minimal text, use OCR
        print("Direct text extraction failed or gave minimal results. Using OCR...")
        extracted_text = ""
        
        for page_num in range(len(doc)):
            print(f"Processing page {page_num + 1}/{len(doc)} with OCR")
            page = doc.load_page(page_num)
            
            # Convert page to image
            mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better OCR accuracy
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            
            # Convert to PIL Image
            image = Image.open(io.BytesIO(img_data))
            
            # Use pytesseract to extract text from image
            page_text = pytesseract.image_to_string(image)
            extracted_text += page_text + "\n"
        
        doc.close()
        return extracted_text
    
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None


def find_certification_name(text):
    """Find the line after 'This is to certify that' in the text."""
    if not text:
        return None
    
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        # Look for the certification phrase (case insensitive)
        if re.search(r'this\s+is\s+to\s+certify\s+that', line, re.IGNORECASE):
            print(f"Found certification phrase in line: '{line.strip()}'")
            
            # Check if the name is on the same line after the phrase
            match = re.search(r'this\s+is\s+to\s+certify\s+that\s+(.+)', line, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                if name:
                    print(f"Found name on same line: '{name}'")
                    return name
            
            # If not on the same line, check the next line
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line:
                    print(f"Found name on next line: '{next_line}'")
                    return next_line
            
            # If next line is empty, check the line after that
            if i + 2 < len(lines):
                next_next_line = lines[i + 2].strip()
                if next_next_line:
                    print(f"Found name on line after next: '{next_next_line}'")
                    return next_next_line
    
    print("Could not find certification phrase or name")
    return None


def rename_pdf_file(pdf_path, new_name):
    """Rename the PDF file with the new name."""
    try:
        pdf_path = Path(pdf_path)
        directory = pdf_path.parent
        
        # Create new filename with snake_case name
        snake_case_name = to_snake_case(new_name)
        new_filename = f"{snake_case_name}.pdf"
        new_path = directory / new_filename
        
        # Avoid overwriting existing files
        counter = 1
        while new_path.exists():
            new_filename = f"{snake_case_name}_{counter}.pdf"
            new_path = directory / new_filename
            counter += 1
        
        # Rename the file
        pdf_path.rename(new_path)
        print(f"Successfully renamed '{pdf_path.name}' to '{new_filename}'")
        return str(new_path)
    
    except Exception as e:
        print(f"Error renaming file: {e}")
        return None


def process_pdf(pdf_path):
    """Main function to process a PDF file."""
    if not os.path.exists(pdf_path):
        print(f"Error: File '{pdf_path}' does not exist")
        return False
    
    if not pdf_path.lower().endswith('.pdf'):
        print(f"Error: '{pdf_path}' is not a PDF file")
        return False
    
    print(f"Processing PDF: {pdf_path}")
    
    # Extract text from PDF using OCR
    extracted_text = extract_text_from_pdf(pdf_path)
    if not extracted_text:
        print("Failed to extract text from PDF")
        return False
    
    print("Extracted text preview:")
    print("-" * 50)
    print(extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text)
    print("-" * 50)
    
    # Find the certification name
    certification_name = find_certification_name(extracted_text)
    if not certification_name:
        print("Could not find certification name in the PDF")
        return False
    
    print(f"Extracted certification name: '{certification_name}'")
    
    # Rename the file
    new_path = rename_pdf_file(pdf_path, certification_name)
    if new_path:
        print(f"File processing completed successfully!")
        return True
    else:
        print("Failed to rename the file")
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Extract certification name from PDF and rename file')
    parser.add_argument('pdf_file', help='Path to the PDF file to process')
    parser.add_argument('--preview-only', action='store_true', 
                       help='Only extract and preview text without renaming file')
    
    args = parser.parse_args()
    
    if args.preview_only:
        # Just extract and show text
        extracted_text = extract_text_from_pdf(args.pdf_file)
        if extracted_text:
            print("Extracted text:")
            print("=" * 60)
            print(extracted_text)
            print("=" * 60)
            
            certification_name = find_certification_name(extracted_text)
            if certification_name:
                snake_case_name = to_snake_case(certification_name)
                print(f"Found certification name: '{certification_name}'")
                print(f"Snake case version: '{snake_case_name}'")
        return
    
    # Process the PDF file
    success = process_pdf(args.pdf_file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
