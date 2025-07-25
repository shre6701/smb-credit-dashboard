from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import numpy as np
import streamlit as st

def run_risk_model(risk):
    features = ['OverdueDays', 'Amount', 'Credit Score', 'UnpaidCount', 'AvgInvoiceAmount']
    risk = risk.dropna(subset=features)
    X = StandardScaler().fit_transform(risk[features])
    y_raw = risk['RiskLabel']

    try:
        y = LabelEncoder().fit_transform(y_raw)
        if len(np.unique(y)) > 1:
            X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2)
            X_train, y_train = SMOTE().fit_resample(X_train, y_train)
            clf = LogisticRegression(max_iter=1000)
            clf.fit(X_train, y_train)
            risk['ModelPrediction'] = clf.predict(X)
            st.success("✅ Model Applied: SMOTE + Logistic Regression")
        else:
            raise ValueError("Only one class found.")
    except:
        iso = IsolationForest(contamination=0.1, random_state=42)
        iso.fit(X)
        risk['AnomalyScore'] = iso.decision_function(X)
        risk['IsAnomaly'] = iso.predict(X)
        risk['RiskStatus'] = risk['IsAnomaly'].map({1: 'Normal', -1: 'Anomaly'})
        st.warning("⚠️ Only one class found. Applied Isolation Forest.")
    
    return risk
