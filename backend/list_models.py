from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

print("API Key:", os.getenv("GOOGLE_API_KEY"))

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

for model in client.models.list():
    print(model.name)