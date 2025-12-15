import streamlit as st

from agents.main_agent.src.load_pdf import load_rfp_pdf
from agents.main_agent.src.summary import extract_role_relevant_text

st.header("🧠 Main Agent")

# ---- Guard ----
if "sales_outputs" not in st.session_state or not st.session_state.sales_outputs:
    st.warning("No Sales Agent output available.")
    st.stop()

# ---- Select RFP ----
rfp_urls = list(st.session_state.sales_outputs.keys())
selected_url = st.selectbox("Select RFP", rfp_urls)

rfp_metadata = st.session_state.sales_outputs[selected_url]

st.subheader("RFP Metadata")
st.json(rfp_metadata)

# ---- Generate role-specific summaries ----
if st.button("Generate Role-Specific Summaries"):

    if "rfp_pdf_path" not in rfp_metadata:
        st.error("No RFP PDF path found in Sales Agent output.")
        st.stop()

    with st.spinner("Loading RFP PDF..."):
        pdf_result = load_rfp_pdf(rfp_metadata["rfp_pdf_path"])

    # ---- IMPORTANT FIX ----
    # load_rfp_pdf returns a dict, not a string
    if isinstance(pdf_result, dict):
        full_text = (
            pdf_result.get("text")
            or pdf_result.get("full_text")
            or ""
        )
    else:
        full_text = pdf_result

    if not full_text.strip():
        st.error("Failed to extract text from PDF.")
        st.stop()

    with st.spinner("Extracting role-specific content..."):
        extracted = extract_role_relevant_text(full_text)

    st.session_state.main_agent_output = {
        "technical": "\n".join(extracted["technical_text"]),
        "pricing": "\n".join(extracted["testing_text"]),
    }

# ---- Editable outputs ----
if "main_agent_output" in st.session_state:

    st.subheader("🔧 Technical Agent Context (Editable)")
    technical_text = st.text_area(
        "Technical Summary",
        value=st.session_state.main_agent_output["technical"],
        height=260
    )

    st.subheader("💰 Pricing Agent Context (Editable)")
    pricing_text = st.text_area(
        "Testing & Acceptance Summary",
        value=st.session_state.main_agent_output["pricing"],
        height=260
    )

    if st.button("Approve & Send to Agents"):
        st.session_state.approved_context = {
            "technical": technical_text,
            "pricing": pricing_text
        }

        st.success("Summaries approved and sent to Technical & Pricing Agents ✅")
