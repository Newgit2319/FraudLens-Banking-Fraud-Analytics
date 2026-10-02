import getpass
import sys

import mysql.connector
import pandas as pd

from config import OUTPUT_DIR


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

HOST = "localhost"
DATABASE = "fraudlens"
USER = "root"


# ============================================================
# CSV LOADING HELPER
# ============================================================

def load_csv(filename):
    path = OUTPUT_DIR / filename

    print(f"Loading {filename}...")

    df = pd.read_csv(path)

    print(f"  Rows: {len(df):,}")

    return df


# ============================================================
# INSERT HELPER
# ============================================================

def insert_dataframe(cursor, table, columns, dataframe):

    column_string = ", ".join(
        f"`{column}`"
        for column in columns
    )

    placeholders = ", ".join(
        ["%s"] * len(columns)
    )

    query = f"""
        INSERT INTO `{table}`
        ({column_string})
        VALUES ({placeholders})
    """

    values = []

    for row in dataframe[columns].itertuples(
        index=False,
        name=None
    ):

        cleaned = []

        for value in row:

            if pd.isna(value):
                cleaned.append(None)

            else:
                cleaned.append(value)

        values.append(tuple(cleaned))

    cursor.executemany(
        query,
        values
    )

    print(
        f"  Inserted {len(values):,} rows into {table}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 65)
    print("FRAUDLENS DATABASE LOADER")
    print("=" * 65)

    password = getpass.getpass(
        "Enter MySQL root password: "
    )

    # --------------------------------------------------------
    # Connect
    # --------------------------------------------------------

    try:

        connection = mysql.connector.connect(

            host=HOST,

            user=USER,

            password=password,

            database=DATABASE,

            autocommit=False
        )

        cursor = connection.cursor()

        print("\nConnected to MySQL successfully.")

    except mysql.connector.Error as error:

        print("\nMySQL connection failed:")
        print(error)

        sys.exit(1)


    try:

        # ====================================================
        # DISABLE FOREIGN KEY CHECKS
        # ====================================================

        cursor.execute(
            "SET FOREIGN_KEY_CHECKS = 0"
        )


        # ====================================================
        # CLEAR EXISTING DATA
        # ====================================================

        print("\nClearing existing/sample data...")

        tables = [

            "auditlog",

            "fraudalert",

            "loginlog",

            "banktransaction",

            "device",

            "fraudrule",

            "bankuser",

            "account",

            "customer",

            "branch"

        ]

        for table in tables:

            cursor.execute(
                f"TRUNCATE TABLE `{table}`"
            )

            print(
                f"  Cleared {table}"
            )


        # ====================================================
        # LOAD CSV FILES
        # ====================================================

        print("\nLoading master data...")


        # ----------------------------------------------------
        # Branch
        # ----------------------------------------------------

        branch_df = load_csv(
            "Branch.csv"
        )

        insert_dataframe(

            cursor,

            "branch",

            [
                "branch_id",
                "branch_code",
                "branch_name",
                "city",
                "state",
                "phone",
                "manager_name"
            ],

            branch_df
        )


        # ----------------------------------------------------
        # Customer
        # ----------------------------------------------------

        customer_df = load_csv(
            "Customer.csv"
        )

        insert_dataframe(

            cursor,

            "customer",

            [
                "customer_id",
                "branch_id",
                "first_name",
                "last_name",
                "dob",
                "gender",
                "phone",
                "email",
                "aadhaar_number",
                "pan_number",
                "address",
                "city",
                "state",
                "kyc_status"
            ],

            customer_df
        )


        # ----------------------------------------------------
        # Account
        # ----------------------------------------------------

        account_df = load_csv(
            "Account.csv"
        )

        insert_dataframe(

            cursor,

            "account",

            [
                "account_id",
                "account_number",
                "customer_id",
                "branch_id",
                "account_type",
                "balance",
                "status",
                "opening_date"
            ],

            account_df
        )


        # ----------------------------------------------------
        # Device
        # ----------------------------------------------------

        device_df = load_csv(
            "Device.csv"
        )

        insert_dataframe(

            cursor,

            "device",

            [
                "device_id",
                "customer_id",
                "device_name",
                "device_type",
                "operating_system",
                "ip_address",
                "trusted_device",
                "last_login"
            ],

            device_df
        )


        # ----------------------------------------------------
        # Bank User
        # ----------------------------------------------------

        bank_user_df = load_csv(
            "BankUser.csv"
        )

        # CSV may use full_name while MySQL uses fullname.
        '''if "full_name" in bank_user_df.columns:

            bank_user_df = bank_user_df.rename(
                columns={
                    "full_name": "fullname"
                }
            )'''

        insert_dataframe(

            cursor,

            "bankuser",

            [
                "user_id",
                "branch_id",
                "full_name",
                "role",
                "email",
                "phone",
                "status"
            ],

            bank_user_df
        )


        # ----------------------------------------------------
        # Fraud Rule
        # ----------------------------------------------------

        fraud_rule_df = load_csv(
            "FraudRule.csv"
        )

        insert_dataframe(

            cursor,

            "fraudrule",

            [
                "rule_id",
                "rule_name",
                "description",
                "risk_score",
                "active"
            ],

            fraud_rule_df
        )


        # ====================================================
        # LOAD TRANSACTION DATA
        # ====================================================

        print("\nLoading transaction data...")


        # ----------------------------------------------------
        # Bank Transaction
        # ----------------------------------------------------

        bank_transaction_df = load_csv(
            "BankTransaction.csv"
        )

        insert_dataframe(

            cursor,

            "banktransaction",

            [
                "transaction_id",
                "reference_number",
                "sender_account_id",
                "receiver_account_id",
                "device_id",
                "amount",
                "transaction_type",
                "channel",
                "city",
                "ip_address",
                "location",
                "status",
                "fraud_flag",
                "fraud_score",
                "remarks",
                "created_by",
                "transaction_time"
            ],

            bank_transaction_df
        )


        # ----------------------------------------------------
        # Login Log
        # ----------------------------------------------------

        login_df = load_csv(
            "LoginLog.csv"
        )

        insert_dataframe(

            cursor,

            "loginlog",

            [
                "login_id",
                "customer_id",
                "device_id",
                "ip_address",
                "city",
                "login_time",
                "login_status"
            ],

            login_df
        )


        # ----------------------------------------------------
        # Fraud Alert
        # ----------------------------------------------------

        fraud_alert_df = load_csv(
            "FraudAlert.csv"
        )

        if len(fraud_alert_df) > 0:

            insert_dataframe(

                cursor,

                "fraudalert",

                [
                    "alert_id",
                    "transaction_id",
                    "rule_id",
                    "customer_id",
                    "assigned_to",
                    "risk_score",
                    "alert_level",
                    "reason",
                    "status"
                ],

                fraud_alert_df
            )


        # ----------------------------------------------------
        # Audit Log
        # ----------------------------------------------------

        audit_df = load_csv(
            "AuditLog.csv"
        )

        insert_dataframe(

            cursor,

            "auditlog",

            [
                "audit_id",
                "table_name",
                "record_id",
                "action_type",
                "changed_by",
                "old_value",
                "new_value"
            ],

            audit_df
        )


        # ====================================================
        # RE-ENABLE FOREIGN KEYS
        # ====================================================

        cursor.execute(
            "SET FOREIGN_KEY_CHECKS = 1"
        )


        # ====================================================
        # COMMIT
        # ====================================================

        connection.commit()


        # ====================================================
        # VALIDATION
        # ====================================================

        print("\n")
        print("=" * 65)
        print("DATABASE VALIDATION")
        print("=" * 65)


        validation_tables = {

            "branch": 20,

            "customer": 47801,

            "account": 47801,

            "device": 95774,

            "bankuser": 50,

            "fraudrule": 6,

            "banktransaction": 30000,

            "loginlog": 30000,

            "fraudalert": 84,

            "auditlog": 30000

        }


        all_valid = True


        for table, expected in validation_tables.items():

            cursor.execute(
                f"SELECT COUNT(*) FROM `{table}`"
            )

            actual = cursor.fetchone()[0]

            if actual == expected:

                status = "OK"

            else:

                status = "MISMATCH"

                all_valid = False


            print(
                f"{table:<20} "
                f"{actual:>8,} / "
                f"{expected:>8,} "
                f"[{status}]"
            )


        print()


        if all_valid:

            print(
                "DATABASE LOAD SUCCESSFUL"
            )

            print(
                "All expected row counts match."
            )

        else:

            print(
                "DATABASE LOAD COMPLETED "
                "WITH ROW COUNT MISMATCHES."
            )


    except Exception as error:

        print("\n")
        print("=" * 65)
        print("DATABASE LOAD FAILED")
        print("=" * 65)

        print(error)

        connection.rollback()

        cursor.execute(
            "SET FOREIGN_KEY_CHECKS = 1"
        )

        sys.exit(1)


    finally:

        cursor.close()

        connection.close()

        print("\nMySQL connection closed.")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()