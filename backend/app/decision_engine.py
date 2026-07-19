def make_decision(risk_result, verification_result):

    score = risk_result["risk_score"]

    if verification_result["overall_status"] == "Rejected":
        return {
            "status": "REJECTED",
            "emoji": "❌",
            "reason": "Policy verification failed or claim exceeds coverage."
        }

    if score >= 85:
        return {
            "status": "APPROVED",
            "emoji": "✅",
            "reason": "All verification checks passed successfully."
        }

    if score >= 60:
        return {
            "status": "MANUAL REVIEW",
            "emoji": "🟡",
            "reason": "Some verification checks require manual review."
        }

    return {
        "status": "HIGH RISK",
        "emoji": "🔴",
        "reason": "Multiple fraud indicators detected."
    }