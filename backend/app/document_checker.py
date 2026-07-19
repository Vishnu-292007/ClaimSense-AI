import os

REQUIRED_DOCUMENTS = {
    "aadhaar": "Aadhaar Card",
    "license": "Driving License",
    "policy": "Insurance Policy",
    "rc": "Vehicle RC",
    "estimate": "Repair Estimate"
}

def verify_documents(uploaded_files):

    available = []
    missing = []

    filenames = [os.path.basename(f).lower() for f in uploaded_files]

    for keyword, name in REQUIRED_DOCUMENTS.items():

        found = False

        for file in filenames:
            if keyword in file:
                found = True
                break

        if found:
            available.append(name)
        else:
            missing.append(name)

    return {
        "available": available,
        "missing": missing
    }