import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "output"

MODELS_DIR = BASE_DIR / "models"

MODELS_DIR.mkdir(
    exist_ok=True
)


TRANSACTION_FILE = (
    OUTPUT_DIR / "BankTransaction.csv"
)

DEVICE_FILE = (
    OUTPUT_DIR / "Device.csv"
)


# ============================================================
# CONFIGURATION
# ============================================================

RANDOM_STATE = 42

TEST_SIZE = 0.20


# ============================================================
# LOAD DATA
# ============================================================

print()
print("=" * 65)
print("FRAUDLENS ML FRAUD DETECTION")
print("=" * 65)

print("\nLoading transaction data...")

df = pd.read_csv(
    TRANSACTION_FILE
)

devices = pd.read_csv(
    DEVICE_FILE
)


print(
    f"Transactions loaded: {len(df):,}"
)


# ============================================================
# BASIC VALIDATION
# ============================================================

required_columns = [

    "transaction_id",
    "sender_account_id",
    "receiver_account_id",
    "device_id",
    "amount",
    "transaction_type",
    "channel",
    "city",
    "transaction_time",
    "fraud_flag"

]


missing_columns = [

    column

    for column in required_columns

    if column not in df.columns

]


if missing_columns:

    raise ValueError(
        "Missing required columns: "
        + ", ".join(missing_columns)
    )


print("\nFraud distribution:")

print(
    df["fraud_flag"].value_counts()
)


# ============================================================
# DEVICE INFORMATION
# ============================================================

print("\nAdding device information...")


device_features = devices[
    [
        "device_id",
        "trusted_device",
        "device_type",
        "operating_system"
    ]
].copy()


df = df.merge(
    device_features,
    on="device_id",
    how="left"
)


# ============================================================
# DATETIME FEATURES
# ============================================================

print("Creating time-based features...")


df["transaction_time"] = pd.to_datetime(
    df["transaction_time"]
)


df["transaction_hour"] = (
    df["transaction_time"].dt.hour
)


df["transaction_day"] = (
    df["transaction_time"].dt.day
)


df["transaction_dayofweek"] = (
    df["transaction_time"].dt.dayofweek
)


df["is_weekend"] = (
    df["transaction_dayofweek"] >= 5
).astype(int)


df["is_night"] = (
    (df["transaction_hour"] < 6)
    |
    (df["transaction_hour"] >= 22)
).astype(int)


# ============================================================
# AMOUNT FEATURES
# ============================================================

print("Creating transaction amount features...")


df["log_amount"] = (
    __import__("numpy")
    .log1p(df["amount"])
)


df["is_high_value"] = (
    df["amount"] >= 200000
).astype(int)


# ============================================================
# CUSTOMER / ACCOUNT BEHAVIOR FEATURES
# ============================================================

print("Creating behavioral features...")


# Number of transactions made by sender account
sender_frequency = (
    df.groupby("sender_account_id")
    .size()
    .rename("sender_transaction_count")
)


df = df.merge(
    sender_frequency,
    on="sender_account_id",
    how="left"
)


# Average transaction amount for sender
sender_avg_amount = (
    df.groupby("sender_account_id")["amount"]
    .mean()
    .rename("sender_average_amount")
)


df = df.merge(
    sender_avg_amount,
    on="sender_account_id",
    how="left"
)


# Number of transactions made using device
device_frequency = (
    df.groupby("device_id")
    .size()
    .rename("device_transaction_count")
)


df = df.merge(
    device_frequency,
    on="device_id",
    how="left"
)


# Number of transactions between sender and receiver
account_pair_frequency = (
    df.groupby(
        [
            "sender_account_id",
            "receiver_account_id"
        ]
    )
    .size()
    .rename("account_pair_frequency")
    .reset_index()
)


df = df.merge(
    account_pair_frequency,
    on=[
        "sender_account_id",
        "receiver_account_id"
    ],
    how="left"
)


# ============================================================
# TARGET
# ============================================================

TARGET = "fraud_flag"


y = df[TARGET].astype(int)


# ============================================================
# FEATURES
# ============================================================

feature_columns = [

    "amount",
    "log_amount",

    "transaction_type",
    "channel",

    "city",

    "device_type",
    "operating_system",

    "trusted_device",

    "transaction_hour",
    "transaction_dayofweek",

    "is_weekend",
    "is_night",
    "is_high_value",

    "sender_transaction_count",
    "sender_average_amount",

    "device_transaction_count",

    "account_pair_frequency"

]


X = df[
    feature_columns
].copy()


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

print("\nSplitting dataset...")


X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=TEST_SIZE,

    random_state=RANDOM_STATE,

    stratify=y

)


print(
    f"Training records : {len(X_train):,}"
)

print(
    f"Testing records  : {len(X_test):,}"
)

print(
    f"Training frauds   : {y_train.sum():,}"
)

print(
    f"Testing frauds    : {y_test.sum():,}"
)


# ============================================================
# COLUMN TYPES
# ============================================================

categorical_features = [

    "transaction_type",
    "channel",
    "city",
    "device_type",
    "operating_system"

]


numeric_features = [

    "amount",
    "log_amount",

    "trusted_device",

    "transaction_hour",
    "transaction_dayofweek",

    "is_weekend",
    "is_night",
    "is_high_value",

    "sender_transaction_count",
    "sender_average_amount",

    "device_transaction_count",

    "account_pair_frequency"

]


# ============================================================
# PREPROCESSING
# ============================================================

