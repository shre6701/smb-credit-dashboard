import pandas as pd

def assign_aging_bucket(overdue_days):
    if overdue_days <= 0:
        return "Not Due"
    elif overdue_days <= 30:
        return "1-30 Days"
    elif overdue_days <= 60:
        return "31-60 Days"
    elif overdue_days <= 90:
        return "61-90 Days"
    else:
        return "90+ Days"

def preprocess_data(df):
    today = pd.Timestamp.today()
    df['OverdueDays'] = (today - df['Due Date']).dt.days.clip(lower=0)
    df['Aging Bucket'] = df['OverdueDays'].apply(assign_aging_bucket)
    df['Month'] = df['Invoice Date'].dt.to_period('M').astype(str)
    df['AvgInvoiceAmount'] = df.groupby('Party Name')['Amount'].transform('mean')
    df['Payment Status'] = df['Payment Status'].astype(str).str.strip().str.lower()
    return df