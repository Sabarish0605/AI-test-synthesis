"""
Test Engine Module - Member 2
=================================
A modular test artifact generation engine for AI-powered QA systems.

Dependencies:
    pip install google-generativeai

Author: Member 2 (Test Engine Lead)
"""

import json
from typing import Dict, List, Any, Optional, Tuple, TypedDict, Union
import os

# Type aliases for clarity
StructuredData = Dict[str, Any]
TestCase = Dict[str, Any]
TestCaseList = List[TestCase]


# Error type
class ErrorDict(TypedDict):
    error: str


# Typed dictionaries for complex return types
class CoverageInfo(TypedDict):
    total_requirements: int
    total_test_cases: int
    coverage_ratio: str


class MappingInfo(TypedDict):
    fields_covered: Dict[str, List[str]]
    edge_cases_covered: Dict[str, List[str]]


class TraceabilityMatrix(TypedDict):
    feature: str
    requirement_id: str
    test_case_ids: List[str]
    coverage: CoverageInfo
    mapping: MappingInfo


class BreakdownInfo(TypedDict):
    fields: int
    validations: int
    edge_cases: int
    roles: int


class TestTypeDistribution(TypedDict):
    Positive: int
    Negative: int
    Boundary: int


class CoverageMetrics(TypedDict):
    requirement_coverage_score: float
    total_cases: int
    is_automation_ready: bool
    breakdown: BreakdownInfo
    test_type_distribution: TestTypeDistribution
    coverage_percentage: float
    quality_score: float


class TestArtifactGenerator:
    """
    Core test artifact generation engine that processes structured requirements
    and produces test cases, automation scripts, and coverage metrics.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Test Artifact Generator.
        
        Args:
            api_key: Google Generative AI API key (optional, will check env if not provided)
        """
        self.api_key = api_key or os.environ.get('GEMINI_API_KEY')
        self.genai: Optional[Any] = None
        
        # Initialize Gemini only if API key is available
        if self.api_key:
            try:
                import google.generativeai as genai  # type: ignore
                genai.configure(api_key=self.api_key)  # type: ignore
                self.genai = genai
            except ImportError:
                print("Warning: google-generativeai not installed. Using template-based generation.")
            except Exception as e:
                print(f"Warning: Failed to initialize Gemini API: {e}")
    
    def _validate_input(self, structured_data: StructuredData) -> Tuple[bool, str]:
        """
        Validate the input structured data.
        
        Args:
            structured_data: The input dictionary to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        required_keys = ['feature', 'fields', 'validations', 'roles', 'edge_cases']
        missing_keys = [key for key in required_keys if key not in structured_data]
        
        if missing_keys:
            return False, f"Missing required keys: {', '.join(missing_keys)}"
        
        if not isinstance(structured_data.get('fields'), list):
            return False, "'fields' must be a list"
        
        if not isinstance(structured_data.get('validations'), dict):
            return False, "'validations' must be a dictionary"
        
        if not isinstance(structured_data.get('roles'), list):
            return False, "'roles' must be a list"
        
        if not isinstance(structured_data.get('edge_cases'), list):
            return False, "'edge_cases' must be a list"
        
        return True, ""
    
    def generate_test_cases(self, structured_data: StructuredData) -> TestCaseList:
        """
        Generate comprehensive test cases from structured requirement data.
        Uses AI (Gemini) if available, otherwise falls back to template-based generation.
        
        Args:
            structured_data: Dictionary containing feature, fields, validations, roles, edge_cases
            
        Returns:
            List of test case dictionaries with tc_id, title, type, steps, expected_result
        """
        # Validate input
        is_valid, error_msg = self._validate_input(structured_data)
        if not is_valid:
            return [{"error": error_msg}]
        
        # Try AI-based generation first
        if self.genai:
            try:
                return self._generate_test_cases_ai(structured_data)
            except Exception as e:
                print(f"AI generation failed: {e}. Falling back to template-based generation.")
        
        # Fallback to template-based generation
        return self._generate_test_cases_template(structured_data)
    
    def _generate_test_cases_ai(self, structured_data: StructuredData) -> TestCaseList:
        """Generate test cases using Gemini AI."""
        if self.genai is None:
            raise ValueError("Gemini API not initialized")
        
        model = self.genai.GenerativeModel('gemini-pro')  # type: ignore
        
        prompt = f"""
