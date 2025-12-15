import streamlit as st

def editable_summary(title: str, value: str, key: str):
    with st.expander(title, expanded=True):
        return st.text_area(
            label="",
            value=value,
            height=200,
            key=key
        )
