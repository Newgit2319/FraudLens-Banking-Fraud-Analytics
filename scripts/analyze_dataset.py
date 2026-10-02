import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

input_file = BASE_DIR / "output" / "FraudLens_30000.csv"

df = pd.read_csv(input_file)

print("\n========== DATASET INFO ==========")
print(df.info())

print("\n========== FIRST 5 ROWS ==========")
print(df.head())

print("\n========== TRANSACTION TYPES ==========")
print(df["type"].value_counts())

print("\n========== UNIQUE SENDER ACCOUNTS ==========")
print(df["nameOrig"].nunique())

print("\n========== UNIQUE RECEIVER ACCOUNTS ==========")
print(df["nameDest"].nunique())

print("\n========== FRAUD COUNT ==========")
print(df["isFraud"].value_counts())

print("\n========== TOTAL ROWS ==========")
print(len(df))