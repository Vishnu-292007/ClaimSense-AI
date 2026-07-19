from app.gemini import ask_gemini


def generate_report(claim_data, verification_result):

    prompt = f"""
You are an Expert Insurance Claim Verification Officer.

Your job is to generate a professional claim verification report.

==================================================
CLAIM DETAILS
==================================================

{claim_data}

==================================================
VERIFICATION RESULTS
==================================================

Overall Status:
{verification_result.get("overall_status")}

Decision:
{verification_result.get("decision")}

Verification Checks:
{verification_result.get("checks")}

Customer Verification:
{verification_result.get("customer_verification")}

Claim History:
{verification_result.get("claim_history")}

Fraud Analysis:
{verification_result.get("fraud_analysis")}

Vehicle Verification:
{verification_result.get("vehicle_verification")}

Duplicate Claim:
{verification_result.get("duplicate_claim")}

Risk Analysis:
{verification_result.get("risk_analysis")}

==================================================
STRICT INSTRUCTIONS
==================================================

1. NEVER invent information.

2. ONLY use the data provided above.

3. NEVER contradict the verification results.

4. If Customer Verification reports a mismatch,
   clearly state:
   "Customer name mismatch detected. Manual verification required."

5. Mention every failed verification check.

6. If documents are missing,
   list every missing document.

7. There are TWO different scores.

   Fraud Score
   = fraud_analysis["fraud_score"]

   Overall Risk Score
   = risk_analysis["risk_score"]

   NEVER confuse these.

8. Fraud Score measures fraud suspicion.

9. Overall Risk Score measures final insurance risk.

10. Display BOTH separately.

11. The Final Decision MUST match the verification decision exactly.

12. If Manual Review is required,
    explain WHY using the verification results.

13. Never say database records match if customer verification reports a mismatch.

14. If hospital is not mentioned for a Motor Insurance claim,
    do NOT treat it as an error.

==================================================
OUTPUT FORMAT
==================================================

# Claim Verification Report

## 1. Claim Summary

- Claim ID
- Customer Name
- Policy Number
- Claim Amount
- Claim Reason

## 2. Verification Findings

Mention

✔ Successful checks

❌ Failed checks

⚠ Manual review reasons

## 3. Fraud Analysis

Display

Fraud Score

Fraud Level

Fraud Reasons

## 4. Risk Analysis

Display

Overall Risk Score

Overall Risk Level

Explain why this score was assigned.

## 5. Final Decision

Use exactly the provided decision.

## 6. Recommendation

Provide short professional recommendations based ONLY on verification results.

Keep the report concise, professional and suitable for an insurance officer.
"""

    try:
        return ask_gemini("", prompt)

    except Exception as e:

        return f"""
CLAIM VERIFICATION REPORT

Claim ID:
{claim_data.get("claim_id")}

Customer:
{claim_data.get("customer_name")}

Policy:
{claim_data.get("policy_number")}

Overall Status:
{verification_result.get("overall_status")}

Decision:
{verification_result.get("decision")}

Checks:
{chr(10).join(verification_result.get("checks", []))}

Risk Analysis:
{verification_result.get("risk_analysis")}

Fraud Analysis:
{verification_result.get("fraud_analysis")}

Recommendation:
Manual verification recommended.

(AI Report generation unavailable: {str(e)})
"""