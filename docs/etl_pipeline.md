# FraudLens – ETL Pipeline

## 1. Overview

FraudLens uses a Python-based ETL pipeline to transform the PaySim-based transaction dataset into a structured banking dataset suitable for MySQL, SQL analytics, fraud investigation, and machine learning.

The ETL process consists of:

```text
PaySim Dataset
      |
      v
Load Source Data
      |
      v
Extract Unique Accounts
      |
      v
Create Account Mapping
      |
      v
Generate Banking Entities
      |
      v
Generate Transactions
      |
      v
Generate Fraud Records
      |
      v
Export CSV Files
      |
      v
Load into MySQL
      |
      v
Validate Database
```

---

## 2. Source Dataset

The project uses a PaySim-based transaction dataset as the source transaction data.

The source dataset contains transaction-level information that is transformed into the banking entities required by FraudLens.

The source identifiers are not directly used as the final banking identifiers. Instead, the ETL process creates a mapping between the source identifiers and the generated customer and account identifiers.

---

## 3. ETL Technologies

The data-processing pipeline uses:

| Technology | Purpose |
|---|---|
| Python | ETL and data generation |
| Pandas | Data loading, transformation and CSV processing |
| Faker | Generation of synthetic banking/customer information |
| tqdm | Progress monitoring during large data-generation operations |
| MySQL | Target relational database |
| CSV | Intermediate data-exchange format |

---

## 4. Configuration

The ETL pipeline uses a centralized configuration file.

The configuration defines:

```text
BASE_DIR
DATASET_DIR
OUTPUT_DIR
INPUT_FILE
```

The source dataset is read from the `dataset` directory.

Generated CSV files are written to the `output` directory.

The configured input file is:

```text
FraudLens_30000.csv
```

---

## 5. Step 1 – Load Dataset

The first ETL operation loads the source transaction dataset using Pandas.

Conceptually:

```python
self.transactions = pd.read_csv(INPUT_FILE)
```

The pipeline then reports the number of source records loaded.

For the current FraudLens dataset:

```text
30,000 transaction records
```

---

## 6. Step 2 – Extract Unique Accounts

The source transaction data contains sender and receiver identifiers.

The pipeline extracts:

```text
nameOrig
nameDest
```

The sender and receiver identifiers are combined to identify the complete set of accounts participating in the transaction data.

Conceptually:

```text
Sender Accounts
      +
Receiver Accounts
      |
      v
Unique Account Set
```

This creates the foundation for generating the Customer and Account entities.

---

## 7. Step 3 – Create Account Mapping

Each unique source account is mapped to generated FraudLens identifiers.

The mapping contains:

| Field | Purpose |
|---|---|
| `paysim_id` | Original PaySim identifier |
| `customer_id` | Generated customer identifier |
| `account_id` | Generated banking account identifier |
| `customer_type` | Customer classification |

The generated customer and account IDs are maintained separately from the source PaySim identifiers.

The mapping is stored in:

```text
output/Mapping.csv
```

---

## 8. Step 4 – Generate Branch Data

FraudLens generates a structured set of banking branches.

The current dataset contains:

```text
20 branches
```

Branches contain information such as:

- Branch ID
- Branch code
- Branch name
- City
- State
- Phone
- Manager name

The generated data is saved as:

```text
output/Branch.csv
```

---

## 9. Step 5 – Generate Customer Data

Customer records are generated from the unique account mapping.

The ETL process assigns each customer:

- Customer ID
- Branch
- Name
- Customer type
- Date of birth
- Gender
- Phone
- Email
- Address
- City
- State
- KYC status

Synthetic customer information is generated using Faker.

The customer branch assignment is stored during customer generation.

This ensures that the corresponding account can use the same branch.

The generated data is saved as:

```text
output/Customer.csv
```

Current record count:

```text
47,801 customers
```

---

## 10. Step 6 – Generate Account Data

Account records are generated from the account mapping.

Each account receives:

- Account ID
- Account number
- Customer ID
- Branch ID
- Account type
- Balance
- Status
- Opening date

Supported account types include:

```text
Savings
Current
Salary
```

Account statuses include:

```text
Active
Frozen
Closed
```

The account uses the same branch assigned to its customer.

This maintains the relationship:

```text
Customer
    |
    | customer_id
    v
Account
    |
    | branch_id
    v
Branch
```

The generated data is saved as:

```text
output/Account.csv
```

Current record count:

```text
47,801 accounts
```

---

## 11. Step 7 – Generate Device Data

The ETL pipeline generates one or more devices for customers.

Supported device types include:

```text
Mobile
Laptop
ATM
Tablet
```

Operating systems are generated according to the device category.

Examples include:

```text
Android
iOS
Windows
Ubuntu
macOS
Embedded Linux
iPadOS
```

Each device contains information such as:

- Device ID
- Customer ID
- Device name
- Device type
- Operating system
- IP address
- Trusted-device status
- Last login

The generated data is saved as:

```text
output/Device.csv
```

Current record count:

```text
95,774 devices
```

---

## 12. Step 8 – Generate Bank Users

FraudLens also generates internal banking users.

The current dataset contains:

```text
50 bank users
```

Example roles include:

```text
Admin
Fraud Analyst
Branch Manager
Cashier
Auditor
```

Each bank user is associated with a branch.

The generated data is saved as:

```text
output/BankUser.csv
```

---

## 13. Step 9 – Generate Fraud Rules

The ETL pipeline generates six fraud rules.

The current rules are:

