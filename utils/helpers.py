# utils/helpers.py
import pandas as pd
import base64
import streamlit as st

def download_csv(data, filename="data.csv"):
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">📥 Download CSV</a>'
    st.markdown(href, unsafe_allow_html=True)

def format_number(val):
    try:
        return f"₹{val:,.0f}"
    except:
        return val
