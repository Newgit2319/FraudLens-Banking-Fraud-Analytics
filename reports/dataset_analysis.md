# FraudLens – Dataset Analysis Report

## 1. Introduction

The FraudLens project uses a PaySim-based banking transaction dataset as the foundation for fraud detection and risk analytics.

The original transaction data is processed and enriched using Python to create additional banking entities such as customers, accounts, branches, devices, bank users, fraud rules, login logs, fraud alerts, and audit logs.

The final transaction dataset used by the FraudLens system contains:

```text
Total transactions: 30,000

The dataset is used for:

- Exploratory data analysis[cite: 1]
- SQL-based fraud analytics[cite: 1]
- Fraud alert generation[cite: 1]
- Machine learning model training[cite: 1]
- Interactive dashboard visualization[cite: 1]

---

## 2. Dataset Source

The transaction data is based on the PaySim synthetic financial dataset[cite: 1].
The source data represents simulated financial transactions and provides transaction-level information suitable for demonstrating fraud detection techniques[cite: 1].
FraudLens extends the transaction data with additional synthetic banking attributes to create a more complete banking analytics environment[cite: 1].

---

## 3. Dataset Structure

The main transaction dataset contains information related to:

- Transaction amount[cite: 1]
- Transaction type[cite: 1]
- Fraud status[cite: 1]
- Fraud score[cite: 1]
- Transaction channel[cite: 1]
- Location[cite: 1]
- Device information[cite: 1]
- Operating system[cite: 1]
- Trusted device status[cite: 1]
- Transaction timestamp[cite: 1]
- Sender activity[cite: 1]
- Device activity[cite: 1]
- Account-pair activity[cite: 1]

The enriched FraudLens database organizes these details across multiple relational tables[cite: 1].

---

## 4. Database-Level Dataset Distribution

The generated FraudLens database contains the following records:

| Table | Records |
| :--- | :--- |
| **Branch** | 20[cite: 1] |
| **Customer** | 47,801[cite: 1] |
| **Account** | 47,801[cite: 1] |
| **Device** | 95,774[cite: 1] |
| **BankUser** | 50[cite: 1] |
| **FraudRule** | 6[cite: 1] |
| **BankTransaction** | 30,000[cite: 1] |
| **LoginLog** | 30,000[cite: 1] |
| **FraudAlert** | 84[cite: 1] |
| **AuditLog** | 30,000[cite: 1] |

The difference between the number of customers/accounts/devices and transactions is expected because the database represents supporting banking entities in addition to the transaction records[cite: 1].

---

## 5. Transaction Summary

The FraudLens database contains:

- **Total transactions:** 30,000[cite: 1]
- **Total transaction value:** ₹412,845,080.25[cite: 1]
- **Fraudulent transactions:** 84[cite: 1]
- **Fraud rate:** 0.28%[cite: 1]
- **Total fraud amount:** ₹4,942,953.62[cite: 1]
- **Average fraud score:** 25.83[cite: 1]

The fraud rate is calculated using the number of transactions identified as fraudulent relative to the total number of transactions[cite: 1].
The relatively small proportion of fraud cases makes fraud detection an imbalanced classification problem[cite: 1].

---

## 6. Transaction Types

The transaction dataset uses the following transaction categories:

- `TRANSFER`[cite: 1]
- `PAYMENT`[cite: 1]
- `CASH_OUT`[cite: 1]
- `CASH_IN`[cite: 1]
- `DEBIT`[cite: 1]

These categories allow fraud activity to be analyzed according to the type of banking operation being performed[cite: 1].
SQL analytics in the project provide fraud counts and transaction distributions by transaction type[cite: 1].

---

## 7. Transaction Channels

Transactions are also associated with banking channels[cite: 1].
Channel information provides additional context for fraud analysis and allows the project to examine whether fraud activity differs across transaction channels[cite: 1].
The `vw_fraud_by_channel` SQL analytical view is used by the dashboard to summarize fraud activity by channel[cite: 1].

---

## 8. Location Analysis

The enriched dataset contains transaction location information[cite: 1].
The FraudLens SQL layer uses location information to calculate:

- Transaction count[cite: 1]
- Fraud count[cite: 1]
- Fraud rate[cite: 1]
- Fraud amount[cite: 1]

The dashboard presents this information through the location analysis section[cite: 1].
Location-level analysis can help identify areas with relatively higher concentrations of suspicious transaction activity[cite: 1].

---

## 9. Fraud Distribution

The database contains:

- **Total transactions:** 30,000[cite: 1]
- **Fraud transactions:** 84[cite: 1]
- **Normal transactions:** 29,916[cite: 1]

The resulting fraud rate is: **0.28%**[cite: 1]

This indicates that fraudulent transactions represent a small portion of the complete transaction population[cite: 1].
The class imbalance is important for the machine learning component because a model can achieve high overall accuracy while still performing poorly on the minority fraud class[cite: 1].

---

## 10. Fraud Amount Analysis

- **Total value associated with fraudulent transactions:** ₹4,942,953.62[cite: 1]
- **Total transaction value across the dataset:** ₹412,845,080.25[cite: 1]

This allows FraudLens to analyze fraud not only by transaction count but also by financial value[cite: 1].
Amount-based analysis is particularly useful because a small number of fraudulent transactions may represent a substantial financial value[cite: 1].

---

## 11. Date Analysis

An important characteristic of the current dataset is that all 30,000 transactions occur on the same calendar date: **2026-01-01**[cite: 1].

The database contains:

| Date | Transactions | Fraud Cases |
| :--- | :--- | :--- |
| **2026-01-01** | 30,000 | 84 |

Therefore, the project does not currently contain a genuine multi-day transaction history[cite: 1].
For this reason, the dashboard presents a Transaction Date Summary rather than implying a multi-day fraud trend[cite: 1].
This is an important data limitation and should be considered when interpreting temporal analysis[cite: 1].

---

## 12. Missing Values and Data Quality

The generated FraudLens dataset was designed to provide consistent relational records across the database[cite: 1].
Important data-quality considerations include:

- Transaction records are populated for the 30,000 source transactions[cite: 1].
- Customer and account relationships are maintained[cite: 1].
- Customer branch and account branch relationships are kept consistent during generation[cite: 1].
- Device records are generated and associated with transaction activity[cite: 1].
- Fraud alerts are associated with fraudulent transactions[cite: 1].
- Login logs and audit logs are generated for the transaction dataset[cite: 1].
- Database loading was validated against expected record counts[cite: 1].

The final database load completed successfully and all expected table counts matched the generated data[cite: 1].

---

## 13. Relational Consistency

The ETL process maintains relationships between the generated entities[cite: 1].
For example:

```text
Customer
   |
   v