numeric_pipeline = Pipeline(

    steps=[

        (
            "imputer",

            SimpleImputer(
                strategy="median"
            )
        )

    ]

)


categorical_pipeline = Pipeline(

    steps=[

        (
            "imputer",

            SimpleImputer(
                strategy="most_frequent"
            )
        ),

        (
            "encoder",

            OneHotEncoder(
                handle_unknown="ignore"
            )
        )

    ]

)


preprocessor = ColumnTransformer(

    transformers=[

        (
            "numeric",

            numeric_pipeline,

            numeric_features
        ),

        (
            "categorical",

            categorical_pipeline,

            categorical_features
        )

    ]

)


# ============================================================
# RANDOM FOREST MODEL
# ============================================================

print("\nBuilding Random Forest model...")


model = RandomForestClassifier(

    n_estimators=300,

    max_depth=12,

    min_samples_leaf=2,

    class_weight="balanced",

    random_state=RANDOM_STATE,

    n_jobs=-1

)


pipeline = Pipeline(

    steps=[

        (
            "preprocessor",
            preprocessor
        ),

        (
            "model",
            model
        )

    ]

)


# ============================================================
# TRAIN
# ============================================================

print("\nTraining model...")

pipeline.fit(
    X_train,
    y_train
)


print("Model training completed.")


# ============================================================
# PREDICTIONS
# ============================================================

print("\nGenerating predictions...")


y_pred = pipeline.predict(
    X_test
)


y_probability = pipeline.predict_proba(
    X_test
)[:, 1]


# ============================================================
# EVALUATION
# ============================================================

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)


recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)


f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)


roc_auc = roc_auc_score(
    y_test,
    y_probability
)


print()
print("=" * 65)
print("MODEL PERFORMANCE")
print("=" * 65)

print(
    f"Precision : {precision:.4f}"
)

print(
    f"Recall    : {recall:.4f}"
)

print(
    f"F1 Score  : {f1:.4f}"
)

print(
    f"ROC-AUC   : {roc_auc:.4f}"
)


print("\nClassification Report:\n")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y_test,
    y_pred
)


print("\nConfusion Matrix:")

print(cm)


fig, ax = plt.subplots(
    figsize=(6, 5)
)


display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=[
        "Normal",
        "Fraud"
    ]
)


display.plot(
    ax=ax
)


ax.set_title(
    "FraudLens - Fraud Detection Confusion Matrix"
)


plt.tight_layout()


confusion_path = (
    MODELS_DIR
    / "confusion_matrix.png"
)


plt.savefig(
    confusion_path,
    dpi=150
)


plt.close()


# ============================================================
# GENERATE FULL DATASET PREDICTIONS
# ============================================================

print("\nGenerating predictions for all transactions...")


all_probability = pipeline.predict_proba(
    X
)[:, 1]


all_prediction = (
    all_probability >= 0.50
).astype(int)


# Convert probability into 0–100 risk score
ml_risk_score = (
    all_probability * 100
).round(2)


def risk_level(score):

    if score >= 80:
        return "Critical"

    elif score >= 60:
        return "High"

    elif score >= 30:
        return "Medium"

    else:
        return "Low"


ml_risk_level = [
    risk_level(score)
    for score in ml_risk_score
]


# ============================================================
# SAVE PREDICTIONS
# ============================================================

prediction_df = df[
    [
        "transaction_id",
        "sender_account_id",
        "receiver_account_id",
        "device_id",
        "amount",
        "transaction_type",
        "channel",
        "city",
        "transaction_time",
        "fraud_flag"
    ]
].copy()


prediction_df[
    "ml_fraud_probability"
] = (
    all_probability.round(6)
)


prediction_df[
    "ml_prediction"
] = (
    all_prediction
)


prediction_df[
    "ml_risk_score"
] = (
    ml_risk_score
)


prediction_df[
    "ml_risk_level"
] = (
    ml_risk_level
)


prediction_path = (
    OUTPUT_DIR
    / "ML_Predictions.csv"
)


prediction_df.to_csv(
    prediction_path,
    index=False
)


# ============================================================
# SAVE MODEL
# ============================================================

model_path = (
    MODELS_DIR
    / "fraud_model.pkl"
)


joblib.dump(
    pipeline,
    model_path
)


# ============================================================
# SAVE METRICS
# ============================================================

metrics = {

    "model": "Random Forest",

    "dataset_size": int(len(df)),

    "fraud_cases": int(y.sum()),

    "non_fraud_cases": int(
        len(y) - y.sum()
    ),

    "test_size": TEST_SIZE,

    "precision": round(
        float(precision),
        4
    ),

    "recall": round(
        float(recall),
        4
    ),

    "f1_score": round(
        float(f1),
        4
    ),

    "roc_auc": round(
        float(roc_auc),
        4
    )

}


metrics_path = (
    MODELS_DIR
    / "model_metrics.json"
)


with open(
    metrics_path,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        metrics,
        file,
        indent=4
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

print()
print("=" * 65)
print("ML PIPELINE COMPLETED")
print("=" * 65)

print(
    f"Model saved       : {model_path}"
)

print(
    f"Predictions saved : {prediction_path}"
)

print(
    f"Metrics saved     : {metrics_path}"
)

print(
    f"Confusion matrix  : {confusion_path}"
)

print(
    f"Predicted frauds  : {all_prediction.sum():,}"
)

print()
print("Risk distribution:")

print(
    prediction_df[
        "ml_risk_level"
    ].value_counts()
)

print()
print("FraudLens ML model is ready.")