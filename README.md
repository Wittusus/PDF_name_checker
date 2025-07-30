# PDF Name Extractor

A Python script that extracts text from PDF files (including image-based PDFs) using OCR, finds the line after "This is to certify that", and renames the file using that text in snake_case format.

## Features

- **OCR Support**: Works with image-based PDFs that can't be searched normally
- **Text Extraction**: Finds certification names after "This is to certify that"
- **Smart Renaming**: Converts names to snake_case format for consistent file naming
- **Safe Operation**: Avoids overwriting existing files by adding numbers
- **Preview Mode**: Option to preview extracted text without renaming files

## Requirements

### Python Libraries
- `pytesseract` - Python wrapper for Tesseract OCR
- `Pillow` (PIL) - Image processing library
- `PyMuPDF` - Pure Python PDF processing library

### System Dependencies
- **Tesseract OCR** - For text recognition from images

## Installation

### Quick Setup
1. Run the setup script to install Python dependencies and check system requirements:
   ```bash
   python setup.py
   ```

### Manual Installation

#### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Install Tesseract OCR

**Windows:**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer and add to PATH

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr
```

## Usage

### Command Line

**Basic usage:**
```bash
python pdf_name_extractor.py "path/to/your/certificate.pdf"
```

**Preview mode (extract text without renaming):**
```bash
python pdf_name_extractor.py "path/to/your/certificate.pdf" --preview-only
```

### Windows Batch File
For easier use on Windows, you can use the provided batch file:
```cmd
process_pdf.bat "C:\path\to\your\certificate.pdf"
```

### Examples

**Input PDF contains:**
```
This is to certify that
John Smith
has successfully completed...
```

**Result:** File renamed to `john_smith.pdf`

**Input PDF contains:**
```
This is to certify that Jane Doe, PhD
has achieved...
```

**Result:** File renamed to `jane_doe_phd.pdf`

## How It Works

1. **Text Extraction**: First tries to extract text directly from the PDF
2. **OCR Fallback**: If direct extraction fails, converts PDF pages to images using PyMuPDF
3. **OCR Processing**: Uses Tesseract to extract text from images
4. **Text Search**: Looks for "This is to certify that" (case-insensitive)
5. **Name Extraction**: Extracts the next line containing the name
6. **Snake Case Conversion**: Converts the name to snake_case format
7. **File Renaming**: Safely renames the file, avoiding overwrites

## Troubleshooting

### Common Issues

**"Missing required library" error:**
- Install the required Python packages: `pip install -r requirements.txt`

**"Tesseract not found" error:**
- Install Tesseract OCR and ensure it's in your PATH
- On Windows, make sure the installation directory is added to PATH

**Poor OCR accuracy:**
- Ensure the PDF has good image quality
- Try processing a higher resolution version of the PDF

**"Could not find certification phrase" error:**
- Check if the PDF actually contains "This is to certify that"
- Use `--preview-only` to see what text was extracted
- The phrase might be split across lines or have different formatting

### Testing OCR Setup

To test if OCR is working correctly:
```bash
python pdf_name_extractor.py "1.pdf" --preview-only
```

This will show you exactly what text is being extracted from your PDF.

## File Structure

```
PDF_name_checker/
├── pdf_name_extractor.py  # Main script
├── setup.py              # Setup and dependency checker
├── requirements.txt      # Python dependencies
├── process_pdf.bat       # Windows batch file
├── README.md            # This file
└── 1.pdf               # Your PDF file(s)
```

## License

This project is open source and available under the MIT License.
