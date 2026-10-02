import random

import pandas as pd
from faker import Faker
from tqdm import tqdm

from config import DATASET_DIR, OUTPUT_DIR


# --------------------------------------------------
# Configuration
# --------------------------------------------------

fake = Faker("en_IN")

random.seed(42)
Faker.seed(42)


# --------------------------------------------------
# Load Customers
# --------------------------------------------------

print("\nLoading Customer.csv...")

customers = pd.read_csv(
    OUTPUT_DIR / "Customer.csv"
)

print(f"Customers loaded: {len(customers):,}")


# --------------------------------------------------
# Device Configuration
# --------------------------------------------------

device_types = [
    "Mobile",
    "Laptop",
    "Tablet"
]

operating_systems = {

    "Mobile": [
        "Android 13",
        "Android 14",
        "iOS 17"
    ],

    "Laptop": [
        "Windows 11",
        "Ubuntu 24.04",
        "macOS Sonoma"
    ],

    "Tablet": [
        "Android 14",
        "iPadOS 17"
    ]

}


# --------------------------------------------------
# Generate Devices
# --------------------------------------------------

print("\nGenerating Device.csv...\n")

devices = []

device_id = 1


for customer in tqdm(
    customers.itertuples(index=False),
    total=len(customers),
    desc="Devices"
):

    # Each customer gets 1–3 devices
    number_of_devices = random.randint(1, 3)

    for _ in range(number_of_devices):

        device_type = random.choice(device_types)

        devices.append({

            "device_id": device_id,

            "customer_id": customer.customer_id,

            "device_name": (
                f"{device_type}-"
                f"{random.randint(1000, 9999)}"
            ),

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


# --------------------------------------------------
# Save
# --------------------------------------------------

device_df = pd.DataFrame(devices)

device_df.to_csv(
    OUTPUT_DIR / "Device.csv",
    index=False
)


# --------------------------------------------------
# Summary
# --------------------------------------------------

print("\n======================================")
print("Device.csv generated successfully")
print("======================================")

print(f"Customers : {len(customers):,}")
print(f"Devices   : {len(device_df):,}")

print(
    f"Average devices/customer: "
    f"{len(device_df) / len(customers):.2f}"
)

print("\nDevice distribution:")

print(
    device_df["device_type"]
    .value_counts()
)

print("\nTrusted device distribution:")

print(
    device_df["trusted_device"]
    .value_counts()
)

print("\n======================================")