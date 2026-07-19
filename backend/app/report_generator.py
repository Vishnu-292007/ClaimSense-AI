from app.gemini import ask_gemini

def generate_report(claim, verification):

    prompt = f"""
You are an insurance claim verification officer.

Claim Details:
{claim}

Verification Result:
{verification}

Generate a professional report.

Include:
1. Claim Summary
2. Verification Findings
3. Final Decision
4. Recommendation

Keep it under 200 words.
"""

    return ask_gemini("", prompt)