def calculate_risk_score(
    verification_result,
    customer_result,
    vehicle_result,
    claim_history_result,
    duplicate_result,
    fraud_result
):

    score = 100
    reasons = []

    # Overall status
    if verification_result["overall_status"] == "Manual Review":
        score -= 35
        reasons.append("Manual review required")

    elif verification_result["overall_status"] == "Rejected":
        score -= 60
        reasons.append("Claim rejected")

    # Customer
    if not customer_result["customer_found"]:
        score -= 30
        reasons.append("Customer not found")

    if not customer_result["name_match"]:
        score -= 20
        reasons.append("Customer name mismatch")

    # Vehicle
    if not vehicle_result["vehicle_found"]:
        score -= 20
        reasons.append("Vehicle not found")

    if not vehicle_result["owner_match"]:
        score -= 15
        reasons.append("Vehicle owner mismatch")

    # Previous Claims
    if claim_history_result["previous_claims_count"] >= 3:
        score -= 15
        reasons.append("Too many previous claims")

    # Duplicate Claim
    if duplicate_result["duplicate_found"]:
        score -= 30
        reasons.append("Duplicate claim detected")

    # Fraud
    score -= fraud_result["fraud_score"]

    if score < 0:
        score = 0

    # Risk Level
    if score >= 80:
        level = "LOW RISK"
    elif score >= 50:
        level = "MEDIUM RISK"
    else:
        level = "HIGH RISK"

    return {
        "risk_score": score,
        "risk_level": level,
        "reasons": reasons
    }