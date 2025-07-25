import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from utils import background_color_risk

def show_kpis(df, unpaid_df):
    col1, col2, col3 = st.columns(3)
    total_invoices = len(df)
    unpaid_amount = unpaid_df['Amount'].sum()
    overdue_pct = (unpaid_amount / df['Amount'].sum()) * 100 if df['Amount'].sum() else 0
    col1.metric("📦 Total Invoices", f"{total_invoices}")
    col2.metric("💰 Unpaid Amount", f"₹{unpaid_amount:,.2f}")
    col3.metric("⚠️ % Invoices Overdue", f"{overdue_pct:.2f}%")

def show_trendline(unpaid_df):
    st.subheader("📈 Overdue Trendline")
    trend = unpaid_df.groupby('Month')['Amount'].sum().sort_index()
    st.line_chart(trend)

def show_aging_chart(unpaid_df):
    st.subheader("🧾 Invoice Aging")
    aging = unpaid_df.groupby('Aging Bucket')['Amount'].sum()
    st.bar_chart(aging)

def show_credit_score_table(risk):
    st.subheader("🔢 Credit Score Table")
    st.dataframe(risk[['OverdueDays', 'Amount', 'Unpaid Ratio', 'Credit Score', 'RiskLabel']], use_container_width=True)

def show_correlation_heatmap(risk):
    corr = risk[['OverdueDays', 'Amount', 'Unpaid Ratio']].corr()
    fig, ax = plt.subplots(figsize=(2.5, 2.5))
    sns.heatmap(corr, annot=True, cmap="RdBu", fmt=".2f", linewidths=0.5, ax=ax, square=True, cbar=False)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    st.pyplot(fig)

def show_risk_distribution(risk):
    fig, ax = plt.subplots(figsize=(4, 3))
    sns.boxplot(data=risk, x='RiskLabel', y='Credit Score', palette='Set2', ax=ax)
    sns.stripplot(data=risk, x='RiskLabel', y='Credit Score', color='black', alpha=0.3, ax=ax)
    ax.set_title("Credit Score Distribution by Risk Level")
    st.pyplot(fig)

def show_avg_factors_by_risk(risk):
    risk_grouped = risk.groupby('RiskLabel')[['OverdueDays', 'Amount', 'Unpaid Ratio']].mean().reset_index()
    fig_bar = px.bar(
        risk_grouped.melt(id_vars='RiskLabel', var_name='Factor', value_name='Average'),
        x='Factor', y='Average', color='RiskLabel', barmode='group',
        title="Average Factors by Risk Level", text_auto=True, height=300
    )
    st.plotly_chart(fig_bar, use_container_width=True)

def show_high_risk_table(risk, threshold):
    risky = risk[risk['Credit Score'] < threshold].copy()
    st.write(f"{len(risky)} parties fall below threshold of {threshold}")
    styled = risky[['OverdueDays', 'Amount', 'Unpaid Ratio', 'Credit Score', 'RiskLabel']].style.map(
        background_color_risk, subset=['RiskLabel']
    ).format({
        'OverdueDays': '{:.2f}',
        'Amount': '{:.2f}',
        'Unpaid Ratio': '{:.2f}',
        'Credit Score': '{:.2f}'
    })
    st.dataframe(styled, use_container_width=True)

def show_facet_scatter(risk):
    st.subheader("📉 Credit Score vs Overdue Days (Faceted Scatter)")
    selected = st.sidebar.multiselect(
        "Select Risk Levels",
        options=risk['RiskLabel'].unique(),
        default=risk['RiskLabel'].unique()
    )
    data = risk[risk['RiskLabel'].isin(selected)]
    if not data.empty:
        fig = px.scatter(
            data, x="OverdueDays", y="Credit Score", size="Amount",
            color="RiskLabel", facet_col="RiskLabel", hover_name=data.index,
            hover_data={"OverdueDays": True, "Credit Score": True, "Amount": ":,.0f", "Unpaid Ratio": ":.2f"},
            opacity=0.7, title="Credit Score vs Overdue Days by Risk Level", height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data to show for selected risk levels.")
