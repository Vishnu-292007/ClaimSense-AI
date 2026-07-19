from fastapi import APIRouter
from pydantic import BaseModel

from app.search import search
from app.gemini import ask_gemini

router = APIRouter()


class Question(BaseModel):
    question: str


@router.post("/ask")
async def ask_question(data: Question):

    # Search relevant chunks from vector database
    results = search(data.question)

    # No matching information found
    if not results:
        return {
            "question": data.question,
            "context_used": 0,
            "answer": "Sorry, I couldn't find any relevant information in the insurance knowledge base."
        }

    # Combine retrieved chunks
    context = "\n\n".join(results)

    # Ask Gemini using retrieved context
    answer = ask_gemini(context, data.question)

    return {
        "question": data.question,
        "context_used": len(results),
        "retrieved_chunks": results,
        "answer": answer
    }