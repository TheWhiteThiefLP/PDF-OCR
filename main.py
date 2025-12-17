import os
import sys
import threading
import tempfile
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from pdf2image import convert_from_path
import pytesseract

# ==========================
# DEFAULT CONFIG
# ==========================

DEFAULT_TESSERACT = r"/usr/bin/tesseract"  # Change if needed
DEFAULT_POPPLER = r"/usr/bin"              # Change if needed
DEFAULT_LANG = "eng"
DEFAULT_DPI = 300


class OCRApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF OCR → Searchable PDF")
        self.geometry("650x450")
        self.resizable(False, False)

        self.input_pdf = tk.StringVar()
        self.output_pdf = tk.StringVar()
        self.tesseract_path = tk.StringVar(value=DEFAULT_TESSERACT)
        self.poppler_path = tk.StringVar(value=DEFAULT_POPPLER)
        self.lang = tk.StringVar(value=DEFAULT_LANG)

        self.create_widgets()

    def create_widgets(self):
        pad = {"padx": 10, "pady": 5}

        tk.Label(self, text="Input PDF").grid(row=0, column=0, sticky="w", **pad)
        tk.Entry(self, textvariable=self.input_pdf, width=60).grid(row=0, column=1, **pad)
        tk.Button(self, text="Browse", command=self.browse_input).grid(row=0, column=2, **pad)

        tk.Label(self, text="Output PDF").grid(row=1, column=0, sticky="w", **pad)
        tk.Entry(self, textvariable=self.output_pdf, width=60).grid(row=1, column=1, **pad)
        tk.Button(self, text="Browse", command=self.browse_output).grid(row=1, column=2, **pad)

        tk.Label(self, text="Tesseract Path").grid(row=2, column=0, sticky="w", **pad)
        tk.Entry(self, textvariable=self.tesseract_path, width=60).grid(row=2, column=1, **pad)
        tk.Button(self, text="Browse", command=self.browse_tesseract).grid(row=2, column=2, **pad)

        tk.Label(self, text="Poppler Bin Path").grid(row=3, column=0, sticky="w", **pad)
        tk.Entry(self, textvariable=self.poppler_path, width=60).grid(row=3, column=1, **pad)
        tk.Button(self, text="Browse", command=self.browse_poppler).grid(row=3, column=2, **pad)

        tk.Label(self, text="OCR Language(s)").grid(row=4, column=0, sticky="w", **pad)
        tk.Entry(self, textvariable=self.lang, width=20).grid(row=4, column=1, sticky="w", **pad)
        tk.Label(self, text="e.g. eng or eng+deu").grid(row=4, column=1, sticky="e", padx=10)

        self.log = tk.Text(self, height=12, width=78, state="disabled")
        self.log.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        tk.Button(self, text="Start OCR", height=2, command=self.start_ocr).grid(
            row=6, column=0, columnspan=3, pady=10
        )

    def log_msg(self, msg):
        self.log.config(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.config(state="disabled")

    def browse_input(self):
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if path:
            self.input_pdf.set(path)

    def browse_output(self):
        path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if path:
            self.output_pdf.set(path)

    def browse_tesseract(self):
        path = filedialog.askopenfilename()
        if path:
            self.tesseract_path.set(path)

    def browse_poppler(self):
        path = filedialog.askdirectory()
        if path:
            self.poppler_path.set(path)

    def start_ocr(self):
        if not self.input_pdf.get() or not self.output_pdf.get():
            messagebox.showerror("Error", "Please select input and output PDFs.")
            return

        threading.Thread(target=self.run_ocr, daemon=True).start()

    def run_ocr(self):
        try:
            pytesseract.pytesseract.tesseract_cmd = self.tesseract_path.get()
            self.log_msg("Converting PDF to images...")

            with tempfile.TemporaryDirectory() as tmpdir:
                pages = convert_from_path(
                    self.input_pdf.get(),
                    dpi=DEFAULT_DPI,
                    poppler_path=self.poppler_path.get(),
                    fmt="png",
                    output_folder=tmpdir
                )

                self.log_msg(f"Total pages: {len(pages)}")

                pdf_pages = []
                for i, page in enumerate(pages, 1):
                    self.log_msg(f"OCR page {i}/{len(pages)}")
                    pdf_bytes = pytesseract.image_to_pdf_or_hocr(
                        page,
                        lang=self.lang.get(),
                        extension="pdf"
                    )
                    page_pdf = os.path.join(tmpdir, f"page_{i}.pdf")
                    with open(page_pdf, "wb") as f:
                        f.write(pdf_bytes)
                    pdf_pages.append(page_pdf)

                self.log_msg("Merging pages...")
                subprocess.run(["pdfunite", *pdf_pages, self.output_pdf.get()], check=True)

            self.log_msg("DONE ✔ Searchable PDF created")
            messagebox.showinfo("Success", "OCR completed successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = OCRApp()
    app.mainloop()
