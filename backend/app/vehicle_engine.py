import json

VEHICLE_DB = "knowledge_base/vehicles/vehicles.json"


def verify_vehicle(claim):

    with open(VEHICLE_DB, "r", encoding="utf-8") as f:
        vehicles = json.load(f)

    policy_number = claim.get("policy_number")

    for vehicle in vehicles:

        if vehicle["policy_number"] == policy_number:

            return {
                "vehicle_found": True,
                "owner_match": vehicle["owner"].lower() == claim.get("customer_name", "").lower(),
                "registration_valid": vehicle["registration_valid"],
                "insurance_status": vehicle["insurance_status"],
                "vehicle": vehicle
            }

    return {
        "vehicle_found": False,
        "owner_match": False,
        "registration_valid": False,
        "insurance_status": "Unknown",
        "vehicle": None
    }