def detect_fraud(claim, customer_result, claim_history_result):

    fraud_score = 0
    reasons = []

    if not customer_result["customer_found"]:
        fraud_score += 40
        reasons.append("Customer not found")

    if not customer_result["name_match"]:
        fraud_score += 30
        reasons.append("Customer name mismatch")

    if claim_history_result["previous_claims_count"] >= 3:
        fraud_score += 20
        reasons.append("Multiple previous claims")

    amount = claim.get("claim_amount", "")

    if isinstance(amount, str):
        amount = amount.replace("₹", "").replace(",", "").replace("n", "").strip()

    try:
        amount = float(amount)
    except:
        amount = 0

    if amount > 100000:
        fraud_score += 10
        reasons.append("High claim amount")

    if fraud_score >= 60:
        level = "HIGH"
    elif fraud_score >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "fraud_score": fraud_score,
        "risk_level": level,
        "reasons": reasons
    }