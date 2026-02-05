import streamlit as st

def header(title):
    st.markdown(f"## {title}")

def kpi_card(label, value):
    st.metric(label, value)
