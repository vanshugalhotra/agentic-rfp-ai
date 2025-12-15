import streamlit as st

def render_url_status(url: str, status: dict):
    st.markdown(f"""
    <div class="status-card">
        <b>{url}</b><br>
        <span class="stage">Stage:</span> {status.get("stage")}
    </div>
    """, unsafe_allow_html=True)

    if "error" in status:
        st.error(status["error"])
