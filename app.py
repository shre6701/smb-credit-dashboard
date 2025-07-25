import streamlit as st
from data_loader import load_data
from preprocess import preprocess_data, aggregate_risk
from risk_model import run_risk_model
from visual import (
    show_kpis, show_trendline, show_aging_chart, show_correlation_heatmap,
    show_risk_distribution, show_avg_factors_by_risk, show_high_risk_table,
    show_credit_score_table, show_facet_scatter
)

st.set_page_config(page_title="Credit Risk Dashboard", layout="wide")
st.title("📊 SMB Credit Risk Dashboard")

uploaded_file = st.sidebar.file_uploader("📅 Upload Excel or CSV", type=["xlsx", "csv"])
if uploaded_file is None:
    st.warning("Upload a file to continue.")
    st.stop()

# Load & filter data
df = load_data(uploaded_file)
if df.empty:
    st.stop()

st.sidebar.header("🔍 Filters")
if 'Category' in df.columns:
    selected = st.sidebar.multiselect("Category", df['Category'].unique(), default=df['Category'].unique())
    df = df[df['Category'].isin(selected)]
if 'Region' in df.columns:
    selected = st.sidebar.multiselect("Region", df['Region'].unique(), default=df['Region'].unique())
    df = df[df['Region'].isin(selected)]

# Preprocess
df = preprocess_data(df)
unpaid_df = df[df['Payment Status'] == 'unpaid']

# KPI section
show_kpis(df, unpaid_df)
show_trendline(unpaid_df)
show_aging_chart(unpaid_df)

# Aggregate & model
risk = aggregate_risk(df)
model_results = run_risk_model(risk)

# Visuals
show_credit_score_table(risk)
col1, col2 = st.columns(2)
with col1:
    show_correlation_heatmap(risk)
with col2:
    show_risk_distribution(risk)
show_facet_scatter(risk)
show_avg_factors_by_risk(risk)
thresh = st.slider("Credit Score Threshold", 0, 100, 60)
show_high_risk_table(risk, thresh)

# Export
st.sidebar.download_button("Download Risk Data", data=risk.to_csv(index=False).encode(), file_name="credit_risk.csv")
