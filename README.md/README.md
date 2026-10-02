# FraudLens – Banking Fraud Detection & Risk Analytics Platform

> An end-to-end banking fraud analytics platform combining Python ETL, MySQL relational analytics, SQL views, machine learning, and an interactive Streamlit dashboard.

---

## 📌 Project Overview

**FraudLens** is an end-to-end banking fraud detection and risk analytics platform designed to demonstrate how data engineering, relational databases, SQL analytics, machine learning, and interactive visualization can work together in a unified system.

The project starts with a PaySim-based transaction dataset and processes it using Python. The processed data is transformed into a relational banking database containing customers, accounts, branches, devices, transactions, fraud alerts, login logs, and audit records.

SQL analytical views are then used to perform fraud analysis, while a Random Forest machine learning model identifies transactions that may require further investigation.

The final results are presented through an interactive **Streamlit dashboard**.

---

## 🎯 Project Objectives

The main objectives of FraudLens are to:

- Build an end-to-end fraud analytics pipeline.
- Process and enrich transaction data using Python.
- Design a normalized relational banking database.
- Load and validate banking data in MySQL.
- Develop SQL-based fraud analytics.
- Identify potentially suspicious transactions using machine learning.
- Generate transaction-level ML risk classifications.
- Build an interactive fraud investigation dashboard.
- Demonstrate integration between SQL analytics and machine learning.
- Provide a portfolio-ready example of a data/ML engineering workflow.

---

# 🏗️ System Architecture

```text
                    PaySim-Based Dataset
                            |
                            v
                 +----------------------+
                 | Python Data Processing|
                 |      & ETL           |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Data Transformation  |
                 | & Entity Generation  |
                 +----------+-----------+
                            |
                            v
                      CSV Datasets
                            |
                            v
                 +----------------------+
                 |      MySQL           |
                 |   fraudlens DB       |
                 +----------+-----------+
                            |
             +--------------+--------------+
             |                             |
             v                             v
      SQL Analytical Views          ML Feature Engineering
             |                             |
             v                             v
       SQL Analytics               Random Forest Model
             |                             |
             |                             v
             |                       ML Predictions
             |                             |
             +--------------+--------------+
                            |
                            v
                 +----------------------+
                 | Streamlit Dashboard  |
                 +----------------------+
# FraudLens – End-to-End Banking Fraud Analytics Platform

## End-to-End Data Flow

```text
Raw Dataset
    ↓
Python ETL
    ↓
Data Cleaning / Transformation
    ↓
Entity Generation
    ↓
CSV Files
    ↓
MySQL Database
    ↓
SQL Analytical Views
    ↓
Machine Learning Feature Engineering
    ↓
Random Forest Model
    ↓
Fraud Probability / Risk Classification
    ↓
Streamlit Dashboard
```[cite: 1]

---

## 🛠️ Technology Stack

### Programming & Data Processing
- **Language:** Python[cite: 1]
- **Libraries:** Pandas, NumPy, Faker, tqdm, scikit-learn[cite: 1]

### Database
- **Engine:** MySQL[cite: 1]
- **Management:** MySQL Workbench[cite: 1]

### Machine Learning
- **Library:** Scikit-learn[cite: 1]
- **Model:** Random Forest Classifier[cite: 1]

### Visualization & Dashboard
- **Framework:** Streamlit[cite: 1]
- **Visualization:** Plotly, Pandas[cite: 1]

### Development Tools
- VS Code, Git, GitHub, MySQL Workbench[cite: 1]

---

## 📊 Dataset

FraudLens uses a PaySim-based synthetic financial transaction dataset[cite: 1].
The project processes **30,000 transactions**[cite: 1].
The dataset contains transaction-level information that is enriched with additional banking entities and attributes[cite: 1].

### Dataset Characteristics

| Attribute | Value |
| :--- | :--- |
| **Transactions** | 30,000[cite: 1] |
| **Fraud Transactions** | 84[cite: 1] |
| **Normal Transactions** | 29,916[cite: 1] |
| **Fraud Rate** | 0.28%[cite: 1] |
| **Total Transaction Value** | ₹412,845,080.25[cite: 1] |
| **Total Fraud Amount** | ₹4,942,953.62[cite: 1] |
| **Average Fraud Score** | 25.83[cite: 1] |
| **Transaction Date** | 2026-01-01[cite: 1] |

> **Note:** All transactions in the current dataset occur on a single calendar date[cite: 1]. Therefore, the dashboard uses a transaction-date summary rather than presenting a multi-day trend[cite: 1].

---

## 🗄️ Database Design

The project uses a MySQL database named `fraudlens` which contains 10 major tables[cite: 1].

| Table | Purpose | Records |
| :--- | :--- | :--- |
| **Branch** | Banking branch information | 20[cite: 1] |
| **Customer** | Customer information | 47,801[cite: 1] |
| **Account** | Customer account information | 47,801[cite: 1] |
| **Device** | Device information | 95,774[cite: 1] |
| **BankUser** | Bank employee/user information | 50[cite: 1] |
| **FraudRule** | Fraud detection rules | 6[cite: 1] |
| **BankTransaction** | Core transaction data | 30,000[cite: 1] |
| **LoginLog** | Login/activity records | 30,000[cite: 1] |
| **FraudAlert** | Fraud alert records | 84[cite: 1] |
| **AuditLog** | Transaction audit records | 30,000[cite: 1] |

---

## 🧩 Core Database Relationships

The main relationship structure is:

```text
Branch
  |
  +---- Customer
          |
          +---- Account
                  |
                  +---- BankTransaction
                          |
                          +---- FraudAlert
                          |
                          +---- AuditLog

