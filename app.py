import streamlit as st

st.title("AI Requirement to Test Generator")

requirement = st.text_area("Enter Requirement")

if st.button("Generate"):
    st.write("Processing...")
