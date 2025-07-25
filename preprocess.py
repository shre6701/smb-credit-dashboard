import pandas as pd
from utils import assign_aging_bucket, label_risk

def preprocess_data(df):
    today = pd.Timestamp.today()
    df['OverdueDays'] = (today - df['Due Date']).dt.days.clip(lower=0)
    df['Aging Bucket'] = df['OverdueDays'].apply(assign_aging_bucket)
    df['Month'] = df['Invoice Date'].dt.to_period('M').astype(str)
    df['AvgInvoiceAmount'] = df.groupby('Party Name')['Amount'].transform('mean')
    df['Payment Status'] = df['Payment Status'].astype(str).str.strip().str.lower()
    return df

def aggregate_risk(df):
    risk = df.groupby('Party Name').agg(
        Total_Invoices=('Invoice No', 'count'),
        OverdueDays=('OverdueDays', 'mean'),
        Amount=('Amount', 'sum'),
        UnpaidCount=('Payment Status', lambda x: (x == 'unpaid').sum()),
        AvgInvoiceAmount=('AvgInvoiceAmount', 'mean')
    )
    risk = risk[risk['Total_Invoices'] > 0]
    risk['Unpaid Ratio'] = risk['UnpaidCount'] / risk['Total_Invoices']
    risk['Credit Score'] = 100 - (risk['OverdueDays'] * 0.5 + risk['Unpaid Ratio'] * 50)
    risk['Credit Score'] = risk['Credit Score'].clip(0, 100).round(2)
    risk['RiskLabel'] = risk.apply(label_risk, axis=1)
    return risk.round(2)