Device
  |
  +---- BankTransaction

Customer
  |
  +---- LoginLog
```[cite: 1]

The relational structure allows transactions to be analyzed together with their associated customers, accounts, devices, alerts, and audit information[cite: 1].

---

## 🔄 ETL Pipeline

The Python ETL pipeline performs the following major operations:

```text
Load Source Dataset
        ↓
Extract Unique Accounts
        ↓
Create Account Mapping
        ↓
Generate Branches
        ↓
Generate Customers
        ↓
Generate Accounts
        ↓
Generate Devices
        ↓
Generate Bank Users
        ↓
Generate Fraud Rules
        ↓
Generate Banking Transactions
        ↓
Generate Login Logs
        ↓
Generate Fraud Alerts
        ↓
Generate Audit Logs
        ↓
Export CSV Files
        ↓
Load Data into MySQL
        ↓
Validate Record Counts
```[cite: 1]

---

## 📁 Generated Data Files

The ETL process generates:

```text
dataset/
├── Mapping.csv
├── Branch.csv
├── Customer.csv
├── Account.csv
├── Device.csv
├── BankUser.csv
├── FraudRule.csv
├── BankTransaction.csv
├── LoginLog.csv
├── FraudAlert.csv
└── AuditLog.csv
```[cite: 1]

---

## 🧮 SQL Analytics

FraudLens uses SQL analytical views to simplify repeated fraud analysis[cite: 1].
The project contains the following views:

- `vw_fraud_summary`[cite: 1]
- `vw_fraud_by_type`[cite: 1]
- `vw_fraud_by_channel`[cite: 1]
- `vw_fraud_by_location`[cite: 1]
- `vw_high_risk_transactions`[cite: 1]
- `vw_customer_fraud_risk`[cite: 1]
- `vw_alert_summary`[cite: 1]
- `vw_device_risk`[cite: 1]
- `vw_daily_fraud_trend`[cite: 1]
- `vw_login_risk`[cite: 1]

### SQL Analytics Include
- Overall fraud summary[cite: 1]
- Fraud by transaction type[cite: 1]
- Fraud by transaction channel[cite: 1]
- Fraud by location[cite: 1]
- High-risk transactions[cite: 1]
- Customer fraud risk[cite: 1]
- Fraud alert summaries[cite: 1]
- Device risk analysis[cite: 1]
- Date-based transaction analysis[cite: 1]
- Login risk analysis[cite: 1]

---

## 🤖 Machine Learning

FraudLens uses a **Random Forest Classifier** to predict whether a transaction may be fraudulent[cite: 1].

### Target Variable
- **`fraud_flag`**[cite: 1]
  - **`0`** → Normal[cite: 1]
  - **`1`** → Fraud[cite: 1]

---

## 🧠 Machine Learning Features

The model uses transaction, contextual, device, temporal, and behavioral features[cite: 1]:

- **Transaction Features:** `amount`, `log_amount`, `transaction_type`[cite: 1]
- **Context Features:** `channel`, `city`[cite: 1]
- **Device Features:** `device_type`, `operating_system`, `trusted_device`[cite: 1]
- **Temporal Features:** `transaction_hour`, `transaction_dayofweek`, `is_weekend`, `is_night`[cite: 1]
- **Behavioral Features:** `is_high_value`, `sender_transaction_count`, `sender_average_amount`, `device_transaction_count`, `account_pair_frequency`[cite: 1]

---

## 🚫 Data Leakage Prevention

The following fields are not used as model input features:

- `fraud_flag` (target variable)[cite: 1]
- `fraud_score` (pre-existing fraud signal)[cite: 1]

Excluding `fraud_score` prevents the ML model from directly relying on a pre-existing fraud indicator[cite: 1].
This allows the model to learn independently from transaction, behavioral, device, location, and temporal features[cite: 1].

---

## 🌲 Random Forest Configuration

```python
RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    min_samples_leaf=2,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)
```[cite: 1]

- **Train/Test Split:** 80% Training / 20% Testing (Stratified)[cite: 1]
- **Training records:** 24,000[cite: 1]
- **Testing records:** 6,000[cite: 1]

---

## 📈 Model Evaluation

The model achieved the following results on the test dataset:

| Metric | Result |
| :--- | :--- |
| **Precision** | 0.0524[cite: 1] |
| **Recall** | 0.8235[cite: 1] |
| **F1-score** | 0.0986[cite: 1] |
| **ROC-AUC** | 0.9521[cite: 1] |

### Interpretation
- The model detected a substantial proportion of fraud cases in the test set (**14 / 17** fraudulent transactions detected)[cite: 1].
- However, the model also generated a relatively large number of false positives[cite: 1].
- Therefore, the current model is better viewed as a potential fraud identification and transaction-prioritization component rather than a system that independently confirms fraud[cite: 1].

---

## 🔢 Confusion Matrix

```python
[[5730,  253],
 [   3,   14]]
