# --- dashboard/dashboard_app.py ---
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
from scripts.load_data import load_data
from scripts.feature_pipeline import preprocess_data, aggregate_risk
from scripts.anomaly_detection import apply_modeling
from utils.helpers import (
    background_color_risk,
    show_correlation_heatmap,
    show_risk_distribution,
    show_avg_factors_by_risk,
    show_high_risk_table
)

# --- MAIN DASHBOARD ---
def main():
    st.set_page_config(page_title="Credit Risk Dashboard", layout="wide")
    st.title("📊 SMB Credit Risk Dashboard")

    uploaded_file = st.sidebar.file_uploader("📥 Upload Excel or CSV", type=["xlsx", "csv"])
    if uploaded_file is None:
        st.warning("Upload a file to continue.")
        return

    df = load_data(uploaded_file)
    if df.empty:
        return

    st.sidebar.header("🔍 Filters")
    if 'Category' in df.columns:
        category_filter = st.sidebar.multiselect("Category", df['Category'].unique(), default=df['Category'].unique())
        df = df[df['Category'].isin(category_filter)]
    if 'Region' in df.columns:
        region_filter = st.sidebar.multiselect("Region", df['Region'].unique(), default=df['Region'].unique())
        df = df[df['Region'].isin(region_filter)]

    df = preprocess_data(df)
    unpaid_df = df[df['Payment Status'] == 'unpaid']

    st.subheader("📌 Key Metrics")
    total_invoices = len(df)
    unpaid_amount = unpaid_df['Amount'].sum()
    overdue_pct = (unpaid_amount / df['Amount'].sum()) * 100 if df['Amount'].sum() else 0
    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total Invoices", f"{total_invoices}")
    col2.metric("💰 Unpaid Amount", f"₹{unpaid_amount:,.2f}")
    col3.metric("⚠️ % Invoices Overdue", f"{overdue_pct:.2f}%")

    st.subheader("📈 Overdue Trendline")
    trend = unpaid_df.groupby('Month')['Amount'].sum().sort_index()
    st.line_chart(trend)

    st.subheader("🧾 Invoice Aging")
    aging = unpaid_df.groupby('Aging Bucket')['Amount'].sum()
    st.bar_chart(aging)

    risk = aggregate_risk(df)

    st.subheader("🔢 Credit Score Table")
    st.dataframe(risk[['OverdueDays', 'Amount', 'Unpaid Ratio', 'Credit Score', 'RiskLabel']], use_container_width=True)

    risk = apply_modeling(risk)

    st.subheader("📌 Credit Score Visuals")
    col1, col2 = st.columns(2)
    with col1:
        show_correlation_heatmap(risk)
    with col2:
        show_risk_distribution(risk)

    st.subheader("📉 Credit Score vs Overdue Days (Faceted Scatter)")
    st.sidebar.markdown("### 🎯 Scatter Plot Filters")
    selected_risk_levels = st.sidebar.multiselect(
        "Select Risk Levels",
        options=risk['RiskLabel'].unique(),
        default=risk['RiskLabel'].unique()
    )

    scatter_data = risk[risk['RiskLabel'].isin(selected_risk_levels)]

    if not scatter_data.empty:
        fig_facet = px.scatter(
            scatter_data,
            x="OverdueDays",
            y="Credit Score",
            size="Amount",
            color="RiskLabel",
            facet_col="RiskLabel",
            hover_name=scatter_data.index,
            hover_data={
                "OverdueDays": True,
                "Credit Score": True,
                "Amount": ":,.0f",
                "Unpaid Ratio": ":.2f",
                "RiskLabel": True
            },
            opacity=0.7,
            title="Credit Score vs Overdue Days by Risk Level",
            height=500
        )
        st.plotly_chart(fig_facet, use_container_width=True)
    else:
        st.info("No data to show based on selected risk filters.")

    st.subheader("🔥 Avg Score Factors by Risk Level")
    show_avg_factors_by_risk(risk)

    st.subheader("⚠️ High Risk Table")
    threshold = st.slider("Credit Score Threshold", 0, 100, 60)
    show_high_risk_table(risk, threshold)

    st.sidebar.download_button("📥 Download Risk Data", data=risk.to_csv(index=False).encode(),
                               file_name="credit_risk_scored.csv")

if __name__ == "__main__":
    main()
