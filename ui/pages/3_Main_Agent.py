import streamlit as st
from agents.main_agent.main_agent import run_main_draft

st.set_page_config(page_title="Main Agent", layout="wide")
st.title("🧠 Main Agent")

# -------------------------------------------------
# GUARD: Sales Agent must have delivered an RFP
# -------------------------------------------------
if "results" not in st.session_state or not st.session_state.results:
    st.info("No Sales Agent output available yet.")
    st.stop()

rfp = st.session_state.results.get("selected_rfp")

if not rfp:
    st.warning("Sales Agent did not select any eligible RFP.")
    st.stop()

# -------------------------------------------------
# RFP METADATA
# -------------------------------------------------
st.subheader("📄 Selected RFP")
st.json({
    "Tender Reference": rfp.get("tender_reference"),
    "Source URL": rfp.get("source_url"),
    "Submission Due Date": rfp.get("submission_due_date"),
})

# -------------------------------------------------
# RUN MAIN AGENT (DRAFT ONLY)
# -------------------------------------------------
if "main_draft" not in st.session_state:
    if st.button("🧠 Generate Main Agent Draft"):
        with st.spinner("Analyzing RFP and preparing technical context..."):
            st.session_state.main_draft = run_main_draft(rfp)

# -------------------------------------------------
# EDITABLE TECHNICAL OUTPUT
# -------------------------------------------------
if "main_draft" in st.session_state:
    draft = st.session_state.main_draft

    st.divider()
    st.subheader("✍️ Technical Summary (Editable)")

    technical_summary = st.text_area(
        "🔧 Technical Context for Technical Agent",
        value=draft.get("technical_summary", ""),
        height=320
    )

    # -------------------------------------------------
    # APPROVAL: SEND ONLY TO TECHNICAL AGENT
    # -------------------------------------------------
    if st.button("➡️ Send to Technical Agent"):
        st.session_state.main_to_technical = {
            **draft,
            "technical_summary": technical_summary
        }

        st.success(
            "Technical context approved and sent to Technical Agent ✅\n\n"
            "Proceed to the Technical Agent page."
        )
