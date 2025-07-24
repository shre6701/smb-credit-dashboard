# SMB Credit Risk Dashboard

A FinTech tool to help small and mid-sized businesses (SMBs) manage and assess credit risk using real-time accounting data from Tally.

## 💡 Problem Statement

SMBs often face challenges in:

* Identifying high-risk customers
* Tracking overdue receivables
* Detecting financial anomalies
* Maintaining healthy cash flow

This tool solves these issues by combining:

* 🔗 Tally ERP/Prime data (Excel or real-time integrations)
* 📊 Dashboards with filters, visual trends, and party-level breakdowns
* 🧠 AI-powered risk scoring using Logistic Regression + Isolation Forest
* ⚖️ SMOTE to handle imbalanced datasets

## ⚙️ Key Features

* Party-wise credit risk profiling
* Aging analysis with overdue trendlines
* Classification of risk into Low / High
* Anomaly detection for unusual entries
* Interactive and exportable dashboard

## 🧱 Tech Stack

* Python (pandas, scikit-learn, imbalanced-learn)
* Streamlit (dashboard UI)
* Plotly, Seaborn, Matplotlib (for visualizations)
* Tally (for accounting data source)

## 🗂️ Project Structure

```
smb_credit_dashboard/
├── data/                    # Raw and sample Tally data
│   └── sample_tally_data.csv
├── model/                  # ML model definitions
│   └── risk_model.py
├── scripts/                # Data loading, processing, and anomaly detection
│   ├── load_data.py
│   ├── feature_pipeline.py
│   └── anomaly_detection.py
├── dashboard/              # Streamlit UI app
│   └── dashboard_app.py
├── utils/                  # Helper functions and CSV export
│   └── helpers.py
├── requirements.txt        # Python dependencies
├── LICENSE                 # MIT License
└── README.md               # Project documentation
```

## 🚀 How to Run the App

```bash
pip install -r requirements.txt
streamlit run dashboard/dashboard_app.py
```

---

### 📄 License

This project is licensed under the [MIT License](LICENSE).
