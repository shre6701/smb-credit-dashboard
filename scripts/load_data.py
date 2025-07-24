import pandas as pd
import streamlit as st

@st.cache_data
def load_data(path):
    try:
        if path.name.endswith('.csv'):
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path)

        df['Invoice Date'] = pd.to_datetime(df['Invoice Date'], errors='coerce')
        df['Due Date'] = pd.to_datetime(df['Due Date'], errors='coerce')
        return df.dropna(subset=['Invoice Date', 'Due Date'])
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return pd.DataFrame()
