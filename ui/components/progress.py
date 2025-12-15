import streamlit as st

def show_spinner(message: str):
    return st.spinner(message)

def show_progress(percent: int):
    st.progress(percent)
