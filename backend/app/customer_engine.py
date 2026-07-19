import json

CUSTOMER_DB = "knowledge_base/customers/customers.json"


def verify_customer(claim):

    with open(CUSTOMER_DB, "r", encoding="utf-8") as f:
        customers = json.load(f)

    customer_name = str(claim.get("customer_name", "")).strip().lower()
    policy_number = str(claim.get("policy_number", "")).strip()

    for customer in customers:

        if customer["policy_number"] == policy_number:

            result = {
                "customer_found": True,
                "name_match": customer["name"].lower() == customer_name,
                "customer": customer
            }

            return result

    return {
        "customer_found": False,
        "name_match": False,
        "customer": None
    }