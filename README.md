# PDF OCR GUI

A standalone Python application for converting PDFs into **searchable PDFs** using **OCR**. The application bundles **Tesseract** and **Poppler**, so no external installation is required.  

---

## Features

- Converts PDFs into **searchable PDFs** with OCR text.
- Maintains **page order** (front-to-back).
- Multi-language OCR support (`eng`, `deu`, etc.).
- Output PDF is saved in the same folder as the input, with `_OCR` appended to the filename.
- Bundled Tesseract and Poppler — no additional setup required.
- Simple GUI with input PDF selection, language selection, log window, and start button.



---

## Dependencies

- Python 3.8+ (tested with Python 3.13)
- Python packages:
  - `pytesseract`
  - `pdf2image`
- Optional: `PyInstaller` for building executable

Install Python packages:

```bash
pip install pytesseract pdf2image
```

## Building the Executable

You can bundle your app as a standalone EXE using PyInstaller.

Step 1 Build as a single-file executable (--onefile)
```bash
pyinstaller --onefile --windowed --add-data "tesseract;tesseract" --add-data "poppler;poppler" ocr_pdf_gui.py
```

Notes:

--add-data "source;dest": includes folders in the bundle.

On Linux/macOS, use : instead of ;:
```bash
pyinstaller --onefile --windowed --add-data "tesseract:tesseract" --add-data "poppler:poppler" ocr_pdf_gui.py
```

Resulting EXE will be in dist/ocr_pdf_gui.exe.

The EXE automatically uses bundled Tesseract and Poppler, no path selection needed.

Step 2 Build as a folder (--onedir) — faster for testing
```
pyinstaller --windowed --add-data "tesseract;tesseract" --add-data "poppler;poppler" ocr_pdf_gui.py
```

Creates dist/ocr_pdf_gui/ folder with all files.

Useful for debugging without waiting for compression of --onefile.

---

## Usage Guide
1. Run the application
   - Double-click `ocr_pdf_gui.exe` (or run `python ocr_pdf_gui.py` if testing with Python).

2. Select input PDF
   - Click the "Browse" button and select a PDF file.

3. Choose OCR language(s)
   - Default is "eng" (English).  
   - For multiple languages: "eng+deu" (English + German), etc.

4. Start OCR
   - Click "Start OCR".  
   - The log window shows progress for each page.

5. Wait for completion
   - Once done, a message box will show the path of the generated searchable PDF.  
   - The output file will be in the same folder as the input PDF, with "_OCR" appended.

---


## Licensing

### Tesseract OCR
- License: Apache License 2.0  
- Official: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)

### Poppler
- License: GPLv2  
- Official: [https://poppler.freedesktop.org/](https://poppler.freedesktop.org/)

> Make sure to comply with the **respective licenses** when redistributing binaries.
