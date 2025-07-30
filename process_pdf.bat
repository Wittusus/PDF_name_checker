@echo off
REM PDF Name Extractor - Windows Batch Script
REM Usage: process_pdf.bat "path\to\your\file.pdf"

if "%~1"=="" (
    echo Usage: %0 "path\to\pdf\file.pdf"
    echo Example: %0 "C:\Documents\certificate.pdf"
    pause
    exit /b 1
)

if not exist "%~1" (
    echo Error: File "%~1" does not exist
    pause
    exit /b 1
)

echo Processing PDF: %~1
python pdf_name_extractor.py "%~1"

echo.
echo Press any key to continue...
pause >nul