```[cite: 1]

| Actual / Predicted | Predicted Normal | Predicted Fraud |
| :--- | :--- | :--- |
| **Actual Normal** | 5,730 | 253 |
| **Actual Fraud** | 3 | 14 |

- **True Negatives (TN):** 5,730[cite: 1]
- **False Positives (FP):** 253[cite: 1]
- **False Negatives (FN):** 3[cite: 1]
- **True Positives (TP):** 14[cite: 1]

---

## 🚨 ML Risk Distribution

After training, the model was applied to the complete dataset of 30,000 transactions, predicting **1,311** potentially fraudulent transactions[cite: 1].

| Risk Level | Transactions |
| :--- | :--- |
| **Low** | 25,779[cite: 1] |
| **Medium** | 3,490[cite: 1] |
| **High** | 650[cite: 1] |
| **Critical** | 81[cite: 1] |
| **Total** | **30,000**[cite: 1] |

> **Note:** The 1,311 ML predictions represent transactions identified by the model as potentially suspicious; they should not be interpreted as confirmed fraudulent transactions[cite: 1].

---

## 📊 Streamlit Dashboard

FraudLens provides an interactive Streamlit dashboard with four major pages[cite: 1]:

```text
FraudLens
│
├── 📊 Dashboard
├── 🔎 Transaction Investigation
├── 🚨 Fraud Alerts
└── 🤖 ML Risk Analysis
```[cite: 1]

### 📊 1. Dashboard
Displays key metrics and high-level summaries[cite: 1]:
- **Transactions:** 30,000[cite: 1]
- **Fraud Cases:** 84[cite: 1]
- **Fraud Rate:** 0.28%[cite: 1]
- **Fraud Amount:** ₹49,429,530.62[cite: 1]
- Fraud distribution by transaction type, channel, location, and date[cite: 1].

### 🔎 2. Transaction Investigation
Allows users to investigate individual transactions with consolidated details across tables[cite: 1]:
- **Transaction Info:** ID, type, amount, status, timestamp, fraud flag, fraud score[cite: 1].
- **Customer Info:** ID, name, type, branch info[cite: 1].
- **Device Info:** ID, device type, operating system, trusted status[cite: 1].

### 🚨 3. Fraud Alert Center
Interface for reviewing generated fraud alerts[cite: 1]:
- **Total Alerts:** 84 | **High Alerts:** 84 | **Critical:** 0 | **Open:** 84[cite: 1]
- Displays risk scores, levels, fraud reasons, alert statuses, and customer mappings[cite: 1].

### 🤖 4. ML Risk Analysis
Displays model evaluation and prediction outputs[cite: 1]:
- Performance metrics (Precision, Recall, F1, ROC-AUC)[cite: 1]
- Predicted fraud, high-risk, and critical-risk transaction counts[cite: 1]
- Risk probability distributions, highest-risk transaction table, and confusion matrix[cite: 1].

---

## 🖥️ Project Screenshots

Located in `screenshots/`[cite: 1]:

| Screenshot | Description |
| :--- | :--- |
| `01_dashboard.png` | Main FraudLens dashboard[cite: 1] |
| `02_transaction_investigation.png` | Individual transaction investigation[cite: 1] |
| `03_fraud_alert_center.png` | Fraud alert center[cite: 1] |
| `04_ml_risk_analysis.png` | ML risk analysis[cite: 1] |
| `05_sql_database.png` | MySQL database/EER diagram[cite: 1] |
| `06_sql_analytics.png` | SQL analytical queries/results[cite: 1] |
| `07_ml_training.png` | ML training and evaluation[cite: 1] |

---

## 📂 Project Structure

```text
FraudLens-Banking-Fraud-Analytics/
│
├── dataset/
│   ├── FraudLens_30000.csv
│   ├── Mapping.csv
│   ├── Branch.csv
│   ├── Customer.csv
│   ├── Account.csv
│   ├── Device.csv
│   ├── BankUser.csv
│   ├── FraudRule.csv
│   ├── BankTransaction.csv
│   ├── LoginLog.csv
│   ├── FraudAlert.csv
│   └── AuditLog.csv
│
├── docs/
│   ├── architecture.md
│   ├── database_design.md
│   ├── etl_pipeline.md
│   ├── machine_learning.md
│   └── dashboard.md
│
├── models/
│   ├── fraud_model.pkl
│   ├── model_metrics.json
│   └── confusion_matrix.png
│
├── output/
│   └── ML_Predictions.csv
│
├── reports/
│   ├── FraudLens_Project_Report.pdf
│   ├── dataset_analysis.md
│   └── model_evaluation.md
│
├── screenshots/
│   ├── 01_dashboard.png
│   ├── 02_transaction_investigation.png
│   ├── 03_fraud_alert_center.png
│   ├── 04_ml_risk_analysis.png
│   ├── 05_sql_database.png
│   ├── 06_sql_analytics.png
│   └── 07_ml_training.png
│
├── scripts/
│   ├── app.py
│   ├── config.py
│   ├── generate_dataset.py
│   ├── load_database.py
│   └── train_fraud_model.py
│
├── sql/
│   └── 06_analytics_views.sql
│
├── README.md
└── requirements.txt
```[cite: 1]

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd FraudLens-Banking-Fraud-Analytics
```[cite: 1]

