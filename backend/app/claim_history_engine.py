import json

CLAIM_HISTORY_DB = "knowledge_base/claim_history/claim_history.json"


def check_claim_history(claim):

    with open(CLAIM_HISTORY_DB, "r", encoding="utf-8") as f:
        history = json.load(f)

    policy_number = claim.get("policy_number")

    previous_claims = []

    for record in history:
        if record["policy_number"] == policy_number:
            previous_claims.append(record)

    return {
        "previous_claims_count": len(previous_claims),
        "previous_claims": previous_claims
    }