from sklearn.ensemble import IsolationForest

def apply_isolation_forest(X):
    iso = IsolationForest(contamination=0.1, random_state=42)
    iso.fit(X)
    return iso
