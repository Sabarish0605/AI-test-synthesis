from requirement_engine import extract_requirement
from test_engine import generate_test_cases, TestArtifactGenerator
import json

def test_spec_v2():
    print("--- TESTING REFINED QA ARCHITECT SYSTEM (SPEC V2) ---")
    
    # Testing expansion logic with a short requirement
    requirement = "Login with mobile number and OTP."
    
    print("\n1. Testing Expansion & Phase 1...")
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
    
    print("\n2. Testing Workflow Tests & Phase 2...")
    test_cases = generate_test_cases(test_engine_data)
    print(f"Generated {len(test_cases)} test cases.")
    workflow_tcs = [tc for tc in test_cases if "workflow" in tc.get("title", "").lower() or tc.get("type") == "Workflow"]
    print(f"Workflow Test Cases found: {len(workflow_tcs)}")
    
    print("\n3. Testing Strict Automation Output & Phase 3...")
    engine = TestArtifactGenerator()
    java_code = engine.generate_selenium_java(test_engine_data)
    
    print(f"Generated {len(java_code)} chars of Java code.")
    print("Code starts with 'package':", java_code.strip().startswith("package"))
    print("Code ends with '}':", java_code.strip().endswith("}"))
    print("Contains 'By.id':", "By.id" in java_code)
    print("Contains markdown block '```':", "```" in java_code)
    
    print("\n--- TEST COMPLETE ---")

if __name__ == "__main__":
    test_spec_v2()
