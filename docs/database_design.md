# FraudLens – Database Design

## 1. Database Overview

FraudLens uses MySQL as its central relational database.

The database is named:

```text
fraudlens
```

The database is designed to organize banking information into separate related entities covering:

- Bank branches
- Customers
- Accounts
- Devices
- Bank users
- Fraud detection rules
- Banking transactions
- Login activity
- Fraud alerts
- Audit records

The relational structure allows transaction information to be connected with customer, account, device, branch, fraud, and audit information.

---

## 2. Database Architecture

The database consists of 10 primary tables:

```text
Branch
   |
   +--------------------+
   |                    |
   v                    v
Customer             BankUser
   |
   +--------------------+
   |                    |
   v                    v
Account              Device
   |
   v
BankTransaction
   |
   +--------------------+
   |                    |
   v                    v
FraudAlert            AuditLog

FraudRule
   |
   +--------------------+
   |
   v
Fraud-related analysis
```

The core transaction relationship is:

```text
Customer
    |
    v
Account
    |
    v
BankTransaction
    |
    +----> Device
    |
    +----> FraudAlert
```

---

## 3. Tables and Responsibilities

### 3.1 Branch

The `branch` table stores information about banking branches.

Purpose:

- Identify individual branches.
- Store branch location information.
- Associate customers with branches.
- Associate bank users with branches.

Key fields include:

| Field | Description |
|---|---|
| `branch_id` | Unique branch identifier |
| `branch_code` | Branch code |
| `branch_name` | Branch name |
| `city` | Branch city |
| `state` | Branch state |
| `phone` | Branch contact number |
| `manager_name` | Branch manager |

Primary Key:

```text
branch_id
```

Current record count:

```text
20
```

---

### 3.2 Customer

The `customer` table stores customer-level information.

Customers are generated from the unique source accounts identified during the data-processing stage.

The system supports customer types such as:

- Individual
- Merchant

Key fields include:

| Field | Description |
|---|---|
| `customer_id` | Unique customer identifier |
| `branch_id` | Associated branch |
| `first_name` | Customer first name |
| `last_name` | Customer last name |
| `customer_type` | Individual or Merchant |
| `dob` | Date of birth |
| `gender` | Customer gender |
| `phone` | Contact number |
| `email` | Email address |
| `aadhaar_number` | Aadhaar identifier |
| `pan_number` | PAN identifier |
| `address` | Customer address |
| `city` | Customer city |
| `state` | Customer state |
| `kyc_status` | KYC verification status |

Primary Key:

```text
customer_id
```

Foreign Key:

```text
branch_id → branch.branch_id
```

Current record count:

```text
47,801
```

---

### 3.3 Account

The `account` table represents banking accounts associated with customers.

Each generated account is associated with a customer and the same branch assigned to that customer.

Supported account types include:

- Savings
- Current
- Salary

Key fields include:

| Field | Description |
|---|---|
| `account_id` | Unique account identifier |
| `account_number` | Account number |
| `customer_id` | Account owner |
| `branch_id` | Associated branch |
| `account_type` | Type of bank account |
| `balance` | Current account balance |
| `status` | Account status |
| `opening_date` | Account opening date |

Primary Key:

```text
account_id
```

Foreign Keys:

```text
customer_id → customer.customer_id
branch_id → branch.branch_id
```

Current record count:

```text
47,801
```

The transaction investigation module uses the sender account to identify the associated customer.

The relationship is:

```text
BankTransaction.sender_account_id
            |
            v
Account.account_id
            |
            v
Customer.customer_id
```

---

### 3.4 Device

The `device` table stores information about devices used by customers.

A customer can have multiple registered devices.

Supported device categories include:

- Mobile
- Laptop
- ATM
- Tablet

Key fields include:

| Field | Description |
|---|---|
| `device_id` | Unique device identifier |
| `customer_id` | Associated customer |
| `device_name` | Device name |
| `device_type` | Device category |
| `operating_system` | Operating system |
| `ip_address` | Device IP address |
| `trusted_device` | Whether the device is trusted |
| `last_login` | Last recorded login |

Primary Key:

```text
device_id
```

Foreign Key:

```text
customer_id → customer.customer_id
```

Current record count:

```text
95,774
```

The transaction investigation page uses the device relationship to display:

- Device ID
- Device type
- Operating system
- Trusted-device status

---

### 3.5 BankUser

The `bankuser` table stores information about internal banking users.

Example roles include:

- Admin
- Fraud Analyst
- Branch Manager
- Cashier
- Auditor

Key fields include:

| Field | Description |
|---|---|
| `user_id` | Unique bank-user identifier |
| `branch_id` | Associated branch |
| `full_name` | User's full name |
| `role` | User role |
| `email` | Email address |
| `phone` | Contact number |
| `status` | User account status |

Primary Key:

```text
user_id
```

Foreign Key:

```text
branch_id → branch.branch_id
```

Current record count:

```text
50
```

---

### 3.6 FraudRule