```text
1. High Amount Transaction
2. Multiple Transactions
3. Unknown Device
4. Location Mismatch
5. Rapid Transfers
6. Blacklisted Receiver
```

Each rule contains:

- Rule ID
- Rule name
- Description
- Risk score
- Active status

The generated data is saved as:

```text
output/FraudRule.csv
```

Current record count:

```text
6 fraud rules
```

---

## 14. Step 10 – Generate Banking Transactions

The source PaySim transactions are transformed into FraudLens banking transactions.

The transaction model includes:

```text
Transaction ID
Reference Number
Sender Account
Receiver Account
Device
Amount
Transaction Type
Channel
City
IP Address
Location
Status
Fraud Flag
Fraud Score
Remarks
Transaction Time
```

The transaction types supported by the database are:

```text
TRANSFER
PAYMENT
CASH_OUT
CASH_IN
DEBIT
```

The generated transaction records are stored in:

```text
output/BankTransaction.csv
```

Current record count:

```text
30,000 transactions
```

---

## 15. Step 11 – Generate Login Logs

Login activity is represented through the `LoginLog` entity.

The generated login records provide information that can be used for security and login-risk analysis.

The records are exported to:

```text
output/LoginLog.csv
```

Current record count:

```text
30,000 login records
```

---

## 16. Step 12 – Generate Fraud Alerts

Fraud-related transaction information is used to create fraud alert records.

Each alert can contain:

- Alert ID
- Transaction ID
- Customer ID
- Risk score
- Alert level
- Reason
- Status
- Creation timestamp

The generated records are saved as:

```text
output/FraudAlert.csv
```

Current record count:

```text
84 fraud alerts
```

---

## 17. Step 13 – Generate Audit Logs

Audit records are generated to maintain traceability of relevant system activity.

The records are exported as:

```text
output/AuditLog.csv
```

Current record count:

```text
30,000 audit records
```

---

## 18. Generated CSV Files

The ETL pipeline produces the following major CSV files:

```text
Mapping.csv
Branch.csv
Customer.csv
Account.csv
Device.csv
BankUser.csv
FraudRule.csv
BankTransaction.csv
LoginLog.csv
FraudAlert.csv
AuditLog.csv
```

These files form the intermediate layer between Python processing and the MySQL database.

---

## 19. ETL Data Flow

The complete transformation can be represented as:

```text
                     PaySim Dataset
                           |
                           v
                  +------------------+
                  | Load with Pandas |
                  +------------------+
                           |
                           v
                Extract Unique Accounts
                           |
                           v
                   Account Mapping
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
          Branch       Customer       Account
                           |
                           v
                        Device
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
       BankTransaction  LoginLog     FraudAlert
             |
             v
          AuditLog
             |
             v
          CSV Files
             |
             v
        MySQL Database
```

---

## 20. Loading CSV Files into MySQL

After CSV generation, the database-loading script imports the generated data into MySQL.

The target database is:

```text
fraudlens
```

The loader performs the following operations:

1. Connect to MySQL.
2. Select the `fraudlens` database.
3. Clear existing table data in dependency-safe order.
4. Load generated CSV files.
5. Commit the inserted records.
6. Validate the number of records in each table.
7. Report the database-load status.

---

## 21. Dependency-Safe Loading

Because the database contains foreign-key relationships, tables cannot always be loaded in an arbitrary order.

Parent entities are loaded before dependent entities.

A simplified loading order is:

```text
Branch
   |
   +--> Customer
   |       |
   |       +--> Device
   |
   +--> Account
           |
           v
     BankTransaction
           |
           v
      FraudAlert

BankUser
FraudRule
LoginLog
AuditLog
```

The database-loading process also clears existing data in reverse dependency order before reloading the generated dataset.

---

## 22. Data Validation

After loading, the pipeline validates the expected record counts.

The validated counts are:

| Table | Records |
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

The final database-load validation reported:

```text
DATABASE LOAD SUCCESSFUL
All expected row counts match.
```

---

## 23. Data Quality and Consistency Considerations

The ETL process maintains several important relationships during data generation.

### Customer–Account Branch Consistency

The branch assigned to a customer is reused when generating that customer's account.

Therefore:

```text
Customer.branch_id
=
Account.branch_id
```

for the corresponding generated customer/account relationship.

### Source-to-Database Mapping

PaySim identifiers are retained in the mapping layer while FraudLens uses generated customer and account identifiers.

This separates source identifiers from the relational database identifiers.

### Referential Relationships

Generated IDs are used to connect:

```text
Customer → Account
Customer → Device
Account → Transaction
Device → Transaction
Customer → FraudAlert
Transaction → FraudAlert
```

---

## 24. ETL Output Structure

The project separates source data, generated data, and processing scripts.

```text
FraudLens-Banking-Fraud-Analytics/
│
├── dataset/
│   └── FraudLens_30000.csv
│
├── output/
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
└── scripts/
    ├── generate_dataset.py
    └── load_database.py
```

---

## 25. ETL Summary

The FraudLens ETL pipeline converts a PaySim-based transaction dataset into a structured banking environment.

The pipeline performs:

```text
Extraction
    ↓
Source-account identification
    ↓
Identifier mapping
    ↓
Entity generation
    ↓
Transaction transformation
    ↓
Fraud and audit record generation
    ↓
CSV export
    ↓
MySQL loading
    ↓
Row-count validation
```

This ETL layer provides the structured data foundation used by the SQL analytics, machine learning, and Streamlit presentation layers.