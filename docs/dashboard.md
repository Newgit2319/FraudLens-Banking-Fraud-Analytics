# FraudLens – Dashboard Documentation

## 1. Overview

FraudLens provides an interactive web dashboard built using **Streamlit**.

The dashboard combines:

- MySQL database analytics
- SQL analytical views
- Transaction investigation
- Fraud alerts
- Machine learning predictions
- Interactive charts and tables

The dashboard acts as the presentation layer of the FraudLens platform.

---

## 2. Technologies Used

The dashboard uses the following technologies:

- Python
- Streamlit
- MySQL
- mysql-connector-python
- Pandas
- Plotly
- Scikit-learn model outputs

The application is implemented in:

```text
scripts/app.py
# FraudLens – Dashboard Architecture & Documentation

## 3. Dashboard Architecture

The dashboard follows this data flow:

```text
MySQL Database
      |
      v
SQL Analytical Views
      |
      v
Python / Pandas
      |
      v
Streamlit Application
      |
      +----------------------+
      |          |           |
      v          v           v
Dashboard   Investigation   Alerts
      |
      v
ML Risk Analysis
```[cite: 1]

The application connects to the `fraudlens` MySQL database and retrieves analytical information for display[cite: 1].

---

## 4. Dashboard Pages

The FraudLens dashboard contains four major pages:

- **Dashboard**[cite: 1]
- **Transaction Investigation**[cite: 1]
- **Fraud Alerts**[cite: 1]
- **ML Risk Analysis**[cite: 1]

---

## 5. Dashboard Page

The main Dashboard page provides an overview of the banking transaction environment[cite: 1].

### Key Metrics
The dashboard displays:

- Total Transactions[cite: 1]
- Fraud Cases[cite: 1]
- Fraud Rate[cite: 1]
- Fraud Amount[cite: 1]
- Average Risk Score[cite: 1]

Current dataset values include:

- **Total Transactions:** 30,000[cite: 1]
- **Fraud Cases:** 84[cite: 1]
- **Fraud Rate:** 0.28%[cite: 1]
- **Total Fraud Amount:** ₹49,429,530.62[cite: 1]

The metrics are retrieved from the database and analytical views rather than being manually entered into the dashboard[cite: 1].

### 5.1 Fraud by Transaction Type
A chart displays fraudulent transactions grouped by transaction type[cite: 1].
The transaction types are based on the PaySim transaction categories:

- `TRANSFER`[cite: 1]
- `PAYMENT`[cite: 1]
- `CASH_OUT`[cite: 1]
- `CASH_IN`[cite: 1]
- `DEBIT`[cite: 1]

This allows users to examine how confirmed fraud records are distributed across transaction categories[cite: 1].

### 5.2 Fraud by Channel
The dashboard displays fraud activity according to transaction channel[cite: 1].
This provides a view of how fraudulent transactions are distributed across different banking channels[cite: 1].

### 5.3 Transaction Date Summary
The current dataset contains all 30,000 transactions on a single calendar date[cite: 1].
Therefore, the dashboard uses a Transaction Date Summary instead of presenting a misleading multi-day trend[cite: 1].

The summary displays:

- Transaction date[cite: 1]
- Transaction count[cite: 1]
- Fraud cases[cite: 1]
- Fraud amount[cite: 1]

This accurately reflects the available dataset[cite: 1].

### 5.4 Fraud by Location
The dashboard also provides location-based fraud analysis[cite: 1].
The location analysis can be used to examine:

- Transaction locations[cite: 1]
- Transaction counts[cite: 1]
- Fraud counts[cite: 1]
- Fraud rates[cite: 1]
- Fraud amounts[cite: 1]

Fraud rate helps compare locations with different transaction volumes[cite: 1].

---

## 6. Transaction Investigation

The Transaction Investigation page allows users to investigate an individual transaction[cite: 1].
A transaction can be selected using its transaction ID[cite: 1].
For the selected transaction, the dashboard displays information from multiple database entities[cite: 1].

### Transaction Information
Examples include:
- Transaction ID[cite: 1]
- Transaction type[cite: 1]
- Transaction amount[cite: 1]
- Transaction status[cite: 1]
- Transaction timestamp[cite: 1]
- Fraud flag[cite: 1]
- Fraud score[cite: 1]

### Customer Information
The investigation view can display associated customer information such as:
- Customer ID[cite: 1]
- Customer name[cite: 1]
- Customer type[cite: 1]
- Branch information[cite: 1]

### Device Information
Device-related information can also be displayed, including:
- Device ID[cite: 1]
- Device type[cite: 1]
- Operating system[cite: 1]
- Trusted-device status[cite: 1]

This provides a consolidated view of the transaction instead of requiring the analyst to query individual tables manually[cite: 1].

---

## 7. Fraud Alert Center

The Fraud Alert Center provides an interface for reviewing fraud alerts generated from the database[cite: 1].
The page displays:

- Total alerts[cite: 1]
- Critical alerts[cite: 1]
- High-risk alerts[cite: 1]
- Open alerts[cite: 1]

Users can filter the alert records and inspect individual alert information[cite: 1].

### 7.1 Alert Information
The alert table contains information such as:

- Alert ID[cite: 1]
- Transaction ID[cite: 1]
- Customer ID[cite: 1]
- Risk score[cite: 1]
- Alert level[cite: 1]
- Fraud reason[cite: 1]
- Alert status[cite: 1]
- Created timestamp[cite: 1]
- Customer name[cite: 1]

This allows analysts to review the transactions associated with generated fraud alerts[cite: 1].

### 7.2 Current Alert Distribution
The current generated dataset contains:

- **Total alerts:** 84[cite: 1]
- **High alerts:** 84[cite: 1]
- **Critical alerts:** 0[cite: 1]
- **Open alerts:** 84[cite: 1]

The uniform alert level reflects the current generated fraud-alert data and is not a dashboard error[cite: 1].

---

## 8. ML Risk Analysis

The ML Risk Analysis page integrates the trained machine learning model with the dashboard[cite: 1].
The page presents the model's transaction-level predictions and evaluation results[cite: 1].

### Key ML Metrics

| Metric | Value |
| :--- | :--- |
| **Precision** | 0.0524[cite: 1] |
| **Recall** | 0.8235[cite: 1] |
| **F1-score** | 0.0986[cite: 1] |
| **ROC-AUC** | 0.9521[cite: 1] |

These values are loaded from the model evaluation output[cite: 1].

### 8.1 ML Prediction Summary
The complete dataset contains 30,000 transactions[cite: 1].
The model generated:

- **Predicted fraud transactions:** 1,311[cite: 1]

#### Risk Distribution

| Risk Level | Transactions |
| :--- | :--- |
| **Low** | 25,779[cite: 1] |
| **Medium** | 3,490[cite: 1] |
| **High** | 650[cite: 1] |
| **Critical** | 81[cite: 1] |

The ML prediction should be interpreted as a model-generated risk indication rather than confirmation of actual fraud[cite: 1].

---

## 9. Risk Distribution

The ML page provides a visualization of the number of transactions in each risk category[cite: 1].
The categories are:

- Low[cite: 1]
- Medium[cite: 1]
- High[cite: 1]
- Critical[cite: 1]

This helps users quickly understand the overall distribution of model-generated risk[cite: 1].

---

## 10. Fraud Probability Distribution

The dashboard also provides a probability distribution visualization[cite: 1].
The model generates a probability associated with the fraud class for each transaction[cite: 1].
The probability distribution allows users to examine how model confidence varies across transactions[cite: 1].

---

## 11. Highest-Risk Transactions

The dashboard provides a table containing transactions with the highest model-generated risk[cite: 1].
The table allows users to inspect transactions that have received high fraud probabilities[cite: 1].
This provides a practical connection between the machine learning model and transaction investigation workflow[cite: 1].

---

## 12. Confusion Matrix

The ML Risk Analysis page displays the model's confusion matrix[cite: 1].

Current test-set confusion matrix:

```python
[[5730,  253],
 [   3,   14]]
