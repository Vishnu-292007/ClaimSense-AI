import re
from app.policy_checker import verify_policy
from app.hospital_checker import verify_hospital
from app.document_checker import verify_documents


def verify_claim(claim, uploaded_files):

    report = {
        "checks": [],
        "overall_status": "Verified"
    }

    policy = verify_policy(claim.get("policy_number"))

    claim_amount = 0

    if claim.get("claim_amount"):
        amount = str(claim["claim_amount"])
        amount = re.sub(r"[^0-9]", "", amount)

        if amount:
            claim_amount = int(amount)

    if policy is None:
        report["checks"].append("❌ Policy not found")
        report["overall_status"] = "Manual Review"

    else:
        report["checks"].append("✅ Valid policy found")

        coverage = policy["coverage_amount"]

        if claim_amount > coverage:
            report["checks"].append(
                f"❌ Claim amount exceeds coverage (₹{coverage})"
            )
            report["overall_status"] = "Rejected"
        else:
            report["checks"].append(
                f"✅ Claim amount is within coverage (₹{coverage})"
            )

    if not claim.get("claim_amount"):
        report["checks"].append("❌ Claim amount missing")
        report["overall_status"] = "Manual Review"
    else:
        report["checks"].append("✅ Claim amount found")

    hospital = verify_hospital(claim.get("hospital"))

    if claim.get("hospital") is None:
        report["checks"].append("⚠ Hospital not mentioned")

    elif hospital is None:
        report["checks"].append("❌ Hospital not in network")
        report["overall_status"] = "Manual Review"

    elif hospital["cashless"]:
        report["checks"].append("✅ Network hospital (Cashless Available)")

    else:
        report["checks"].append("⚠ Hospital found (Cashless Not Available)")

    documents = verify_documents(uploaded_files)

    if len(documents["missing"]) == 0:
        report["checks"].append("✅ All required documents submitted")
    else:
        report["checks"].append(
            "⚠ Missing Documents: " +
            ", ".join(documents["missing"])
        )
        report["overall_status"] = "Manual Review"

    if report["overall_status"] == "Verified":
        report["decision"] = "✅ APPROVED"

    elif report["overall_status"] == "Rejected":
        report["decision"] = "❌ REJECTED"

    else:
        report["decision"] = "🟡 MANUAL REVIEW REQUIRED"

    return report