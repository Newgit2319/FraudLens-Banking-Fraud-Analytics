import random
import uuid
from datetime import timedelta

import pandas as pd
from faker import Faker
from tqdm import tqdm

from config import INPUT_FILE, OUTPUT_DIR


# ============================================================
# CONFIGURATION
# ============================================================

random.seed(42)
Faker.seed(42)

fake = Faker("en_IN")


# ============================================================
# LOAD DATA
# ============================================================

print("\nLoading FraudLens datasets...")

transactions = pd.read_csv(INPUT_FILE)

mapping = pd.read_csv(
    OUTPUT_DIR / "Mapping.csv"
)

customers = pd.read_csv(
    OUTPUT_DIR / "Customer.csv"
)

accounts = pd.read_csv(
    OUTPUT_DIR / "Account.csv"
)

devices = pd.read_csv(
    OUTPUT_DIR / "Device.csv"
)

fraud_rules = pd.read_csv(
    OUTPUT_DIR / "FraudRule.csv"
)

bank_users = pd.read_csv(
    OUTPUT_DIR / "BankUser.csv"
)


print(f"Transactions : {len(transactions):,}")
print(f"Customers    : {len(customers):,}")
print(f"Accounts     : {len(accounts):,}")
print(f"Devices      : {len(devices):,}")


# ============================================================
# LOOKUPS
# ============================================================

print("\nBuilding lookup dictionaries...")


# PaySim ID → Account ID
account_lookup = dict(
    zip(
        mapping["paysim_id"],
        mapping["account_id"]
    )
)


# PaySim ID → Customer ID
customer_lookup = dict(
    zip(
        mapping["paysim_id"],
        mapping["customer_id"]
    )
)


# Customer → Branch
customer_branch_lookup = dict(
    zip(
        customers["customer_id"],
        customers["branch_id"]
    )
)


# Customer → City
customer_city_lookup = dict(
    zip(
        customers["customer_id"],
        customers["city"]
    )
)


# Customer → State
customer_state_lookup = dict(
    zip(
        customers["customer_id"],
        customers["state"]
    )
)


# Customer → Devices
customer_devices = {}

for row in devices.itertuples(index=False):

    customer_devices.setdefault(
        row.customer_id,
        []
    ).append(row.device_id)


# Device → row
device_lookup = {
    row.device_id: row
    for row in devices.itertuples(index=False)
}


# ============================================================
# VALIDATION
# ============================================================

print("\nValidating relationships...")

missing_senders = 0
missing_receivers = 0
missing_devices = 0


for row in transactions.itertuples(index=False):

    if row.nameOrig not in account_lookup:
        missing_senders += 1

    if row.nameDest not in account_lookup:
        missing_receivers += 1


for customer_id in customer_branch_lookup:

    if customer_id not in customer_devices:
        missing_devices += 1


print(
    f"Missing sender mappings   : {missing_senders}"
)

print(
    f"Missing receiver mappings : {missing_receivers}"
)

print(
    f"Customers without devices : {missing_devices}"
)


if missing_senders > 0:

    raise ValueError(
        "Sender mapping validation failed."
    )


if missing_receivers > 0:

    raise ValueError(
        "Receiver mapping validation failed."
    )


if missing_devices > 0:

    raise ValueError(
        "Device mapping validation failed."
    )


# ============================================================
# OUTPUT COLLECTIONS
# ============================================================

bank_transactions = []
login_logs = []
fraud_alerts = []
audit_logs = []


transaction_id = 1
login_id = 1
alert_id = 1
audit_id = 1


# ============================================================
# VALID MYSQL ENUM VALUES
# ============================================================

channels = [
    "UPI",
    "ATM",
    "Internet Banking",
    "Branch"
]


statuses = [
    "Success",
    "Success",
    "Success",
    "Pending",
    "Failed"
]


# ============================================================
# TRANSACTION PROCESSING
# ============================================================

print("\nGenerating transaction datasets...")


