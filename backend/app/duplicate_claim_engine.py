import json

CLAIM_HISTORY_DB = "knowledge_base/claim_history/claim_history.json"


def detect_duplicate_claim(claim):

    with open(CLAIM_HISTORY_DB, "r", encoding="utf-8") as f:
        history = json.load(f)

    policy = str(claim.get("policy_number", "")).strip()
    date = str(claim.get("incident_date", "")).strip()

    matches = []

    for record in history:
        if (
            record["policy_number"] == policy
            and record["incident_date"] == date
        ):
            matches.append(record)

    return {
        "duplicate_found": len(matches) > 0,
        "count": len(matches),
        "matches": matches
    }