import streamlit as st

def load_css():
    st.markdown("""
    <style>
    .status-card {
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        border: 1px solid #ddd;
        background-color: #fafafa;
    }
    .stage {
        font-weight: 600;
        color: #2e7d32;
    }
    </style>
    """, unsafe_allow_html=True)
