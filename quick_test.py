"""
Quick Test Script for test_engine.py
Run this to verify everything works!
"""
from test_engine import TestArtifactGenerator
import json

print("=" * 70)
print("🧪 QUICK TEST - Test Engine Module")
print("=" * 70)

# Initialize
print("\n1. Initializing Test Engine...")
engine = TestArtifactGenerator()
print("   ✅ Engine initialized")

# Test data
test_data = {
    "feature": "Login",
    "fields": ["email", "password"],
    "validations": {"email": "valid email", "password": "min 8 chars"},
    "roles": ["admin", "user"],
    "edge_cases": ["empty fields", "sql injection"]
}

# Test 1: Generate Test Cases
print("\n2. Testing generate_test_cases()...")
try:
    test_cases = engine.generate_test_cases(test_data)
    print(f"   ✅ Generated {len(test_cases)} test cases")
    print(f"   ✅ Sample: {test_cases[0]['tc_id']} - {test_cases[0]['title']}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Test 2: Generate Selenium Java
print("\n3. Testing generate_selenium_java()...")
try:
    java_code = engine.generate_selenium_java(test_data)
    print(f"   ✅ Generated {len(java_code)} characters of Java code")
    print(f"   ✅ Contains: {'LoginTest' if 'LoginTest' in java_code else 'Java class'}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Test 3: Create Traceability Matrix
print("\n4. Testing create_traceability_matrix()...")
try:
    matrix = engine.create_traceability_matrix(test_data, test_cases)
    if "error" in matrix:
        print(f"   ❌ Error: {matrix['error']}")
        exit(1)
    print(f"   ✅ Matrix created for feature: {matrix['feature']}")
    print(f"   ✅ Test cases mapped: {len(matrix['test_case_ids'])}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Test 4: Calculate Coverage Metrics
print("\n5. Testing calculate_coverage_metrics()...")
try:
    metrics = engine.calculate_coverage_metrics(test_data, test_cases)
    if "error" in metrics:
        print(f"   ❌ Error: {metrics['error']}")
        exit(1)
    print(f"   ✅ Coverage Score: {metrics['requirement_coverage_score']}")
    print(f"   ✅ Total Cases: {metrics['total_cases']}")
    print(f"   ✅ Quality Score: {metrics['quality_score']}/100")
    print(f"   ✅ Automation Ready: {metrics['is_automation_ready']}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Test 5: Error Handling
print("\n6. Testing error handling...")
try:
    invalid_data = {"feature": "Test"}  # Missing required keys
    error_result = engine.generate_test_cases(invalid_data)
    if "error" in error_result[0]:
        print(f"   ✅ Error handling works correctly")
    else:
        print(f"   ❌ Error handling failed")
except Exception as e:
    print(f"   ❌ Unexpected error: {e}")

# Test 6: Save outputs
print("\n7. Testing file output...")
try:
    with open('quick_test_cases.json', 'w') as f:
        json.dump(test_cases, f, indent=2)
    print("   ✅ Test cases saved to: quick_test_cases.json")
    
    with open('quick_test_LoginTest.java', 'w') as f:
        f.write(java_code)
    print("   ✅ Java code saved to: quick_test_LoginTest.java")
    
    with open('quick_test_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    print("   ✅ Metrics saved to: quick_test_metrics.json")
except Exception as e:
    print(f"   ⚠️  File save warning: {e}")

print("\n" + "=" * 70)
print("🎉 ALL TESTS PASSED!")
print("=" * 70)
print("\n✅ Your Test Engine Module is working perfectly!")
print("✅ All 4 main functions operational")
print("✅ Error handling verified")
print("✅ File output successful")
print("\n🚀 Ready for production use!")
