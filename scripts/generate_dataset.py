import random
from datetime import datetime

import pandas as pd
from faker import Faker
from tqdm import tqdm

from config import *
fake = Faker("en_IN")

random.seed(42)
Faker.seed(42)
class FraudLensGenerator:
        def __init__(self):

         self.transactions = None

         self.unique_accounts = []

         self.account_mapping = {}

         self.mapping_df = None

         self.activity_df = None

         self.active_accounts = None

         self.branch_df = None

         self.customer_df = None

         self.account_df = None

         self.device_df = None

         self.bank_user_df = None

         self.fraud_rule_df = None
         self.customer_branch = {}
        def load_dataset(self):

         print("\nLoading dataset...")

         self.transactions = pd.read_csv(INPUT_FILE)

         print(f"Rows Loaded : {len(self.transactions):,}")
        def extract_unique_accounts(self):

         print("\nExtracting Accounts...")

         senders = set(self.transactions["nameOrig"])

         receivers = set(self.transactions["nameDest"])

         self.unique_accounts = sorted(senders.union(receivers))

         print(f"Unique Accounts : {len(self.unique_accounts):,}")
        def create_mapping(self):

         print("\nCreating Account Mapping...")

         customer_id = 1

         account_id = 100001

         for account in self.unique_accounts:

            if account.startswith("C"):

                customer_type = "Individual"

            else:

                customer_type = "Merchant"

            self.account_mapping[account] = {

                "customer_id": customer_id,

                "account_id": account_id,

                "customer_type": customer_type

            }

            customer_id += 1

            account_id += 1

         print("Mapping Created.")
        def save_mapping(self):

          rows = []

          for paysim_id, data in self.account_mapping.items():

            rows.append({

                "paysim_id": paysim_id,

                "customer_id": data["customer_id"],

                "account_id": data["account_id"],

                "customer_type": data["customer_type"]

            })

          self.mapping_df = pd.DataFrame(rows)

          self.mapping_df.to_csv(

            OUTPUT_DIR / "Mapping.csv",

            index=False

         )

          print("Mapping.csv saved.")
        def generate_branches(self):

         print("\nGenerating Branch.csv...")

         cities = [
            ("Mumbai", "Maharashtra"),
            ("Delhi", "Delhi"),
            ("Bengaluru", "Karnataka"),
            ("Hyderabad", "Telangana"),
            ("Chennai", "Tamil Nadu"),
            ("Pune", "Maharashtra"),
            ("Kolkata", "West Bengal"),
            ("Ahmedabad", "Gujarat"),
            ("Jaipur", "Rajasthan"),
            ("Lucknow", "Uttar Pradesh"),
            ("Visakhapatnam", "Andhra Pradesh"),
            ("Vijayawada", "Andhra Pradesh"),
            ("Kochi", "Kerala"),
            ("Bhopal", "Madhya Pradesh"),
            ("Nagpur", "Maharashtra"),
            ("Indore", "Madhya Pradesh"),
            ("Patna", "Bihar"),
            ("Surat", "Gujarat"),
            ("Mysuru", "Karnataka"),
            ("Coimbatore", "Tamil Nadu")
         ]

         branches = []

         for branch_id, (city, state) in enumerate(cities, start=1):

            branches.append({

                "branch_id": branch_id,

                "branch_code": f"BR{branch_id:04}",

                "branch_name": f"{city} Branch",

                "city": city,

                "state": state,

                "phone": fake.numerify("9#########"),

                "manager_name": fake.name()

            })

         self.branch_df = pd.DataFrame(branches)

         self.branch_df.to_csv(
            OUTPUT_DIR / "Branch.csv",
            index=False
         )

         print(f"Generated {len(self.branch_df)} branches.")
        def generate_customers(self):

         print("\nGenerating Customer.csv...")

         customers = []

         for account, data in tqdm(
            self.account_mapping.items(),
            desc="Customers"):

          first = fake.first_name()

          last = fake.last_name()

        
          branch_id = random.randint(1, 20)

        
          self.customer_branch[data["customer_id"]] = branch_id

          customers.append({

            "customer_id": data["customer_id"],

            "branch_id": branch_id,

            "first_name": first,

            "last_name": last,

            "customer_type": data["customer_type"],

            "dob": fake.date_of_birth(
                minimum_age=18,
                maximum_age=75
            ),

            "gender": random.choice([
                "Male",
                "Female"
            ]),

            "phone": fake.unique.numerify(
                "9#########"
            ),

            "email": fake.unique.email(),

            "aadhaar_number": fake.unique.numerify(
                "############"
            ),

            "pan_number": fake.unique.bothify(
                text="?????####?"
            ).upper(),

            "address": fake.address().replace("\n", " "),

            "city": fake.city(),

            "state": fake.state(),

            "kyc_status": random.choices(
                ["Verified", "Pending", "Rejected"],
                weights=[85, 10, 5]
            )[0]

          })

          self.customer_df = pd.DataFrame(customers)

          self.customer_df.to_csv(
          OUTPUT_DIR / "Customer.csv",
          index=False
         )

         print(f"Generated {len(self.customer_df)} customers.")
        def generate_accounts(self):

         print("\nGenerating Account.csv...")

         accounts = []
 
         for account, data in tqdm(
            self.account_mapping.items(),
            desc="Accounts"):

    
            branch_id = self.customer_branch[data["customer_id"]]

            balance = round(
            random.uniform(5000, 500000),
            2
            )

            accounts.append({

            "account_id": data["account_id"],

            "account_number": fake.unique.numerify(
                "############"
            ),

            "customer_id": data["customer_id"],

            # Use the same branch as the customer
            "branch_id": branch_id,

            "account_type": random.choice([
                "Savings",
                "Current",
                "Salary"
            ]),

            "balance": balance,

            "status": random.choices(
                [
                    "Active",
                    "Frozen",
                    "Closed"
                ],
                weights=[90, 7, 3]
            )[0],

            "opening_date": fake.date_between(
                start_date="-10y",
                end_date="-1y"
            )

           })

            self.account_df = pd.DataFrame(accounts)

            self.account_df.to_csv(
            OUTPUT_DIR / "Account.csv",
            index=False
            )

            print(f"Generated {len(self.account_df)} accounts.")
        def generate_devices(self):

          print("\nGenerating Device.csv...")

          devices = []

          device_types = [
          "Mobile",
          "Laptop",
          "ATM",
          "Tablet"
          ]

          operating_systems = {

           "Mobile": ["Android 13", "Android 14", "iOS 17"],

           "Laptop": ["Windows 11", "Ubuntu 24.04", "macOS Sonoma"],

           "ATM": ["Embedded Linux"],

           "Tablet": ["Android 14", "iPadOS 17"]

         }

          device_id = 1

          for customer in tqdm(
            self.customer_df.itertuples(index=False),
            total=len(self.customer_df),
            desc="Devices"):

        
            number_of_devices = random.randint(1, 3)

          for _ in range(number_of_devices):

            device_type = random.choice(device_types)

            devices.append({

                "device_id": device_id,

                "customer_id": customer.customer_id,

                "device_name": f"{device_type}-{random.randint(1000,9999)}",

                "device_type": device_type,

                "operating_system": random.choice(
                    operating_systems[device_type]
                ),

                "ip_address": fake.ipv4_public(),

                "trusted_device": random.choices(
                    [True, False],
                    weights=[85, 15]
                )[0],

                "last_login": fake.date_time_between(
                    start_date="-30d",
                    end_date="now"
                )

            })

            device_id += 1

            self.device_df = pd.DataFrame(devices)

            self.device_df.to_csv(
            OUTPUT_DIR / "Device.csv",
            index=False
            )

            print(f"Generated {len(self.device_df)} devices.")
        def generate_bank_users(self):

          print("\nGenerating BankUser.csv...")

          users = []

          roles = [

         "Admin",

         "Fraud Analyst",

         "Branch Manager",

         "Cashier",

         "Auditor"

         ]

          for user_id in range(1, 51):

           users.append({

            "user_id": user_id,

            "branch_id": random.randint(1, 20),

            "full_name": fake.name(),

            "role": random.choice(roles),

            "email": fake.unique.email(),

            "phone": fake.unique.numerify(
                "9#########"
            ),

            "status": random.choices(
                ["Active", "Inactive"],
                weights=[90, 10]
            )[0]

          })

          self.bank_user_df = pd.DataFrame(users)

          self.bank_user_df.to_csv(
          OUTPUT_DIR / "BankUser.csv",
          index=False
          )

          print(f"Generated {len(self.bank_user_df)} bank users.")
        def generate_fraud_rules(self):

         print("\nGenerating FraudRule.csv...")

         rules = [

         ("High Amount Transaction",
         "Transaction exceeds ₹2,00,000",
         90),

         ("Multiple Transactions",
         "More than 10 transactions in one hour",
         80),

         ("Unknown Device",
         "Transaction from an untrusted device",
         75),

         ("Location Mismatch",
         "Transaction from a new city",
         70),

         ("Rapid Transfers",
          "Multiple outward transfers within minutes",
         95),

         ("Blacklisted Receiver",
         "Receiver account is blacklisted",
         100)

         ]

         fraud_rules = []

         for rule_id, (name, description, score) in enumerate(rules, start=1):

          fraud_rules.append({

            "rule_id": rule_id,

            "rule_name": name,

            "description": description,

            "risk_score": score,

            "active": True

          })

         self.fraud_rule_df = pd.DataFrame(fraud_rules)

         self.fraud_rule_df.to_csv(
         OUTPUT_DIR / "FraudRule.csv",
         index=False
         )

         print(f"Generated {len(self.fraud_rule_df)} fraud rules.")

        def run(self):

          self.load_dataset()

          self.extract_unique_accounts()

          self.create_mapping()

          self.save_mapping()

          self.generate_branches()

          self.generate_customers()

          self.generate_accounts()

          self.generate_devices()

          self.generate_bank_users()

          self.generate_fraud_rules()

          print("\nAll master datasets generated successfully.")
if __name__ == "__main__":

    generator = FraudLensGenerator()

    generator.run()

    print("\nFraudLens master data generation completed.")