The `fraudrule` table stores predefined fraud detection rules.

The current rule set contains six rules:

| Rule | Purpose | Risk Score |
|---|---|---:|
| High Amount Transaction | Identifies unusually high-value transactions | 90 |
| Multiple Transactions | Identifies excessive transaction frequency | 80 |
| Unknown Device | Identifies transactions from untrusted devices | 75 |
| Location Mismatch | Identifies transactions from a new city | 70 |
| Rapid Transfers | Identifies multiple outward transfers within minutes | 95 |
| Blacklisted Receiver | Identifies transactions involving a blacklisted receiver | 100 |

Key fields include:

| Field | Description |
|---|---|
| `rule_id` | Unique rule identifier |
| `rule_name` | Name of fraud rule |
| `description` | Rule description |
| `risk_score` | Risk score associated with the rule |
| `active` | Whether the rule is active |

Primary Key:

```text
rule_id
```

Current record count:

```text
6
```

---

### 3.7 BankTransaction

The `banktransaction` table is the central transaction table of FraudLens.

It stores the banking transactions used for fraud analysis and transaction investigation.

The supported transaction types are:

- `TRANSFER`
- `PAYMENT`
- `CASH_OUT`
- `CASH_IN`
- `DEBIT`

Key fields used by the application include:

| Field | Description |
|---|---|
| `transaction_id` | Unique transaction identifier |
| `reference_number` | Transaction reference |
| `sender_account_id` | Sending account |
| `receiver_account_id` | Receiving account |
| `device_id` | Device used for transaction |
| `amount` | Transaction amount |
| `transaction_type` | Transaction category |
| `channel` | Transaction channel |
| `city` | Transaction city |
| `ip_address` | Transaction IP address |
| `location` | Transaction location |
| `status` | Transaction status |
| `fraud_flag` | Existing fraud indicator |
| `fraud_score` | Existing fraud risk score |
| `remarks` | Transaction remarks |
| `transaction_time` | Transaction timestamp |

Primary Key:

```text
transaction_id
```

Foreign Keys:

```text
sender_account_id → account.account_id
receiver_account_id → account.account_id
device_id → device.device_id
```

Current record count:

```text
30,000
```

The transaction table is used by:

- SQL analytics
- Transaction investigation
- Fraud alert analysis
- Machine learning feature engineering
- Dashboard visualizations

---

### 3.8 LoginLog

The `loginlog` table stores login-related activity.

It provides information that can be used for login-risk and security analysis.

The table contains:

- Login activity
- Associated customer/device information
- IP/location information
- Login status
- Login timestamps

Primary key and foreign-key relationships are used to associate login activity with the relevant banking entities.

Current record count:

```text
30,000
```

The table contributes to the SQL login-risk analysis represented by:

```text
vw_login_risk
```

---

### 3.9 FraudAlert

The `fraudalert` table stores fraud alerts generated from transaction risk information.

Key fields used by the Fraud Alert Center include:

| Field | Description |
|---|---|
| `alert_id` | Unique alert identifier |
| `transaction_id` | Related transaction |
| `customer_id` | Related customer |
| `risk_score` | Alert risk score |
| `alert_level` | Alert severity |
| `reason` | Reason for alert |
| `status` | Alert status |
| `created_at` | Alert creation time |

Primary Key:

```text
alert_id
```

Relationships:

```text
transaction_id → banktransaction.transaction_id
customer_id → customer.customer_id
```

Current record count:

```text
84
```

The Streamlit Fraud Alert Center uses this table to display:

- Total alerts
- Critical alerts
- High alerts
- Open alerts
- Alert reasons
- Alert status
- Customer information
- Alert distribution

---

### 3.10 AuditLog

The `auditlog` table stores audit-related records associated with system activity and transactions.

Its purpose is to maintain an auditable record of relevant banking-system activity.

The table supports audit and traceability requirements within the FraudLens database.

Current record count:

```text
30,000
```

---

## 4. Primary Key Structure

The main primary keys are:

| Table | Primary Key |
|---|---|
| `branch` | `branch_id` |
| `customer` | `customer_id` |
| `account` | `account_id` |
| `device` | `device_id` |
| `bankuser` | `user_id` |
| `fraudrule` | `rule_id` |
| `banktransaction` | `transaction_id` |
| `loginlog` | Login-log identifier |
| `fraudalert` | `alert_id` |
| `auditlog` | Audit-log identifier |

Primary keys uniquely identify records within each table.

---

## 5. Foreign Key Relationships

The major relationships are:

### Branch → Customer

```text
branch.branch_id
       |
       v
customer.branch_id
```

One branch can be associated with multiple customers.

---

### Branch → Account

```text
branch.branch_id
       |
       v
account.branch_id
```

Accounts are associated with branches.

---

### Branch → BankUser

```text
branch.branch_id
       |
       v
bankuser.branch_id
```

Internal bank users are associated with branches.

---

### Customer → Account

```text
customer.customer_id
       |
       v
account.customer_id
```

