# scripts/risk_aggregation.py
def label_risk(row):
    if row['OverdueDays'] > 90 and row['Amount'] > 30000:
        return 'High'
    elif row['OverdueDays'] > 30:
        return 'Medium'
    else:
        return 'Low'

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
    risk['Unpaid Ratio'] = risk['Unpaid Ratio'].fillna(0)
    risk['Credit Score'] = 100 - (risk['OverdueDays'] * 0.5 + risk['Unpaid Ratio'] * 50)
    risk['Credit Score'] = risk['Credit Score'].clip(0, 100).round(2)
    risk['RiskLabel'] = risk.apply(label_risk, axis=1)
    return risk.round(2)
