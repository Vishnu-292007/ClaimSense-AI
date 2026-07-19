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
from app.customer_engine import verify_customer
from app.claim_history_engine import check_claim_history
from app.fraud_engine import detect_fraud
from app.vehicle_engine import verify_vehicle
from app.duplicate_claim_engine import detect_duplicate_claim
from app.risk_score import calculate_risk_score

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

    # Customer Verification
    customer_result = verify_customer(claim_data)
    verification_result["customer_verification"] = customer_result

    # Claim History
    claim_history_result = check_claim_history(claim_data)
    verification_result["claim_history"] = claim_history_result

    # Fraud Analysis
    fraud_result = detect_fraud(
        claim_data,
        customer_result,
        claim_history_result
    )
    verification_result["fraud_analysis"] = fraud_result

    # Vehicle Verification
    vehicle_result = verify_vehicle(claim_data)
    verification_result["vehicle_verification"] = vehicle_result

    # Duplicate Claim Detection
    duplicate_result = detect_duplicate_claim(claim_data)
    verification_result["duplicate_claim"] = duplicate_result

    # Cross Check Documents
    verification_result["checks"].extend(
        cross_check(
            claim_data,
            uploaded_texts
        )
    )

    # -----------------------------
    # Risk Score Calculation
    # -----------------------------
    risk_result = calculate_risk_score(
    verification_result,
    customer_result,
    vehicle_result,
    claim_history_result,
    duplicate_result,
    fraud_result
    )

    verification_result["risk_analysis"] = risk_result

    # AI Report
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