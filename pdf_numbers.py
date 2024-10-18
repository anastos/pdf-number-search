#!/usr/bin/env python3

import fitz
import PIL
import pypdf
import pytesseract
import re
import sys

# Searches input string for numbers, returns all found numbers
# with their original string representations and float values
def find_numbers(string: str) -> list[tuple[float, str]]:
    # matches numbers with (or without) comma separators,
    # decimal point, or scientific notation
    regex = re.compile("\d+(,\d{3})*(\.\d+)?([eE][+-]?\d+)?")
    matches = regex.finditer(string)

    numbers = []
    for match in matches:
        number_str = match.group(0)
        # remove any commas and parse string as float
        number = float(number_str.replace(",", ""))
        numbers.append((number, number_str))

    return list(numbers)

# Opens PDF file from path argument, returns the largest number in the document
# (in float and original string form) or None if no numbers are found
def max_number_pdf(file_path: str) -> tuple[float, str]:

    pdf_reader = pypdf.PdfReader(file_path) # default reader for native-text PDFs
    pdf_document = fitz.open(file_path) # backup for scanned PDFs

    max_num = (float("-inf"), None)
    for i, page in enumerate(pdf_reader.pages):
        page_str = page.extract_text()

        # if no native text on page, use OCR
        if page_str == "":
            page = pdf_document.load_page(i)
            pixmap = page.get_pixmap(dpi=500) # high DPI to improve OCR accuracy
            image = PIL.Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
            page_str = pytesseract.image_to_string(image)

        page_numbers = find_numbers(page_str)

        for (n, s) in page_numbers:
            if max_num[0] < n:
                max_num = (n, s)

    if max_num[1] == None:
        return None
    else:
        return max_num

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Usage: python pdf_numbers.py /path/to/file.pdf")
        sys.exit(1)

    pdf_path = sys.argv[1]

    try:
        max_num = max_number_pdf(pdf_path)
    except:
        # file not found or non-PDF file
        print("Could not parse file as PDF: '" + pdf_path + "'")
        sys.exit(1)

    if max_num == None:
        print("No numbers found in document.")
    else:
        print(max_num[1])