Account
   |
   v
BankTransaction
   |
   +---- Device
   |
   +---- FraudAlert
   |
   +---- AuditLog
```[cite: 1]

Customer and account branch assignments are also kept consistent through the generated customer-branch mapping[cite: 1].
This relational consistency allows the SQL layer to join multiple tables for analytical queries[cite: 1].

---

## 14. Device Data

The generated database contains **95,774 device records**[cite: 1].

Device information includes attributes such as:

- Device type[cite: 1]
- Operating system[cite: 1]
- Trusted-device status[cite: 1]

Device-level information is used by the SQL analytics layer and ML feature engineering[cite: 1].
The project includes a `vw_device_risk` analytical view for device-level risk analysis[cite: 1].

---

## 15. Customer and Account Data

The database contains:

- **47,801 customers**[cite: 1]
- **47,801 accounts**[cite: 1]

Customer information provides additional context for transaction analysis[cite: 1].
Account information connects customers with their banking transactions[cite: 1].

These relationships allow FraudLens to perform customer-level fraud analysis through the `vw_customer_fraud_risk` SQL analytical view[cite: 1].

---

## 16. Fraud Alerts

The database contains **84 fraud alerts** corresponding to the generated fraudulent transactions[cite: 1].

### Current Alert Distribution
- **High:** 84[cite: 1]
- **Critical:** 0[cite: 1]

### Current Alert Status
- **Open:** 84[cite: 1]

The uniform alert distribution reflects the current generated fraud-alert dataset[cite: 1].

---

## 17. Login and Audit Records

The database contains:

- **LoginLog records:** 30,000[cite: 1]
- **AuditLog records:** 30,000[cite: 1]

These records provide additional activity and audit information for the FraudLens environment[cite: 1].
The login information is used by the SQL analytics layer to support login-risk analysis[cite: 1].
Audit records provide a record of transaction-related activity for analysis and traceability[cite: 1].

---

## 18. Important Dataset Patterns

Several important patterns can be identified from the dataset:

- **Low Fraud Frequency:** Only 84 of the 30,000 transactions are marked as fraudulent, producing a fraud rate of 0.28%[cite: 1].
- **Financial Impact:** The fraudulent transactions represent approximately ₹4.94 million in transaction value[cite: 1].
- **Single-Date Dataset:** All transactions occur on 2026-01-01, limiting long-term temporal analysis[cite: 1].
- **Relational Enrichment:** The transaction dataset is enriched with customers, accounts, branches, devices, alerts, login logs, and audit records[cite: 1].
- **Class Imbalance:** The small number of fraud cases compared with normal transactions creates a highly imbalanced classification problem for machine learning[cite: 1].

---

## 19. Machine Learning Relevance

The dataset provides features for machine learning fraud detection[cite: 1].
The ML pipeline uses:

- Transaction amount[cite: 1]
- Log-transformed amount[cite: 1]
- Transaction type[cite: 1]
- Channel[cite: 1]
- City[cite: 1]
- Device type[cite: 1]
- Operating system[cite: 1]
- Trusted device[cite: 1]
- Transaction hour[cite: 1]
- Day of week[cite: 1]
- Weekend indicator[cite: 1]
- Night-time indicator[cite: 1]
- High-value indicator[cite: 1]
- Sender transaction count[cite: 1]
- Sender average amount[cite: 1]
- Device transaction count[cite: 1]
- Account-pair frequency[cite: 1]

The target variable is:

`fraud_flag`[cite: 1]

The model does not use `fraud_flag` or the existing `fraud_score` as input features, helping prevent direct target leakage[cite: 1].

---

## 20. Data Quality Assessment

Overall, the generated dataset is structurally suitable for demonstrating the FraudLens workflow[cite: 1].

The main observations are:

- All expected database tables were successfully populated[cite: 1].
- Expected row counts were validated[cite: 1].
- Relationships between generated banking entities were maintained[cite: 1].
- Fraud records are available for SQL and ML analysis[cite: 1].
- The dataset contains a substantial class imbalance[cite: 1].
- The transaction data is restricted to a single calendar date[cite: 1].
- The enriched banking attributes are synthetic/generated for the project environment[cite: 1].

These characteristics should be considered when interpreting project results[cite: 1].

---

## 21. Limitations

The dataset has several limitations:

- **Synthetic Nature:** The PaySim source is a simulated financial dataset, and several additional banking attributes are generated for the project[cite: 1].
- **Limited Transaction Volume:** The current ML and analytics workflow uses 30,000 transaction records[cite: 1].
- **Single-Date Coverage:** All transactions occur on a single date, preventing meaningful long-term temporal trend analysis[cite: 1].
- **Fraud Class Imbalance:** Fraudulent transactions represent only 0.28% of the transaction population[cite: 1].
- **No Real-Time Data:** The dataset is static and does not represent a live banking transaction stream[cite: 1].

---

## 22. Conclusion

The FraudLens dataset provides a structured environment for demonstrating banking fraud detection and risk analytics[cite: 1].

It contains 30,000 transaction records, 84 fraudulent transactions, and multiple enriched banking entities including customers, accounts, devices, branches, alerts, login records, and audit records[cite: 1].

The dataset supports both SQL-based analytics and machine learning[cite: 1]. Its main analytical limitations are the highly imbalanced fraud class and the fact that all transactions occur on a single calendar date[cite: 1].

Despite these limitations, the dataset provides the required foundation for demonstrating the complete FraudLens pipeline from data preparation and relational storage to fraud analysis, machine learning, and dashboard visualization[cite: 1].