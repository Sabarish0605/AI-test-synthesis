def calculate_coverage(structured_data, test_cases):
    total_fields = len(structured_data.get("fields", []))
    total_tests = len(test_cases)

    coverage_percentage = min(100, total_tests * 20)

    return {
        "Total Fields": total_fields,
        "Total Test Cases": total_tests,
        "Requirement Coverage (%)": coverage_percentage
    }
