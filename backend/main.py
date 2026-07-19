from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.upload import router as upload_router
from app.chat import router as chat_router
from app.kb_upload import router as kb_router
app = FastAPI(title="ClaimSense AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(kb_router)
@app.get("/")
def home():
    return {
        "message": "ClaimSense AI Backend is Running!"
    }