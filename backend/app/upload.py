from fastapi import APIRouter, UploadFile, File
import os

from app.pdf_reader import extract_text
from app.text_chunker import chunk_text
from app.embeddings import create_embeddings
from app.vector_store import store_embeddings
from app.extractor import extract_claim_details
from app.verifier import verify_claim
from app.report_generator import generate_report
from app.cross_checker import cross_check

router = APIRouter()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_pdf(files: list[UploadFile] = File(...)):

    combined_text = ""
    uploaded_files = []
    uploaded_texts = {}

    for file in files:

        extension = os.path.splitext(file.filename)[1].lower()

        if extension not in [".pdf", ".jpg", ".jpeg", ".png"]:
            return {
                "error": f"{file.filename} is not a supported file type."
            }

        uploaded_files.append(file.filename)

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        text = extract_text(file_path)
        print("\n==========================")
        print(file.filename)
        print(text)
        print("==========================\n")
        uploaded_texts[file.filename.lower()] = text

        combined_text += "\n\n" + text

    claim_data = extract_claim_details(combined_text)

    verification_result = verify_claim(
        claim_data,
        uploaded_files
    )

    verification_result["checks"].extend(
        cross_check(
            claim_data,
            uploaded_texts
        )
    )

    report = generate_report(
        claim_data,
        verification_result
    )

    print("\n========== CLAIM DETAILS ==========")
    print(claim_data)
    print("===================================\n")

    chunks = chunk_text(combined_text)

    print("Total Chunks:", len(chunks))

    embeddings = create_embeddings(chunks)

    print("Embeddings Shape:", embeddings.shape)

    store_embeddings(embeddings, chunks)

    print("Embeddings stored successfully.")

    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1}:\n")
        print(chunk)

    return {
        "uploaded_files": uploaded_files,
        "claim_data": claim_data,
        "verification": verification_result,
        "report": report,
        "text": combined_text[:1000]
    }