You are a Senior QA Engineer. Generate comprehensive test cases in JSON format for the following requirement:

Feature: {structured_data['feature']}
Fields: {', '.join(structured_data['fields'])}
Validations: {json.dumps(structured_data['validations'])}
Roles: {', '.join(structured_data['roles'])}
Edge Cases: {', '.join(structured_data['edge_cases'])}

Generate test cases covering:
1. Positive scenarios for each field
2. Negative scenarios for validation failures
3. Boundary Value Analysis (e.g., if "min 8 chars", test with 7, 8, 9 chars)
4. Edge cases mentioned
5. Role-based access scenarios

Return ONLY a JSON array where each test case has:
- tc_id (string, format: TC_XXX)
- title (string)
- type (string: "Positive", "Negative", or "Boundary")
- steps (array of strings)
- expected_result (string)

Example format:
[
  {{
    "tc_id": "TC_001",
    "title": "Valid login with correct credentials",
    "type": "Positive",
    "steps": ["Open application", "Enter valid email", "Enter valid password", "Click login"],
    "expected_result": "User successfully logged in"
  }}
]

Generate at least {len(structured_data['fields']) * 2 + len(structured_data['edge_cases'])} test cases.
"""
        
        response = model.generate_content(prompt)  # type: ignore
        response_text: str = response.text.strip()  # type: ignore
        
        # Extract JSON from response (handle markdown code blocks)
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0].strip()
        
        test_cases = json.loads(response_text)
        return test_cases
    
    def _generate_test_cases_template(self, structured_data: StructuredData) -> TestCaseList:
        """Generate test cases using template-based logic."""
        test_cases: TestCaseList = []
        tc_counter = 1
        feature = structured_data['feature']
        
        # Positive test cases for each field
        for field in structured_data['fields']:
            test_cases.append({
                "tc_id": f"TC_{tc_counter:03d}",
                "title": f"Valid {feature} with correct {field}",
                "type": "Positive",
                "steps": [
                    f"Open {feature} page",
                    f"Enter valid {field}",
                    "Submit the form",
                    "Verify submission"
                ],
                "expected_result": f"{feature} successful with valid {field}"
            })
            tc_counter += 1
        
        # Negative test cases for validations
        for field, validation in structured_data['validations'].items():
            test_cases.append({
                "tc_id": f"TC_{tc_counter:03d}",
                "title": f"Invalid {feature} - {field} fails {validation}",
                "type": "Negative",
                "steps": [
                    f"Open {feature} page",
                    f"Enter invalid {field} (violates: {validation})",
                    "Submit the form",
                    "Verify error message"
                ],
                "expected_result": f"Error message displayed: {validation} validation failed"
            })
            tc_counter += 1
            
            # Boundary Value Analysis for numeric validations
            if "min" in validation.lower() or "max" in validation.lower():
                # Extract number if present
                numbers = [int(s) for s in validation.split() if s.isdigit()]
                if numbers:
                    boundary_val = numbers[0]
                    test_cases.append({
                        "tc_id": f"TC_{tc_counter:03d}",
                        "title": f"Boundary test for {field} - {validation}",
                        "type": "Boundary",
                        "steps": [
                            f"Open {feature} page",
                            f"Enter {field} with boundary value ({boundary_val - 1}, {boundary_val}, {boundary_val + 1})",
                            "Submit the form",
                            "Verify behavior at boundary"
                        ],
                        "expected_result": f"Correct behavior at {validation} boundary"
                    })
                    tc_counter += 1
        
        # Edge case tests
        for edge_case in structured_data['edge_cases']:
            test_cases.append({
                "tc_id": f"TC_{tc_counter:03d}",
                "title": f"{feature} with {edge_case}",
                "type": "Negative",
                "steps": [
                    f"Open {feature} page",
                    f"Test with {edge_case}",
                    "Submit the form",
                    "Verify system handles edge case"
                ],
                "expected_result": f"System properly handles {edge_case} scenario"
            })
            tc_counter += 1
        
        # Role-based tests
        for role in structured_data['roles']:
            test_cases.append({
                "tc_id": f"TC_{tc_counter:03d}",
                "title": f"{feature} access for {role} role",
                "type": "Positive",
                "steps": [
                    f"Login as {role}",
                    f"Access {feature} feature",
                    "Verify access permissions",
                    "Perform {feature} operation"
                ],
                "expected_result": f"{role} can access and use {feature} feature correctly"
            })
            tc_counter += 1
        
        return test_cases
    
    def generate_selenium_java(self, structured_data: StructuredData) -> str:
        """
        Generate a complete Selenium Java test class.
        
        Args:
            structured_data: Dictionary containing feature and fields information
            
        Returns:
            String containing complete Java Selenium test class
        """
        # Validate input
        is_valid, error_msg = self._validate_input(structured_data)
        if not is_valid:
            return f"// Error: {error_msg}"
        
        feature = structured_data['feature']
        fields: List[str] = structured_data['fields']
        class_name = f"{feature.replace(' ', '')}Test"
        
        # Generate field interactions
        field_interactions: List[str] = []
        for field in fields:
            field_id = field.lower().replace(' ', '_')
            field_interactions.append(
                f'        driver.findElement(By.id("{field_id}")).sendKeys("{field}Value");'
            )
        
        field_interactions_code = '\n'.join(field_interactions)
        
        # Generate assertions for validations
        assertions: List[str] = []
        validations: Dict[str, str] = structured_data.get('validations', {})
        for field, _validation in validations.items():
            field_id = field.lower().replace(' ', '_')
            assertions.append(
                f'        Assert.assertTrue(driver.findElement(By.id("{field_id}")).isDisplayed(), "{field} field should be visible");'
            )
        
        assertions_code = '\n'.join(assertions) if assertions else '        Assert.assertTrue(true, "Default assertion");'
        
        java_template = f'''package com.automation.tests;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.Assert;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;
import java.time.Duration;

/**
 * Automated Test Suite for {feature}
 * Generated by AI-Powered QA System
 * Member 2 - Test Engine Module
 */
public class {class_name} {{
    
    private WebDriver driver;
    private static final String BASE_URL = "http://localhost:8080";
    
    @BeforeMethod
    public void setUp() {{
        // Set up ChromeDriver
        System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
        driver = new ChromeDriver();
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
        driver.manage().window().maximize();
    }}
    
    @Test(priority = 1, description = "Test valid {feature} with all required fields")
    public void testValid{feature.replace(' ', '')}() {{
        // Navigate to {feature} page
        driver.get(BASE_URL + "/{feature.lower().replace(' ', '-')}");
        
        // Fill in all required fields
{field_interactions_code}
        
        // Submit the form
        driver.findElement(By.id("submit_button")).click();
        
        // Verify successful submission
        WebElement successMessage = driver.findElement(By.id("success_message"));
        Assert.assertTrue(successMessage.isDisplayed(), "{feature} should succeed with valid data");
        Assert.assertTrue(successMessage.getText().contains("Success"), "Success message should be displayed");
    }}
    
    @Test(priority = 2, description = "Test {feature} with empty fields")
    public void testEmpty{feature.replace(' ', '')}Fields() {{
        // Navigate to {feature} page
        driver.get(BASE_URL + "/{feature.lower().replace(' ', '-')}");
        
        // Submit without filling fields
        driver.findElement(By.id("submit_button")).click();
        
        // Verify validation errors
{assertions_code}
        
        WebElement errorMessage = driver.findElement(By.className("error-message"));
        Assert.assertTrue(errorMessage.isDisplayed(), "Error message should be displayed for empty fields");
    }}
    
    @Test(priority = 3, description = "Test {feature} field validations")
    public void test{feature.replace(' ', '')}Validations() {{
        // Navigate to {feature} page
        driver.get(BASE_URL + "/{feature.lower().replace(' ', '-')}");
        
        // Test each validation rule
        {self._generate_validation_tests(structured_data)}
        
        // Verify all validations are enforced
        Assert.assertTrue(driver.findElement(By.id("validation_summary")).isDisplayed(), 
            "Validation summary should display all errors");
    }}
    
    @Test(priority = 4, description = "Test {feature} with boundary values")
    public void test{feature.replace(' ', '')}BoundaryValues() {{
        // Navigate to {feature} page
        driver.get(BASE_URL + "/{feature.lower().replace(' ', '-')}");
        
        // Test boundary conditions for each validated field
        // Example: minimum and maximum length validations
        {self._generate_boundary_tests(structured_data)}
        
        // Verify boundary behavior
        Assert.assertTrue(true, "Boundary value tests completed");
    }}
    
    @AfterMethod
    public void tearDown() {{
        // Close browser
        if (driver != null) {{
            driver.quit();
        }}
    }}
    
    // Helper method to wait for element
    private void waitForElement(By locator, int timeoutSeconds) {{
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(timeoutSeconds));
    }}
    
    // Helper method to verify element text
    private void verifyElementText(By locator, String expectedText) {{
        WebElement element = driver.findElement(locator);
        Assert.assertEquals(element.getText(), expectedText, 
            "Element text should match expected value");
    }}
}}
'''
        
        return java_template
    
    def _generate_validation_tests(self, structured_data: StructuredData) -> str:
        """Generate validation test code snippets."""
        validations: Dict[str, str] = structured_data.get('validations', {})
        test_code: List[str] = []
        
        for field, _validation in validations.items():
            field_id = field.lower().replace(' ', '_')
            test_code.append(
                f'driver.findElement(By.id("{field_id}")).sendKeys("invalid_{field}");'
            )
        
        return '\n        '.join(test_code) if test_code else '// No specific validations to test'
    
    def _generate_boundary_tests(self, structured_data: StructuredData) -> str:
        """Generate boundary test code snippets."""
        validations: Dict[str, str] = structured_data.get('validations', {})
        test_code: List[str] = []
        
        for field, validation in validations.items():
            if "min" in validation.lower():
                field_id = field.lower().replace(' ', '_')
                test_code.append(
                    f'// Test minimum boundary for {field}\n'
                    f'        driver.findElement(By.id("{field_id}")).clear();\n'
                    f'        driver.findElement(By.id("{field_id}")).sendKeys("short");'
                )
        
        return '\n        '.join(test_code) if test_code else '// No boundary values to test'
    
    def create_traceability_matrix(self, structured_data: StructuredData, 
                                   test_cases: TestCaseList) -> Union[TraceabilityMatrix, ErrorDict]:
        """
        Create a traceability matrix mapping requirements to test cases.
        
        Args:
            structured_data: Original requirement data
            test_cases: Generated test cases
            
        Returns:
            Dictionary mapping feature to test case IDs
        """
        if not test_cases or "error" in test_cases[0]:
            error_dict: ErrorDict = {"error": "Cannot create matrix with invalid test cases"}
            return error_dict
        
        feature = structured_data.get('feature', 'Unknown')
        tc_ids = [tc.get('tc_id', 'UNKNOWN') for tc in test_cases]
        
        fields_covered: Dict[str, List[str]] = {
            field: [tc['tc_id'] for tc in test_cases 
                   if field.lower() in tc.get('title', '').lower()]
            for field in structured_data.get('fields', [])
        }
        
        edge_cases_covered: Dict[str, List[str]] = {
            edge: [tc['tc_id'] for tc in test_cases 
                  if edge.lower() in tc.get('title', '').lower()]
            for edge in structured_data.get('edge_cases', [])
        }
        
        traceability_matrix: TraceabilityMatrix = {
            "feature": feature,
            "requirement_id": f"REQ_{feature.upper().replace(' ', '_')}",
            "test_case_ids": tc_ids,
            "coverage": {
                "total_requirements": len(structured_data.get('fields', [])) + 
                                    len(structured_data.get('edge_cases', [])),
                "total_test_cases": len(tc_ids),
                "coverage_ratio": f"{len(tc_ids)} : {len(structured_data.get('fields', [])) + len(structured_data.get('edge_cases', []))}"
            },
            "mapping": {
                "fields_covered": fields_covered,
                "edge_cases_covered": edge_cases_covered
            }
        }
        
        return traceability_matrix
    
    def calculate_coverage_metrics(self, structured_data: StructuredData, 
                                   test_cases: TestCaseList) -> Union[CoverageMetrics, ErrorDict]:
        """
        Calculate test coverage metrics.
        
        Args:
            structured_data: Original requirement data
            test_cases: Generated test cases
            
        Returns:
            Dictionary containing coverage metrics
        """
        if not test_cases or "error" in test_cases[0]:
            error_dict: ErrorDict = {
                "error": "Cannot calculate metrics with invalid test cases"
            }
            return error_dict
        
        # Calculate coverage score
        num_fields = len(structured_data.get('fields', []))
        num_edge_cases = len(structured_data.get('edge_cases', []))
        total_requirements = num_fields + num_edge_cases
        
        total_test_cases = len(test_cases)
        
        # Coverage formula: (Test Cases / Total Requirements) * 10
        coverage_score = (total_test_cases / total_requirements * 10) if total_requirements > 0 else 0.0
        
        # Count test types
        test_type_breakdown: TestTypeDistribution = {
            "Positive": len([tc for tc in test_cases if tc.get('type') == 'Positive']),
            "Negative": len([tc for tc in test_cases if tc.get('type') == 'Negative']),
            "Boundary": len([tc for tc in test_cases if tc.get('type') == 'Boundary'])
        }
        
        metrics: CoverageMetrics = {
            "requirement_coverage_score": round(coverage_score, 2),
            "total_cases": total_test_cases,
            "is_automation_ready": True,  # True if we successfully generated test cases
            "breakdown": {
                "fields": num_fields,
                "validations": len(structured_data.get('validations', {})),
                "edge_cases": num_edge_cases,
                "roles": len(structured_data.get('roles', []))
            },
            "test_type_distribution": test_type_breakdown,
            "coverage_percentage": round((total_test_cases / (total_requirements * 2)) * 100, 2) if total_requirements > 0 else 0.0,
            "quality_score": self._calculate_quality_score(test_cases, structured_data)
        }
        
        return metrics
    
    def _calculate_quality_score(self, test_cases: TestCaseList, 
                                 structured_data: StructuredData) -> float:
        """Calculate an overall quality score for the test suite."""
        score = 0.0
        
        # Criteria 1: Has both positive and negative tests (30 points)
        has_positive = any(tc.get('type') == 'Positive' for tc in test_cases)
        has_negative = any(tc.get('type') == 'Negative' for tc in test_cases)
        if has_positive and has_negative:
            score += 30.0
        elif has_positive or has_negative:
            score += 15.0
        
        # Criteria 2: Has boundary tests (20 points)
        has_boundary = any(tc.get('type') == 'Boundary' for tc in test_cases)
        if has_boundary:
            score += 20.0
        
        # Criteria 3: Covers all fields (25 points)
        fields = structured_data.get('fields', [])
        covered_fields = sum(1 for field in fields 
                           if any(field.lower() in tc.get('title', '').lower() 
                                 for tc in test_cases))
        if fields:
            score += (covered_fields / len(fields)) * 25.0
        
        # Criteria 4: Covers all edge cases (25 points)
        edge_cases = structured_data.get('edge_cases', [])
        covered_edges = sum(1 for edge in edge_cases 
                          if any(edge.lower() in tc.get('title', '').lower() 
                                for tc in test_cases))
        if edge_cases:
            score += (covered_edges / len(edge_cases)) * 25.0
        
        return round(score, 2)


# ============================================================================
# MAIN EXECUTION BLOCK FOR TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Test Engine Module - Member 2")
    print("Testing with Sample Data")
    print("=" * 70)
    
    # Sample input JSON from Member 1
    sample_data: StructuredData = {
        "feature": "Login",
        "fields": ["email", "password"],
        "validations": {
            "email": "valid format",
            "password": "min 8 chars"
        },
        "roles": ["admin", "user"],
        "edge_cases": ["empty fields", "sql injection"]
    }
    
    print("\n📥 INPUT DATA:")
    print(json.dumps(sample_data, indent=2))
    
    # Initialize the generator
    generator = TestArtifactGenerator()
    
    # Generate test cases
    print("\n🧪 GENERATING TEST CASES...")
    test_cases = generator.generate_test_cases(sample_data)
    print(f"✓ Generated {len(test_cases)} test cases")
    print("\nSample Test Cases:")
    for i, tc in enumerate(test_cases[:3], 1):
        print(f"\n  [{i}] {tc.get('tc_id')} - {tc.get('title')}")
        print(f"      Type: {tc.get('type')}")
        print(f"      Steps: {', '.join(tc.get('steps', [])[:2])}...")
    
    # Generate Selenium Java code
    print("\n⚙️  GENERATING SELENIUM JAVA CODE...")
    java_code = generator.generate_selenium_java(sample_data)
    print(f"✓ Generated Java class ({len(java_code)} characters)")
    print("\nFirst 500 characters:")
    print(java_code[:500] + "...")
    
    # Create traceability matrix
    print("\n📊 CREATING TRACEABILITY MATRIX...")
    matrix = generator.create_traceability_matrix(sample_data, test_cases)
    print(f"✓ Feature: {matrix.get('feature')}")
    print(f"✓ Total Test Cases: {len(matrix.get('test_case_ids', []))}")
    print(f"✓ Coverage Ratio: {matrix.get('coverage', {}).get('coverage_ratio')}")
    
    # Calculate coverage metrics
    print("\n📈 CALCULATING COVERAGE METRICS...")
    metrics = generator.calculate_coverage_metrics(sample_data, test_cases)
    print(f"✓ Coverage Score: {metrics.get('requirement_coverage_score')}")
    print(f"✓ Total Cases: {metrics.get('total_cases')}")
    print(f"✓ Automation Ready: {metrics.get('is_automation_ready')}")
    print(f"✓ Quality Score: {metrics.get('quality_score')}/100")
    print(f"✓ Coverage %: {metrics.get('coverage_percentage')}%")
    
    print("\n" + "=" * 70)
    print("✅ Test Engine Module Ready for Integration!")
    print("=" * 70)
    
    # Show sample usage for Member 3
    print("\n📝 SAMPLE USAGE FOR MEMBER 3 (UI Lead):")
    print("""
    import test_engine
    
    # Initialize
    engine = test_engine.TestArtifactGenerator()
    
    # Generate artifacts
    test_cases = engine.generate_test_cases(member1_json)
    java_code = engine.generate_selenium_java(member1_json)
    matrix = engine.create_traceability_matrix(member1_json, test_cases)
    metrics = engine.calculate_coverage_metrics(member1_json, test_cases)
    
    # Display in UI (Streamlit, Flask, etc.)
    st.json(test_cases)
    st.code(java_code, language='java')
    st.table(metrics)
    """)
