import json

def verify_policy(policy_number):

    with open("knowledge_base/policies/policies.json", "r") as f:
        policies = json.load(f)

    for policy in policies:
        if policy["policy_number"] == policy_number:
            return policy

    return None