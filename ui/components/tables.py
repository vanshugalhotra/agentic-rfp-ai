import streamlit as st
import pandas as pd

def render_dataframe(df: pd.DataFrame, title: str = ""):
    if title:
        st.subheader(title)
    st.dataframe(df, use_container_width=True)
