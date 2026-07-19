from google import genai
import os

print("Loaded gemini.py")

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

def ask_gemini(context, question):

    prompt = f"""
You are an insurance claim assistant.

Context:
{context}

Question:
{question}

Answer:
"""

    print("Using model: gemini-3.5-flash")

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text