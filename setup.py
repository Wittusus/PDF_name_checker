#!/usr/bin/env python3
"""
Setup script for PDF Name Extractor

This script helps set up the required dependencies for the PDF name extractor.
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Run a command and return success status."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def install_python_packages():
    """Install required Python packages."""
    print("Installing Python packages...")
    command = f"{sys.executable} -m pip install -r requirements.txt"
    return run_command(command, "Installing Python packages")

def check_tesseract():
    """Check if Tesseract OCR is installed."""
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        print("✓ Tesseract OCR is already installed and accessible")
        return True
    except:
        print("✗ Tesseract OCR is not installed or not accessible")
        return False


def check_pymupdf():
    """Check if PyMuPDF is installed."""
    try:
        import fitz
        print("✓ PyMuPDF is already installed and accessible")
        return True
    except ImportError:
        print("✗ PyMuPDF is not installed")
        return False

def install_tesseract_instructions():
    """Provide instructions for installing Tesseract OCR."""
    system = platform.system().lower()
    
    print("\n" + "="*60)
    print("TESSERACT OCR INSTALLATION REQUIRED")
    print("="*60)
    
    if system == "windows":
        print("For Windows:")
        print("1. Download Tesseract installer from:")
        print("   https://github.com/UB-Mannheim/tesseract/wiki")
        print("2. Run the installer and follow the setup wizard")
        print("3. Make sure to add Tesseract to your PATH during installation")
        print("4. Restart your command prompt after installation")
        
    elif system == "darwin":  # macOS
        print("For macOS:")
        print("1. Install Homebrew if you haven't already:")
        print("   /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
        print("2. Install Tesseract:")
        print("   brew install tesseract")
        
    elif system == "linux":
        print("For Linux (Ubuntu/Debian):")
        print("   sudo apt-get update")
        print("   sudo apt-get install tesseract-ocr")
        print("\nFor Linux (CentOS/RHEL/Fedora):")
        print("   sudo yum install tesseract")
        
    print("\nAfter installing Tesseract, run this setup script again.")


def main():
    """Main setup function."""
    print("PDF Name Extractor Setup")
    print("="*30)
    
    # Install Python packages
    if not install_python_packages():
        print("Failed to install Python packages. Please check your pip installation.")
        return False
    
    # Check Tesseract
    tesseract_ok = check_tesseract()
    
    # Check PyMuPDF
    pymupdf_ok = check_pymupdf()
    
    if tesseract_ok and pymupdf_ok:
        print("\n" + "="*60)
        print("SETUP COMPLETE!")
        print("="*60)
        print("All dependencies are installed and ready to use.")
        print("\nYou can now run the PDF name extractor:")
        print("python pdf_name_extractor.py your_file.pdf")
        return True
    
    else:
        print("\n" + "="*60)
        print("ADDITIONAL SETUP REQUIRED")
        print("="*60)
        
        if not tesseract_ok:
            install_tesseract_instructions()
        
        if not pymupdf_ok:
            print("PyMuPDF should have been installed with pip. Try running:")
            print("pip install PyMuPDF")
        
        print("\nAfter installing the missing dependencies, run this setup script again to verify.")
        return False

if __name__ == "__main__":
    main()
