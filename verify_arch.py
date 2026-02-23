from requirement_engine import extract_requirement, compare_requirements
from test_engine import generate_test_cases
import json

def test_workflow():
    print("--- Phase 1: Requirement Extraction ---")
    raw_req = "User Login: Users must be able to login with email and password. Email must be valid format. Password must be at least 8 characters."
    structured = extract_requirement(raw_req)
    print(json.dumps(structured, indent=2))

    print("\n--- Phase 2: Test Case Generation ---")
    test_engine_data = {
        "feature": structured.get("feature_name", "Unknown"),
        "fields": structured.get("fields", []),
        "validations": structured.get("validations", {}),
        "roles": structured.get("actors", []),
        "edge_cases": structured.get("edge_cases", [])
    }
    test_cases = generate_test_cases(test_engine_data)
    print(f"Generated {len(test_cases)} test cases.")
    if test_cases:
        print(f"First TC: {test_cases[0].get('tc_id')} - {test_cases[0].get('title')}")

    print("\n--- Phase 5: Change Detection ---")
    old_req = "Login with email."
    new_req = "Login with email and password."
    diff = compare_requirements(old_req, new_req)
    print(json.dumps(diff, indent=2))

if __name__ == "__main__":
    test_workflow()
