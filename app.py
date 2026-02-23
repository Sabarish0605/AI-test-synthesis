from requirement_engine import extract_requirement, compare_requirements
from test_engine import generate_test_cases, generate_selenium_script
from metrics import calculate_coverage
import streamlit as st

st.set_page_config(page_title="AI Requirement to Test Generator")

st.title("AI Requirement to Test Generator")

tabs = st.tabs(["Generate Tests", "Compare Requirements"])

with tabs[0]:
    st.header("Requirement Input")
    requirement = st.text_area("Enter Requirement")

    if st.button("Generate"):
        if requirement:
            with st.spinner("Analyzing requirement..."):
                # Phase 1: Requirement Understanding
                structured_data = extract_requirement(requirement)
                st.subheader("PHASE 1 — REQUIREMENT UNDERSTANDING")
                st.json(structured_data)

                # Map names for test_engine compatibility
                test_engine_data = {
                    "feature": structured_data.get("feature_name", "Unknown"),
                    "functional_fields": structured_data.get("functional_fields", []),
                    "validations": structured_data.get("validations", {}),
                    "roles": structured_data.get("actors", []),
                    "edge_cases": structured_data.get("edge_cases", []),
                    "risk_analysis": structured_data.get("risk_analysis", {})
                }

                # Phase 2: Test Case Generation
                with st.spinner("Generating test cases..."):
                    test_cases = generate_test_cases(test_engine_data)
                    st.subheader("PHASE 2 — INTELLIGENT TEST CASE GENERATION")
                    st.json(test_cases)

                # Phase 3: Automation Script Generation
                with st.spinner("Generating automation script..."):
                    from test_engine import TestArtifactGenerator
                    engine = TestArtifactGenerator()
                    selenium_script = engine.generate_selenium_java(test_engine_data)
                    st.subheader("PHASE 3 — AUTOMATION SCRIPT GENERATION")
                    st.code(selenium_script, language="java")

                # Phase 4: Traceability Map
                st.subheader("PHASE 4 — TRACEABILITY MAP")
                traceability = engine.create_traceability_matrix(test_engine_data, test_cases)
                st.json(traceability)


                # Coverage Metrics
                st.subheader("Coverage Metrics")
                metrics = calculate_coverage(structured_data, test_cases)
                st.write(metrics)
        else:
            st.warning("Please enter a requirement.")

with tabs[1]:
    st.header("Requirement Comparison")

    old_req = st.text_area("Old Requirement")
    new_req = st.text_area("New Requirement")

    if st.button("Compare"):
        if old_req and new_req:
            with st.spinner("Comparing requirements..."):
                diff = compare_requirements(old_req, new_req)
                st.subheader("PHASE 5 — REQUIREMENT CHANGE DETECTION (CRITICAL)")
                st.json(diff)
        else:
            st.warning("Please enter both old and new requirements.")
