from fastapi import APIRouter
from pydantic import BaseModel
from app.search import search
from app.gemini import ask_gemini
router = APIRouter()

class Question(BaseModel):
    question: str

@router.post("/ask")
async def ask_question(data: Question):
    results = search(data.question)

    context = "\n".join(results)

    answer = ask_gemini(context, data.question)

    return {
        "question": data.question,
        "answer": answer
    }