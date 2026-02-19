"""
Custom Test Template
Copy this file and modify the feature_data to test your own features!
"""
from test_engine import TestArtifactGenerator
import json

# ============================================================================
# CUSTOMIZE YOUR FEATURE HERE
# ============================================================================

# TODO: Replace with your feature details
YOUR_FEATURE = {
    "feature": "User Registration",  # ← Change this to your feature name
    
    "fields": [                       # ← List all input fields
        "email",
        "password",
        "confirm_password",
        "phone",
        "age"
    ],
    
    "validations": {                  # ← Define validation rules
        "email": "valid email format",
        "password": "min 8 chars, 1 uppercase, 1 number, 1 special char",
        "confirm_password": "must match password",
        "phone": "10 digits",
        "age": "between 18 and 120"
    },
    
    "roles": [                        # ← Define user roles
        "new_user",
        "social_signup"
    ],
    
    "edge_cases": [                   # ← List edge cases to test
        "duplicate email",
        "weak password",
        "password mismatch",
        "invalid phone format",
        "underage user",
        "special characters in name",
        "SQL injection attempt"
    ]
}

# ============================================================================
# TEST EXECUTION (No need to change below this line)
# ============================================================================

print("=" * 80)
print(f"Testing Feature: {YOUR_FEATURE['feature']}")
print("=" * 80)

# Initialize Test Engine
print("\n1. Initializing Test Engine...")
engine = TestArtifactGenerator()
print("   ✅ Ready")

# Display input data
print("\n2. Feature Configuration:")
print(f"   Feature Name:     {YOUR_FEATURE['feature']}")
print(f"   Fields:           {len(YOUR_FEATURE['fields'])} fields")
print(f"   Validations:      {len(YOUR_FEATURE['validations'])} rules")
print(f"   Roles:            {len(YOUR_FEATURE['roles'])} roles")
print(f"   Edge Cases:       {len(YOUR_FEATURE['edge_cases'])} cases")

# Generate Test Cases
print("\n3. Generating Test Cases...")
test_cases = engine.generate_test_cases(YOUR_FEATURE)
print(f"   ✅ Generated {len(test_cases)} test cases")

# Show test case distribution
pos_count = sum(1 for tc in test_cases if tc.get('type') == 'Positive')
neg_count = sum(1 for tc in test_cases if tc.get('type') == 'Negative')
bnd_count = sum(1 for tc in test_cases if tc.get('type') == 'Boundary')

print(f"   • Positive Tests:  {pos_count}")
print(f"   • Negative Tests:  {neg_count}")
print(f"   • Boundary Tests:  {bnd_count}")

# Display sample test cases
print("\n4. Sample Test Cases (First 5):")
for i, tc in enumerate(test_cases[:5], 1):
    print(f"\n   [{i}] {tc['tc_id']}: {tc['title']}")
    print(f"       Type: {tc['type']}")
    print(f"       Steps:")
    for j, step in enumerate(tc['steps'][:3], 1):
        print(f"         {j}. {step}")
    if len(tc['steps']) > 3:
        print(f"         ... ({len(tc['steps']) - 3} more steps)")
    print(f"       Expected: {tc['expected_result'][:60]}...")

# Generate Selenium Code
print("\n5. Generating Automation Code...")
java_code = engine.generate_selenium_java(YOUR_FEATURE)
class_name = YOUR_FEATURE['feature'].replace(' ', '') + 'Test'
print(f"   ✅ Generated {class_name}.java ({len(java_code)} characters)")

# Create Traceability Matrix
print("\n6. Creating Traceability Matrix...")
matrix = engine.create_traceability_matrix(YOUR_FEATURE, test_cases)
if "error" not in matrix:
    print(f"   ✅ Matrix created")
    print(f"   • Requirement ID: {matrix['requirement_id']}")
    print(f"   • Test Cases Mapped: {len(matrix['test_case_ids'])}")
    print(f"   • Coverage Ratio: {matrix['coverage']['coverage_ratio']}")
    
    # Field coverage
    print("\n   Field Coverage:")
    for field, tcs in matrix['mapping']['fields_covered'].items():
        print(f"      • {field}: {len(tcs)} test case(s)")
    
    # Edge case coverage
    print("\n   Edge Case Coverage:")
    for edge, tcs in matrix['mapping']['edge_cases_covered'].items():
        print(f"      • {edge}: {len(tcs)} test case(s)")
else:
    print(f"   ❌ Error: {matrix['error']}")

# Calculate Metrics
print("\n7. Calculating Coverage Metrics...")
metrics = engine.calculate_coverage_metrics(YOUR_FEATURE, test_cases)
if "error" not in metrics:
    print(f"   ✅ Metrics calculated")
    print(f"   • Coverage Score:      {metrics['requirement_coverage_score']}")
    print(f"   • Coverage Percentage: {metrics['coverage_percentage']}%")
    print(f"   • Quality Score:       {metrics['quality_score']}/100")
    print(f"   • Total Cases:         {metrics['total_cases']}")
    print(f"   • Automation Ready:    {'✅ Yes' if metrics['is_automation_ready'] else '❌ No'}")
    
    print("\n   Requirements Breakdown:")
    print(f"      • Fields:      {metrics['breakdown']['fields']}")
    print(f"      • Validations: {metrics['breakdown']['validations']}")
    print(f"      • Edge Cases:  {metrics['breakdown']['edge_cases']}")
    print(f"      • Roles:       {metrics['breakdown']['roles']}")
else:
    print(f"   ❌ Error: {metrics['error']}")

# Save Outputs
print("\n8. Saving Outputs...")
try:
    # Create safe filename
    feature_name = YOUR_FEATURE['feature'].replace(' ', '_').lower()
    
    # Save test cases
    tc_filename = f"{feature_name}_test_cases.json"
    with open(tc_filename, 'w') as f:
        json.dump(test_cases, f, indent=2)
    print(f"   ✅ Test cases saved: {tc_filename}")
    
    # Save Java code
    java_filename = f"{class_name}.java"
    with open(java_filename, 'w') as f:
        f.write(java_code)
    print(f"   ✅ Java code saved: {java_filename}")
    
    # Save traceability matrix
    matrix_filename = f"{feature_name}_traceability.json"
    with open(matrix_filename, 'w') as f:
        json.dump(matrix, f, indent=2)
    print(f"   ✅ Traceability saved: {matrix_filename}")
    
    # Save metrics
    metrics_filename = f"{feature_name}_metrics.json"
    with open(metrics_filename, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"   ✅ Metrics saved: {metrics_filename}")
    
except Exception as e:
    print(f"   ⚠️  Save error: {e}")

# Summary
print("\n" + "=" * 80)
print("✅ TEST GENERATION COMPLETE!")
print("=" * 80)

print(f"\n📊 Summary for {YOUR_FEATURE['feature']}:")
print(f"   • Test Cases Generated:    {len(test_cases)}")
print(f"   • Automation Code:         Ready ({len(java_code)} chars)")
print(f"   • Coverage Score:          {metrics.get('requirement_coverage_score', 'N/A')}")
print(f"   • Quality Score:           {metrics.get('quality_score', 'N/A')}/100")

print("\n🎯 Next Steps:")
print("   1. Review the generated test cases")
print("   2. Customize the Selenium code as needed")
print("   3. Run the automation tests")
print("   4. Integrate with CI/CD pipeline")

print("\n💡 Tip: Modify the YOUR_FEATURE dictionary at the top of this file")
print("   to generate tests for different features!")

print("\n" + "=" * 80)
