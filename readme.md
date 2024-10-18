# PDF Number Search

A short Python script that searches though the text of a PDF document for
numbers, and returns the largest one found.

`python pdf_numbers.py /path/to/file.pdf` to run the script.

Python dependencies include `pillow`, `pymupdf`, `pypdf`, and `pytesseract`, all
installable through `pip install <package name>`. You may be able to install all
of them by running `pip install -r requirements.txt`.

You will also need to install [Tesseract][] outside of Python in order for the
OCR component of the script to function.

[Tesseract]: https://tesseract-ocr.github.io/tessdoc/Installation.html
