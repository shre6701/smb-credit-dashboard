# SMB Credit Risk Dashboard

A FinTech tool to help small and mid-sized businesses (SMBs) manage and assess credit risk using real-time accounting data from Tally.

---

## 💡 Problem Statement

SMBs often face challenges in:

- Identifying high-risk customers  
- Tracking overdue receivables  
- Detecting financial anomalies  
- Maintaining healthy cash flow  

This tool addresses these challenges by combining:

- 🔗 Tally ERP/Prime data (Excel or real-time integrations)  
- 📊 Dashboards with filters, visual trends, and party-level breakdowns  
- 🧠 AI-powered risk scoring using Logistic Regression + Isolation Forest  
- ⚖️ SMOTE to handle imbalanced datasets  

---

## ⚙️ Key Features

- Party-wise credit risk profiling  
- Overdue analysis with aging buckets and monthly trends  
- Classification into Low / High risk using ML  
- Fallback anomaly detection with Isolation Forest  
- Interactive charts, filters, and export to CSV  

---

## 🧱 Tech Stack

- **Python** (pandas, scikit-learn, imbalanced-learn)  
- **Streamlit** (dashboard UI)  
- **Plotly / Seaborn / Matplotlib** (for visualization)  
- **Tally ERP/Prime** (accounting data source)  

---

## 🗂️ Project Structure

```
smb_credit_dashboard/
├── app.py                     # Streamlit app entrypoint
├── data_loader.py             # File loading logic
├── preprocess.py              # Data cleaning & feature engineering
├── risk_model.py              # SMOTE, Logistic Regression & Isolation Forest logic
├── visuals.py                 # All charts and tables
├── utils.py                   # CSV export & helper utilities
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## 🚀 How to Run the App

```bash
# Step 1: Install required dependencies
pip install -r requirements.txt

# Step 2: Run the Streamlit app
streamlit run app.py
```

---

## 📋 Input Data Format

Your file should be in `.xlsx` or `.csv` format and include these columns:

- `Invoice No`  
- `Party Name`  
- `Invoice Date`  
- `Due Date`  
- `Amount`  
- `Payment Status` (`paid` / `unpaid`)  

Missing values in key fields will be dropped during preprocessing.

---

## 🧠 Machine Learning Logic

- ✅ Uses **SMOTE + Logistic Regression** for interpretable binary classification.
- 🧩 **Fallback to Isolation Forest** when only one risk class is present.
- 📈 Features like `OverdueDays`, `UnpaidRatio`, and `InvoiceAge` are used in scoring.

---

## 📤 Export Functionality

- Export filtered data and risk summary tables directly from the dashboard.

---

## 🔍 Visual Highlights

- 📌 Faceted scatter plots with color-coded risk levels  
- 📊 Risk trendlines and overdue aging heatmaps  
- 🧮 Credit score tables and anomaly flags  
- 📉 Correlation matrix for credit scoring inputs  

---

## 📧 Contact & Contributions

For suggestions or contributions, feel free to fork or raise an issue on the repository.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
