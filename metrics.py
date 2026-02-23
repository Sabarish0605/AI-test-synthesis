def calculate_coverage(structured_data, test_cases):
    fields = structured_data.get("functional_fields", structured_data.get("fields", []))
    total_fields = len(fields)
    total_tests = len(test_cases)

    # Basic coverage logic: assume 2 tests per field for good coverage
    coverage_ratio = (total_tests / (total_fields * 2)) if total_fields > 0 else 0.0
    coverage_percentage = min(100.0, coverage_ratio * 100.0)

    return {
        "Total Fields": total_fields,
        "Total Test Cases": total_tests,
        "Requirement Coverage (%)": round(float(coverage_percentage), 2)
    }