### 2. Create a Virtual Environment
**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```[cite: 1]

*(Explicit Python 3.13 usage if multiple versions exist)*[cite: 1]:
```bash
py -3.13 -m venv venv
venv\Scripts\activate
```[cite: 1]

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```[cite: 1]

---

## 🗄️ MySQL Setup

1. **Start MySQL:** Ensure your local MySQL server is running[cite: 1].
2. **Create the Database:**
   ```sql
   CREATE DATABASE fraudlens;
   USE fraudlens;
   ```[cite: 1]
3. **Create Tables:** Create the 10 FraudLens tables as defined in `docs/database_design.md`[cite: 1].

---

## 🔄 Execution Steps

### 1. Run the ETL Pipeline
Generates CSV files inside `dataset/`[cite: 1]:
```bash
python scripts/generate_dataset.py
```[cite: 1]

### 2. Load Data into MySQL
Clears existing data safely, loads generated CSVs, and validates row counts[cite: 1]:
```bash
python scripts/load_database.py
```[cite: 1]

### 3. Create SQL Analytical Views
Execute `sql/06_analytics_views.sql` inside MySQL Workbench to construct analytical views[cite: 1].

### 4. Train the ML Model
Performs feature engineering, trains Random Forest, calculates metrics, and generates predictions[cite: 1]:
```bash
python scripts/train_fraud_model.py
```[cite: 1]

### 5. Launch the Dashboard
```bash
streamlit run scripts/app.py
```[cite: 1]

---

## 🔍 Example SQL Analysis

```sql
-- Overall fraud summary
SELECT * FROM vw_fraud_summary;

-- Fraud by transaction type
SELECT * FROM vw_fraud_by_type;

-- High-risk transactions
SELECT * FROM vw_high_risk_transactions;

-- Customer-level fraud risk
SELECT * FROM vw_customer_fraud_risk;
```[cite: 1]

---

## 🔐 FraudLens Analytical Layers

1. **Layer 1 – Data Engineering:** Python (ETL, transformations, synthetic generation, validation)[cite: 1].
2. **Layer 2 – Relational Database:** MySQL (Structured storage, schemas, constraints, relations)[cite: 1].
3. **Layer 3 – SQL Analytics:** SQL Views (Aggregations, risk indices, location/device metrics)[cite: 1].
4. **Layer 4 – Machine Learning:** Random Forest (Risk classification, probability scoring)[cite: 1].
5. **Layer 5 – Visualization:** Streamlit & Plotly (Interactive UI, alerts, transaction exploration)[cite: 1].

