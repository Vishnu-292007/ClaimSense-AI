import json

def verify_hospital(hospital_name):

    if not hospital_name:
        return None

    with open("knowledge_base/hospitals/hospitals.json", "r") as f:
        hospitals = json.load(f)

    for hospital in hospitals:
        if hospital["hospital"].lower() == hospital_name.lower():
            return hospital

    return None