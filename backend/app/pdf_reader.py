import os
import numpy as np
import pdfplumber
import easyocr
from pdf2image import convert_from_path

reader = easyocr.Reader(["en"], gpu=False)

POPPLER_PATH = r"C:\poppler-26.02.0\Library\bin"


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

    images = convert_from_path(
        pdf_path,
        poppler_path=POPPLER_PATH
    )

    for image in images:
        image = np.array(image)
        result = reader.readtext(image, detail=0)
        text += " ".join(result) + "\n"

    return text.strip()


def extract_text_from_image(image_path):
    image = np.array(image_path)
    result = reader.readtext(image_path, detail=0)
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