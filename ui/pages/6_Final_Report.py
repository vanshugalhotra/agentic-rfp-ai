import streamlit as st
from agents.main_agent.src.resolve.resolver import generate_final_report

st.header("📄 Final RFP Response")

for url, pricing in st.session_state.pricing_results.items():
    if st.button("Generate Final Report", key=f"final_{url}"):
        report = generate_final_report(pricing)
        st.text_area("Final Report", report, height=400)
