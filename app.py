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
        st.success("Processing...")

        st.subheader("Structured Requirement")
        st.json({"placeholder": "JSON will appear here"})

        st.subheader("Generated Test Cases")
        st.write("Test cases will appear here")

        st.subheader("Automation Script")
        st.code("// Selenium script will appear here")

        st.subheader("Coverage Metrics")
        st.write("Coverage metrics will appear here")

with tabs[1]:
    st.header("Requirement Comparison")

    old_req = st.text_area("Old Requirement")
    new_req = st.text_area("New Requirement")

    if st.button("Compare"):
        st.write("Comparison result will appear here")