```[cite: 1]

### Matrix Interpretation

| | Predicted Normal | Predicted Fraud |
| :--- | :--- | :--- |
| **Actual Normal** | 5,730 | 253 |
| **Actual Fraud** | 3 | 14 |

The visualization helps users understand the model's true positives, true negatives, false positives, and false negatives[cite: 1].

---

## 13. SQL Analytics Integration

The dashboard uses SQL analytical views created in the MySQL database[cite: 1].
The views include:

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

The dashboard retrieves these analytical results and converts them into interactive tables, metrics, and charts[cite: 1].

---

## 14. Database Integration

The Streamlit application connects to the MySQL database:

- **Database:** `fraudlens`[cite: 1]

The application retrieves:

- Transaction data[cite: 1]
- Customer data[cite: 1]
- Account data[cite: 1]
- Device data[cite: 1]
- Fraud alerts[cite: 1]
- SQL analytical results[cite: 1]
- ML predictions[cite: 1]

The database acts as the central storage layer for the application[cite: 1].

---

## 15. Interactive Features

The dashboard provides several interactive capabilities:

- **Filters:** Users can filter alert and analytical information based on available fields[cite: 1].
- **Transaction Selection:** Users can select a transaction ID and investigate its details[cite: 1].
- **Interactive Charts:** Plotly visualizations allow users to interact with charts and inspect individual values[cite: 1].
- **Risk Analysis:** Users can examine ML-generated risk levels and high-risk transactions[cite: 1].
- **Alert Investigation:** Users can review generated fraud alerts and their associated transaction information[cite: 1].

---

## 16. Dashboard Design

The dashboard is organized into separate functional pages to keep investigation workflows clear[cite: 1].

```text
FraudLens
│
├── Dashboard
│   ├── KPIs
│   ├── Fraud by Type
│   ├── Fraud by Channel
│   ├── Date Summary
│   └── Location Analysis
│
├── Transaction Investigation
│   ├── Transaction Details
│   ├── Customer Details
│   └── Device Details
│
├── Fraud Alerts
│   ├── Alert Summary
│   ├── Alert Filters
│   └── Alert Records
│
└── ML Risk Analysis
    ├── Model Metrics
    ├── Risk Distribution
    ├── Probability Distribution
    ├── High-Risk Transactions
    └── Confusion Matrix
