from requirement_engine import extract_requirement
from test_engine import generate_test_cases, TestArtifactGenerator
import json

def test_pipeline():
    print("--- TESTING INTEGRATED QA ARCHITECT SYSTEM ---")
    
    requirement = """
    Feature: User Registration
    Requirement: Users can register with username, email, password, and age.
    - Username: Required, 5-20 chars.
    - Email: Must be valid format.
    - Password: Strong password required (min 8 chars, 1 uppercase, 1 number).
    - Age: Must be between 18 and 120.
    Role: Guest
    """
    
    print("\n1. Extracting Requirement (Phase 1)...")
    structured_data = extract_requirement(requirement)
    print(json.dumps(structured_data, indent=2))
    
    test_engine_data = {
        "feature": structured_data.get("feature_name", "Unknown"),
        "functional_fields": structured_data.get("functional_fields", []),
        "validations": structured_data.get("validations", {}),
        "roles": structured_data.get("actors", []),
        "edge_cases": structured_data.get("edge_cases", []),
        "risk_analysis": structured_data.get("risk_analysis", {})
    }
    
    print("\n2. Generating Test Cases (Phase 2)...")
    test_cases = generate_test_cases(test_engine_data)
    print(f"Generated {len(test_cases)} test cases.")
    if test_cases:
        print(f"Sample TC IDs: {[tc['tc_id'] for tc in test_cases[:3]]}")
    
    print("\n3. Generating Automation Script (Phase 3)...")
    engine = TestArtifactGenerator()
    java_code = engine.generate_selenium_java(test_engine_data)
    print(f"Generated {len(java_code)} chars of Java code.")
    print("Code preview (first 100 chars):")
    print(java_code[:100])
    
    print("\n4. Creating Traceability Map (Phase 4)...")
    traceability = engine.create_traceability_matrix(test_engine_data, test_cases)
    print(json.dumps(traceability, indent=2))
    
    print("\n--- TEST COMPLETE ---")

if __name__ == "__main__":
    test_pipeline()