A customer can own an account.

---

### Customer → Device

```text
customer.customer_id
       |
       v
device.customer_id
```

A customer can have multiple devices.

---

### Account → BankTransaction

The transaction table references accounts through both sender and receiver relationships:

```text
account.account_id
       |
       +----> banktransaction.sender_account_id
       |
       +----> banktransaction.receiver_account_id
```

This allows a transaction to identify both the sending and receiving accounts.

---

### Device → BankTransaction

```text
device.device_id
       |
       v
banktransaction.device_id
```

This associates a transaction with the device used to perform it.

---

### Customer → FraudAlert

```text
customer.customer_id
       |
       v
fraudalert.customer_id
```

Fraud alerts can be associated with customers.

---

### BankTransaction → FraudAlert

```text
banktransaction.transaction_id
       |
       v
fraudalert.transaction_id
```

A fraud alert can reference the transaction that generated the alert.

---

## 6. Entity Relationship Summary

The overall logical relationship structure is:

```text
                         +-------------+
                         |   Branch    |
                         +-------------+
                           /     |     \
                          /      |      \
                         v       v       v
                 +---------+ +---------+ +----------+
                 |Customer | | Account | | BankUser |
                 +---------+ +---------+ +----------+
                      |
                      |
               +------+------+
               |             |
               v             v
          +---------+   +-------------+
          | Device  |   | Transactions|
          +---------+   +-------------+
                              |
                    +---------+---------+
                    |                   |
                    v                   v
              +-----------+       +-----------+
              | FraudAlert|       | AuditLog  |
              +-----------+       +-----------+

              +-------------+
              | FraudRule   |
              +-------------+

              +-------------+
              |  LoginLog   |
              +-------------+
```

---

## 7. Database Record Summary

The current FraudLens database contains:

| Table | Record Count |
|---|---:|
| Branch | 20 |
| Customer | 47,801 |
| Account | 47,801 |
| Device | 95,774 |
| BankUser | 50 |
| FraudRule | 6 |
| BankTransaction | 30,000 |
| LoginLog | 30,000 |
| FraudAlert | 84 |
| AuditLog | 30,000 |

Total records across the ten tables:

```text
261,? 
```

The individual table counts above are the authoritative counts used for database validation.

---

## 8. Database Validation

After loading the generated CSV files, the database-loading process validates the expected row counts.

The validated counts are:

```text
branch             20
customer           47,801
account            47,801
device             95,774
bankuser           50
fraudrule          6
banktransaction    30,000
loginlog           30,000
fraudalert         84
auditlog           30,000
```

The database load completed successfully and all expected row counts matched.

---

## 9. Database and Dashboard Usage

The Streamlit application retrieves information from the database through SQL queries and analytical views.

For transaction investigation, the application performs the following relationship traversal:

```text
BankTransaction
      |
      | sender_account_id
      v
Account
      |
      | customer_id
      v
Customer
```

The transaction is also connected to the device:

```text
BankTransaction
      |
      | device_id
      v
Device
```

This allows the application to display transaction, customer, and device information together.

The Fraud Alert Center uses:

```text
FraudAlert
      |
      +----> Customer
      |
      +----> BankTransaction
```

This allows alerts to be displayed together with customer and transaction identifiers.

---

## 10. SQL Analytics Views

FraudLens uses SQL views to provide reusable analytical queries.

The main views are:

```text
vw_fraud_summary
vw_fraud_by_type
vw_fraud_by_channel
vw_fraud_by_location
vw_high_risk_transactions
vw_customer_fraud_risk
vw_alert_summary
vw_device_risk
vw_daily_fraud_trend
vw_login_risk
```

These views support:

- Fraud summary analysis
- Transaction-type analysis
- Channel analysis
- Location analysis
- High-risk transaction analysis
- Customer risk analysis
- Alert analysis
- Device risk analysis
- Transaction-date analysis
- Login-risk analysis

---

## 11. Database Design Principles

The FraudLens database follows several relational database principles:

### Entity Separation

Different banking entities are stored in separate tables.

### Referential Relationships

Foreign-key relationships connect related entities.

### Central Transaction Table

`banktransaction` acts as the central transaction-level table.

### Reusable Analytics

SQL views provide reusable analytical queries instead of repeatedly writing the same aggregation logic.

### Traceability

Fraud alerts and audit records provide additional information for investigating suspicious activity and system activity.

### Integration with Machine Learning

The transaction database provides the structured data required for ML feature engineering and fraud-risk prediction.

---

## 12. Database Design Summary

The FraudLens database provides a structured relational foundation for the complete fraud analytics platform.

The design connects:

```text
Branches
    +
Customers
    +
Accounts
    +
Devices
    +
Transactions
    +
Fraud Rules
    +
Fraud Alerts
    +
Login Logs
    +
Audit Logs
    +
Bank Users
```

This structure allows FraudLens to combine relational database management, SQL analytics, transaction investigation, fraud alerts, and machine learning within a single system.