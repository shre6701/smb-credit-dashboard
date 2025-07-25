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

def label_risk(row):
    if row['OverdueDays'] > 90 and row['Amount'] > 30000:
        return 'High'
    elif row['OverdueDays'] > 30:
        return 'Medium'
    else:
        return 'Low'

def background_color_risk(val):
    if val == 'High':
        return 'background-color: #ffcccc'
    elif val == 'Medium':
        return 'background-color: #fff2cc'
    else:
        return 'background-color: #ccffcc'
