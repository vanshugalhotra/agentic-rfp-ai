import streamlit as st
from datetime import datetime


def render_timeline(history):
    """
    history = List[Tuple[str, float]]
    """
    if not history:
        st.caption("No activity yet")
        return

    st.markdown("**Timeline**")

    for stage, ts in history:
        try:
            time_str = datetime.fromtimestamp(float(ts)).strftime("%H:%M:%S")
        except Exception:
            time_str = "—"

        st.write(f"• `{time_str}` — {stage}")
