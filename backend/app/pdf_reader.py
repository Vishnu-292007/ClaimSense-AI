import os
import numpy as np
import pdfplumber
import easyocr
from pdf2image import convert_from_path

reader = None


def get_reader():
    global reader

    if reader is None:
        print("Loading EasyOCR model...")
        reader = easyocr.Reader(["en"], gpu=False)

    return reader

if os.name == "nt":
    POPPLER_PATH = r"C:\poppler-26.02.0\Library\bin"
else:
    POPPLER_PATH = None


def extract_text_from_pdf(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text.strip()


def extract_text_using_ocr(pdf_path):
    text = ""

    if POPPLER_PATH:
        images = convert_from_path(
            pdf_path,
            poppler_path=POPPLER_PATH
        )
    else:
        images = convert_from_path(pdf_path)

    ocr_reader = get_reader()

    for image in images:
        image = np.array(image)
        result = ocr_reader.readtext(image, detail=0)
        text += " ".join(result) + "\n"

    return text.strip()


def extract_text_from_image(image_path):
    ocr_reader = get_reader()
    result = ocr_reader.readtext(image_path, detail=0)
    return " ".join(result)


def extract_text(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension in [".jpg", ".jpeg", ".png"]:
        print("Image detected. Running OCR...")
        return extract_text_from_image(file_path)

    if extension == ".pdf":
        text = extract_text_from_pdf(file_path)

        if len(text.strip()) > 30:
            print("Text PDF detected")
            return text

        print("Scanned PDF detected. Running OCR...")
        return extract_text_using_ocr(file_path)

    return ""