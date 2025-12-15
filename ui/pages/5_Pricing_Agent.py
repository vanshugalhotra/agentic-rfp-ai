import streamlit as st
from agents.pricing_agent.pipeline import run_pricing

st.header("💰 Pricing Agent")

for url, tech_data in st.session_state.tech_results.items():
    if st.button("Compute Pricing", key=f"price_{url}"):
        pricing = run_pricing(tech_data)
        st.session_state.pricing_results[url] = pricing

    if url in st.session_state.pricing_results:
        st.dataframe(st.session_state.pricing_results[url]["final_table"])
        st.download_button(
            "Download Pricing CSV",
            st.session_state.pricing_results[url]["csv"],
            file_name="pricing.csv"
        )
