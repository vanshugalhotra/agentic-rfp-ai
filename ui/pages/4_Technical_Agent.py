import streamlit as st
from agents.technical_agent.pipeline import run_technical_match

st.header("🧪 Technical Agent")

product_file = st.file_uploader("Upload Product Catalog (CSV)", type=["csv"])

for url, summary in st.session_state.main_summary.items():
    st.subheader(f"RFP: {url}")

    if st.button("Run Technical Matching", key=f"tech_{url}"):
        result = run_technical_match(summary["technical"], product_file)
        st.session_state.tech_results[url] = result

    if url in st.session_state.tech_results:
        st.dataframe(st.session_state.tech_results[url]["comparison_table"])
