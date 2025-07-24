# model/risk_model.py
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from imblearn.over_sampling import SMOTE


def train_model(risk, features):
    X = StandardScaler().fit_transform(risk[features])
    y_raw = risk['RiskLabel']

    try:
        y = LabelEncoder().fit_transform(y_raw)
        if len(np.unique(y)) > 1:
            X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2)
            X_train, y_train = SMOTE().fit_resample(X_train, y_train)
            clf = LogisticRegression(max_iter=1000)
            clf.fit(X_train, y_train)
            preds = clf.predict(X)
            return clf, preds, "SMOTE + Logistic Regression"
        else:
            raise ValueError("Only one class found.")
    except:
        return None, None, "Isolation Forest"