---

## 📌 Key Project Results

- **30,000** total transactions[cite: 1]
- **84** confirmed dataset fraud cases (**0.28%** fraud rate)[cite: 1]
- **₹49,429,530.62** total fraud amount[cite: 1]
- **84** fraud alerts[cite: 1]
- **1,311** ML predicted fraud cases (**650** High Risk, **81** Critical Risk)[cite: 1]
- **ML Evaluation:** Precision = `0.0524`, Recall = `0.8235`, F1 = `0.0986`, ROC-AUC = `0.9521`[cite: 1]

---

## ⚠️ Project Limitations

- Synthetic dataset based on PaySim[cite: 1].
- Single-date coverage (2026-01-01) preventing multi-day time series analysis[cite: 1].
- Extreme class imbalance (0.28% positive cases)[cite: 1].
- Prototype ML model produces high false positives; intended as a risk-ranking component rather than automated decisioning[cite: 1].
- Lacks production-grade authorization, real-time ingestion, and security controls[cite: 1].

---

## 🚀 Future Enhancements

- **Data:** Larger multi-date datasets, real-time transaction streams, enriched customer histories[cite: 1].
- **ML:** XGBoost/LightGBM, threshold optimization, PR-AUC evaluation, Explainable AI (SHAP), drift monitoring[cite: 1].
- **Database:** Stored procedures, automated triggers, optimized indexing[cite: 1].
- **Dashboard:** Authentication/RBAC, real-time alerts, downloadable reports[cite: 1].
- **Deployment:** Dockerization, CI/CD pipeline, cloud database hosting[cite: 1].

---

## 👨‍💻 Project Workflow Summary

```text
                 FRAUDLENS
                    |
                    v
          +-------------------+
          | PaySim Dataset    |
          +---------+---------+
                    |
                    v
          +-------------------+
          | Python ETL        |
          +---------+---------+
                    |
                    v
          +-------------------+
          | Enriched CSV Data |
          +---------+---------+
                    |
                    v
          +-------------------+
          | MySQL Database    |
          +---------+---------+
                    |
             +------+------+
             |             |
             v             v
       SQL Analytics      ML
             |             |
             |             v
             |       Random Forest
             |             |
             |             v
             |       Risk Predictions
             |             |
             +------+------+
                    |
                    v
          +-------------------+
          | Streamlit         |
          | Dashboard         |
          +-------------------+
                    |
        +-----------+-----------+
        |           |           |
        v           v           v
    Analytics   Investigation  Alerts
                    |
                    v
               ML Risk
                Analysis
```[cite: 1]

---

## ✅ Project Status

| Component | Status |
| :--- | :---: |
| **Dataset Preparation** | ✅ Completed[cite: 1] |
| **Python ETL Pipeline** | ✅ Completed[cite: 1] |
| **CSV Generation** | ✅ Completed[cite: 1] |
| **MySQL Database** | ✅ Completed[cite: 1] |
| **Database Loading** | ✅ Completed[cite: 1] |
| **SQL Analytical Views** | ✅ Completed[cite: 1] |
| **ML Model** | ✅ Completed[cite: 1] |
| **Model Evaluation** | ✅ Completed[cite: 1] |
| **ML Predictions** | ✅ Completed[cite: 1] |
| **Streamlit Dashboard** | ✅ Completed[cite: 1] |
| **Transaction Investigation** | ✅ Completed[cite: 1] |
| **Fraud Alert Center** | ✅ Completed[cite: 1] |
| **ML Risk Analysis** | ✅ Completed[cite: 1] |
| **Project Documentation** | ✅ Completed[cite: 1] |
| **Screenshots** | ✅ Completed[cite: 1] |

---

## 📌 Conclusion

FraudLens demonstrates a complete data-driven fraud analytics workflow starting from transaction data and progressing through ETL, relational database management, SQL analytics, machine learning, and interactive visualization[cite: 1].

The project combines multiple technologies into a single banking analytics platform where SQL provides structured analytical insights and machine learning provides predictive risk information[cite: 1].

The final Streamlit dashboard brings these components together into an interactive environment for transaction investigation, fraud alert analysis, and ML-based risk analysis[cite: 1].

FraudLens is designed as a portfolio and academic project demonstrating practical skills across Data Engineering, SQL, Data Analytics, Machine Learning, and Dashboard Development[cite: 1].