for tx in tqdm(
    transactions.itertuples(index=False),
    total=len(transactions),
    desc="Transactions"
):

    # --------------------------------------------------------
    # Resolve PaySim accounts
    # --------------------------------------------------------

    sender_account_id = account_lookup[
        tx.nameOrig
    ]

    receiver_account_id = account_lookup[
        tx.nameDest
    ]


    # --------------------------------------------------------
    # Resolve sender customer
    # --------------------------------------------------------

    sender_customer_id = customer_lookup[
        tx.nameOrig
    ]


    # --------------------------------------------------------
    # Resolve customer information
    # --------------------------------------------------------

    branch_id = customer_branch_lookup[
        sender_customer_id
    ]

    city = customer_city_lookup[
        sender_customer_id
    ]

    state = customer_state_lookup[
        sender_customer_id
    ]


    # --------------------------------------------------------
    # Select one of customer's actual devices
    # --------------------------------------------------------

    available_devices = customer_devices[
        sender_customer_id
    ]

    selected_device_id = random.choice(
        available_devices
    )

    selected_device = device_lookup[
        selected_device_id
    ]


    # --------------------------------------------------------
    # Transaction metadata
    # --------------------------------------------------------

    channel = random.choice(
        channels
    )

    status = random.choice(
        statuses
    )


    # --------------------------------------------------------
    # Transaction timestamp
    # --------------------------------------------------------

    transaction_time = (
        pd.Timestamp("2026-01-01")
        + timedelta(
            hours=int(tx.step)
        )
    )


    # --------------------------------------------------------
    # Fraud information
    # --------------------------------------------------------

    fraud_flag = int(
        tx.isFraud
    )

    flagged_fraud = int(
        tx.isFlaggedFraud
    )


    # --------------------------------------------------------
    # Risk score
    # --------------------------------------------------------

    if fraud_flag == 1:

        fraud_score = random.randint(
            80,
            100
        )

        alert_level = "High"

    elif flagged_fraud == 1:

        fraud_score = random.randint(
            70,
            85
        )

        alert_level = "High"

    else:

        fraud_score = random.randint(
            1,
            50
        )

        if fraud_score >= 40:

            alert_level = "Medium"

        else:

            alert_level = "Low"


    # --------------------------------------------------------
    # Location
    # --------------------------------------------------------

    location = f"{city}, {state}"


    # --------------------------------------------------------
    # Reference number
    # --------------------------------------------------------

    reference_number = (
        "FLX-"
        + uuid.uuid4()
        .hex[:12]
        .upper()
    )


    # ========================================================
    # BANK TRANSACTION
    # ========================================================

    bank_transactions.append({

        "transaction_id":
            transaction_id,

        "reference_number":
            reference_number,

        "sender_account_id":
            sender_account_id,

        "receiver_account_id":
            receiver_account_id,

        "device_id":
            selected_device_id,

        "amount":
            round(
                float(tx.amount),
                2
            ),

        "transaction_type":
            tx.type,

        "channel":
            channel,

        "city":
            city,

        "ip_address":
            selected_device.ip_address,

        "location":
            location,

        "status":
            status,

        "fraud_flag":
            fraud_flag,

        "fraud_score":
            fraud_score,

        "remarks":
            (
                "Fraud transaction detected"
                if fraud_flag == 1
                else "Normal transaction"
            ),

        "created_by":
            "FraudLens ETL",

        "transaction_time":
            transaction_time
    })


    # ========================================================
    # LOGIN LOG
    # ========================================================

    login_logs.append({

        "login_id":
            login_id,

        "customer_id":
            sender_customer_id,

        "device_id":
            selected_device_id,

        "ip_address":
            selected_device.ip_address,

        "city":
            city,

        "login_time":
            transaction_time
            - timedelta(
                minutes=random.randint(
                    1,
                    30
                )
            ),

        "login_status":
            "Success"
    })


    login_id += 1


    # ========================================================
    # FRAUD ALERT
    # ========================================================

    if fraud_flag == 1 or flagged_fraud == 1:

        # Select appropriate fraud rule
        if float(tx.amount) >= 200000:

            rule_id = 1
            reason = (
                "High-value transaction"
            )

        elif not bool(
            selected_device.trusted_device
        ):

            rule_id = 3
            reason = (
                "Transaction from "
                "untrusted device"
            )

        else:

            rule_id = 5
            reason = (
                "Suspicious transaction "
                "pattern detected"
            )


        # Pick an existing BankUser
        assigned_to = random.choice(
            bank_users["user_id"].tolist()
        )


        fraud_alerts.append({

            "alert_id":
                alert_id,

            "transaction_id":
                transaction_id,

            "rule_id":
                rule_id,

            "customer_id":
                sender_customer_id,

            "assigned_to":
                assigned_to,

            "risk_score":
                fraud_score,

            "alert_level":
                alert_level,

            "reason":
                reason,

            "status":
                "Open"
        })


        alert_id += 1


    # ========================================================
    # AUDIT LOG
    # ========================================================

    audit_logs.append({

        "audit_id":
            audit_id,

        "table_name":
            "BankTransaction",

        "record_id":
            transaction_id,

        "action_type":
            "INSERT",

        "changed_by":
            "FraudLens ETL",

        "old_value":
            None,

        "new_value":
            (
                f"Transaction {reference_number} "
                f"imported"
            )
    })


    audit_id += 1

    transaction_id += 1


# ============================================================
# CREATE DATAFRAMES
# ============================================================

bank_transaction_df = pd.DataFrame(
    bank_transactions
)

login_df = pd.DataFrame(
    login_logs
)

fraud_alert_df = pd.DataFrame(
    fraud_alerts
)

audit_df = pd.DataFrame(
    audit_logs
)


# ============================================================
# SAVE FILES
# ============================================================

bank_transaction_df.to_csv(
    OUTPUT_DIR / "BankTransaction.csv",
    index=False
)

login_df.to_csv(
    OUTPUT_DIR / "LoginLog.csv",
    index=False
)

fraud_alert_df.to_csv(
    OUTPUT_DIR / "FraudAlert.csv",
    index=False
)

audit_df.to_csv(
    OUTPUT_DIR / "AuditLog.csv",
    index=False
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n")
print("=" * 60)
print("TRANSACTION ETL COMPLETED")
print("=" * 60)

print(
    f"Bank Transactions : "
    f"{len(bank_transaction_df):,}"
)

print(
    f"Login Logs        : "
    f"{len(login_df):,}"
)

print(
    f"Fraud Alerts      : "
    f"{len(fraud_alert_df):,}"
)

print(
    f"Audit Logs        : "
    f"{len(audit_df):,}"
)

print(
    f"Known fraud cases : "
    f"{bank_transaction_df['fraud_flag'].sum():,}"
)

print("\nOutput files generated successfully.")