```[cite: 1]

---

## 17. Dashboard Screenshots

The project includes screenshots demonstrating the major dashboard components[cite: 1].

### Recommended Screenshots
```text
screenshots/
├── 01_dashboard.png
├── 02_transaction_investigation.png
├── 03_fraud_alert_center.png
├── 04_ml_risk_analysis.png
├── 05_sql_database.png
├── 06_sql_analytics.png
└── 07_ml_training.png
```[cite: 1]

### Screenshot Descriptions
- **`01_dashboard.png`**: Shows the main FraudLens dashboard with KPIs, fraud analysis charts, date summary, and location analysis[cite: 1].
- **`02_transaction_investigation.png`**: Shows investigation of an individual transaction with transaction, customer, and device information[cite: 1].
- **`03_fraud_alert_center.png`**: Shows the fraud alert interface with alert metrics, filters, and alert records[cite: 1].
- **`04_ml_risk_analysis.png`**: Shows machine learning metrics, risk distribution, probability analysis, high-risk transactions, and the confusion matrix[cite: 1].
- **`05_sql_database.png`**: Shows the MySQL Workbench database/EER design[cite: 1].
- **`06_sql_analytics.png`**: Shows SQL analytical queries and their results[cite: 1].
- **`07_ml_training.png`**: Shows the ML training process and evaluation results[cite: 1].

---

## 18. Running the Dashboard

From the project root directory, the Streamlit application can be started using:

```bash
streamlit run scripts/app.py
```[cite: 1]

If multiple Python installations are present, the Streamlit installation associated with the configured Python environment should be used[cite: 1].

The application requires:

- MySQL server to be running[cite: 1]
- `fraudlens` database to be available[cite: 1]
- Required Python packages to be installed[cite: 1]
- Project database tables and analytical views to be populated[cite: 1]

---

## 19. Dashboard Role in FraudLens

The Streamlit dashboard serves as the final presentation layer of FraudLens[cite: 1].
It combines:

```text
Database
    +
SQL Analytics
    +
Machine Learning
    +
Interactive Visualization
```[cite: 1]

into a single interface[cite: 1].

This allows the project to demonstrate an end-to-end banking fraud analytics workflow from raw transaction data through data processing, database storage, SQL analysis, machine learning prediction, and interactive investigation[cite: 1].

---

## 20. Limitations

The current dashboard has several project-level limitations:

- The dataset contains transactions from a single calendar date[cite: 1].
- ML predictions are prototype-level predictions and should not be treated as confirmed fraud[cite: 1].
- The current ML model produces a relatively high number of false positives[cite: 1].
- Dashboard results depend on the generated project dataset[cite: 1].
- The system is not connected to a live banking transaction stream[cite: 1].
- Authentication, production-grade access control, and deployment security are outside the current project scope[cite: 1].

---

## 21. Conclusion

The FraudLens Streamlit dashboard provides a unified interface for exploring fraud analytics, investigating individual transactions, reviewing fraud alerts, and analyzing machine learning predictions[cite: 1].

By connecting MySQL, SQL analytical views, Python processing, machine learning outputs, and interactive visualizations, the dashboard demonstrates how multiple data and analytics technologies can be combined into an end-to-end fraud detection and risk analytics platform[cite: 1].