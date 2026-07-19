import re

def clean_amount(amount):
    if amount is None:
        return None

    amount = str(amount)
    amount = re.sub(r"[^0-9]", "", amount)

    if amount == "":
        return None

    return int(amount)


def extract_estimate_amount(text):
    match = re.search(
        r"(?:Total|Grand Total|Estimate Amount)[^\d]*(\d[\d,]*)",
        text,
        re.IGNORECASE
    )

    if match:
        return int(match.group(1).replace(",", ""))

    numbers = re.findall(r"\d[\d,]*", text)

    amounts = []

    for n in numbers:
        value = int(n.replace(",", ""))

        if value > 1000:
            amounts.append(value)

    if amounts:
        return max(amounts)

    return None


def cross_check(claim_data, uploaded_texts):

    checks = []

    policy_text = ""
    aadhaar_text = ""
    estimate_text = ""
    claim_text = ""

    for filename, text in uploaded_texts.items():

        name = filename.lower()

        if "policy" in name:
            policy_text = text

        elif "aadhaar" in name or "aadhar" in name:
            aadhaar_text = text

        elif "estimate" in name:
            estimate_text = text

        elif "claim" in name:
            claim_text = text

    print("\n===== OCR Aadhaar Text =====")
    print(aadhaar_text)
    print("============================\n")

    if claim_data.get("policy_number") and claim_data["policy_number"] in policy_text:
        checks.append("✅ Policy number matches policy document")
    else:
        checks.append("❌ Policy number mismatch")

    claim_name = claim_data.get("customer_name", "").lower().strip()
    aadhaar = aadhaar_text.lower()

    if claim_name in aadhaar:
        checks.append("✅ Customer name matches Aadhaar")
    else:
        checks.append("❌ Customer name mismatch")

    claim_amount = clean_amount(claim_data.get("claim_amount"))
    estimate_amount = extract_estimate_amount(estimate_text)

    if claim_amount is not None and estimate_amount is not None:
        if claim_amount == estimate_amount:
            checks.append("✅ Claim amount matches repair estimate")
        else:
            checks.append(
                f"❌ Claim Amount ₹{claim_amount} != Estimate ₹{estimate_amount}"
            )

    return checks