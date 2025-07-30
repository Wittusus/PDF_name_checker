"""
Tesseract Installation Helper for Windows

This script helps you install Tesseract OCR on Windows.
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def check_tesseract_installed():
    """Check if Tesseract is already installed."""
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        print("✓ Tesseract is already installed and working!")
        return True
    except Exception as e:
        print(f"✗ Tesseract not found: {e}")
        return False

def find_tesseract_executable():
    """Try to find Tesseract executable in common locations."""
    common_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        r"C:\Users\{}\AppData\Local\Tesseract-OCR\tesseract.exe".format(os.getenv('USERNAME')),
        r"C:\tesseract\tesseract.exe",
    ]
    
    print("\nSearching for Tesseract executable...")
    for path in common_paths:
        if os.path.exists(path):
            print(f"✓ Found Tesseract at: {path}")
            return path
    
    print("✗ Tesseract executable not found in common locations")
    return None

def configure_tesseract_path(tesseract_path):
    """Configure pytesseract to use the found executable."""
    try:
        import pytesseract
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        # Test if it works
        pytesseract.get_tesseract_version()
        print(f"✓ Successfully configured Tesseract path: {tesseract_path}")
        
        # Create a config file for the PDF extractor
        config_content = f'''# Tesseract configuration for PDF Name Extractor
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"{tesseract_path}"
'''
        
        with open("tesseract_config.py", "w") as f:
            f.write(config_content)
        
        print("✓ Created tesseract_config.py file")
        print("\u2713 Loaded local Tesseract configuration")
        return True
        
    except Exception as e:
        print(f"✗ Failed to configure Tesseract: {e}")
        return False

def download_tesseract():
    """Open the Tesseract download page."""
    print("\n" + "="*60)
    print("TESSERACT DOWNLOAD INSTRUCTIONS")
    print("="*60)
    print("1. I'll open the Tesseract download page in your browser")
    print("2. Download the Windows installer (usually named like 'tesseract-ocr-w64-setup-5.x.x.exe')")
    print("3. Run the installer with default settings")
    print("4. Make sure to check 'Add to PATH' during installation")
    print("5. After installation, run this script again")
    print("\nPress Enter to open the download page...")
    
    input()
    
    try:
        webbrowser.open("https://github.com/UB-Mannheim/tesseract/wiki")
        print("✓ Opened download page in browser")
    except:
        print("✗ Could not open browser. Please manually visit:")
        print("https://github.com/UB-Mannheim/tesseract/wiki")

def test_pdf_processing():
    """Test if PDF processing works with the current setup."""
    try:
        print("\nTesting PDF processing...")
        result = subprocess.run([
            sys.executable, "pdf_name_extractor.py", "1.pdf", "--preview-only"
        ], capture_output=True, text=True, cwd=".")
        
        if result.returncode == 0:
            print("✓ PDF processing test successful!")
            print("Preview of extracted text:")
            print("-" * 40)
            print(result.stdout)
            print("-" * 40)
            return True
        else:
            print("✗ PDF processing test failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ Error testing PDF processing: {e}")
        return False

def main():
    """Main function."""
    print("Tesseract Installation Helper")
    print("=" * 30)
    
    # Check if already installed
    if check_tesseract_installed():
        print("\nTesting PDF processing with current setup...")
        if test_pdf_processing():
            print("\n🎉 Everything is working! You can now process PDFs.")
            return
        else:
            print("\n⚠️ Tesseract is installed but PDF processing failed.")
    
    # Try to find existing installation
    tesseract_path = find_tesseract_executable()
    if tesseract_path:
        print(f"\nFound Tesseract but it's not configured properly.")
        if configure_tesseract_path(tesseract_path):
            print("\nTesting PDF processing...")
            if test_pdf_processing():
                print("\n🎉 Successfully configured! You can now process PDFs.")
                return
    
    # Need to download and install
    print("\nTesseract needs to be installed.")
    choice = input("Do you want to download Tesseract now? (y/n): ").lower().strip()
    
    if choice in ['y', 'yes']:
        download_tesseract()
        print("\nAfter installing Tesseract, run this script again to test the setup.")
    else:
        print("\nTo install Tesseract manually:")
        print("1. Visit: https://github.com/UB-Mannheim/tesseract/wiki")
        print("2. Download the Windows installer")
        print("3. Run the installer and add to PATH")
        print("4. Run this script again")

if __name__ == "__main__":
    main()
