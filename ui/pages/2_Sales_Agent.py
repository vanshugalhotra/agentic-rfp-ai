# ui/pages/2_Sales_Agent.py
import streamlit as st
from callbacks import start_sales_agent, retry_url
from components.url_status import render_url_status
from components.timeline import render_timeline

st.header("🧾 Sales Agent")

if not st.session_state.urls:
    st.info("No URLs submitted yet.")
else:
    for url in st.session_state.urls:
        status = st.session_state.url_status[url]

        col1, col2 = st.columns([3, 1])

        with col1:
            render_url_status(url, status)
            render_timeline(status["history"])

        with col2:
            st.button(
                "▶ Start",
                on_click=start_sales_agent,
                args=(url,),
                key=f"start_{url}"
            )
            st.button(
                "🔄 Retry",
                on_click=retry_url,
                args=(url,),
                key=f"retry_{url}"
            )
