from fastapi import APIRouter, UploadFile, File
import os

router = APIRouter()

BASE_FOLDER = "knowledge_base"

@router.post("/kb/upload/{category}")
async def upload_kb(category: str, file: UploadFile = File(...)):
    folder = os.path.join(BASE_FOLDER, category)
    os.makedirs(folder, exist_ok=True)

    file_path = os.path.join(folder, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {
        "message": "Knowledge Base file uploaded successfully",
        "category": category,
        "filename": file.filename
    }