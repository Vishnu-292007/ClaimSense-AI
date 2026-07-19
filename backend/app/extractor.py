from app.gemini import ask_gemini
import json

def extract_claim_details(text):
    prompt = f"""
You are an insurance claim extraction AI.

Extract the following information from the insurance claim.

Return ONLY valid JSON.

If a field is missing, return null.

{{
  "claim_id":"",
  "customer_name":"",
  "policy_number":"",
  "hospital":"",
  "claim_amount":"",
  "incident_date":"",
  "status":"",
  "reason":"",
  "documents":[]
}}

Claim:
{text}
"""

    response = ask_gemini("", prompt)

    response = response.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(response)
    except:
        return {
            "error": "Failed to parse Gemini response",
            "raw_response": response
        }