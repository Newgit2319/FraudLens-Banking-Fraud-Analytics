import json
from pathlib import Path

import pandas as pd
import streamlit as st
import mysql.connector
import plotly.express as px


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "output"
MODELS_DIR = BASE_DIR / "models"

ML_PREDICTIONS_FILE = OUTPUT_DIR / "ML_Predictions.csv"
METRICS_FILE = MODELS_DIR / "model_metrics.json"
CONFUSION_MATRIX_FILE = MODELS_DIR / "confusion_matrix.png"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="FraudLens",
    page_icon="🛡️",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        color: #888888;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .risk-critical {
        color: #ff4b4b;
        font-weight: bold;
    }

    .risk-high {
        color: #ff8c00;
        font-weight: bold;
    }

    .risk-medium {
        color: #e6b800;
        font-weight: bold;
    }

    .risk-low {
        color: #21c55d;
        font-weight: bold;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🛡️ FraudLens</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Banking Fraud Detection & Risk Analytics Platform'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

@st.cache_resource
def get_connection(
    host,
    port,
    user,
    password,
    database
):

    return mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ FraudLens")

st.sidebar.markdown("### Database")

db_host = st.sidebar.text_input(
    "Host",
    value="localhost"
)

db_port = st.sidebar.number_input(
    "Port",
    value=3306
)

db_user = st.sidebar.text_input(
    "Username",
    value="root"
)

db_password = st.sidebar.text_input(
    "Password",
    type="password"
)

db_name = st.sidebar.text_input(
    "Database",
    value="fraudlens"
)


try:

    connection = get_connection(
        db_host,
        db_port,
        db_user,
        db_password,
        db_name
    )

    st.sidebar.success(
        "🟢 MySQL Connected"
    )

except Exception as e:

    st.sidebar.error(
        "🔴 Database connection failed"
    )

    st.sidebar.caption(
        "Check MySQL credentials."
    )

    st.stop()


# ============================================================
# HELPER FUNCTION
# ============================================================

def run_query(query):

    cursor = connection.cursor(
        dictionary=True
    )

    cursor.execute(query)

    result = cursor.fetchall()

    cursor.close()

    return pd.DataFrame(result)


# ============================================================
# NAVIGATION
# ============================================================

page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Dashboard",
        "🔎 Transaction Investigation",
        "🚨 Fraud Alerts",
        "🤖 ML Risk Analysis"
    ]
)


# ============================================================
# PAGE 1 — DASHBOARD
# ============================================================

if page == "📊 Dashboard":

    st.header(
        "Fraud Detection Dashboard"
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    summary = run_query(
        """
        SELECT *
        FROM vw_fraud_summary
        """
    )

    if not summary.empty:

        row = summary.iloc[0]

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric(
            "Transactions",
            f"{int(row['total_transactions']):,}"
        )

        col2.metric(
            "Fraud Cases",
            f"{int(row['fraud_transactions']):,}"
        )

        col3.metric(
            "Fraud Rate",
            f"{row['fraud_rate_percent']:.2f}%"
        )

        col4.metric(
            "Fraud Amount",
            f"₹{row['total_fraud_amount']:,.2f}"
        )

        col5.metric(
            "Avg Risk Score",
            f"{row['average_fraud_score']:.2f}"
        )

    st.divider()

    # --------------------------------------------------------
    # Fraud by transaction type
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "Fraud by Transaction Type"
        )

        fraud_type = run_query(
            """
            SELECT *
            FROM vw_fraud_by_type
            """
        )

        if not fraud_type.empty:

            fig = px.bar(
                fraud_type,
                x="transaction_type",
                y="fraud_transactions",
                title="Fraud Transactions by Type"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # --------------------------------------------------------
    # Fraud by channel
    # --------------------------------------------------------

    with col2:

        st.subheader(
            "Fraud by Channel"
        )

        channel = run_query(
            """
            SELECT *
            FROM vw_fraud_by_channel
            """
        )

        if not channel.empty:

            fig = px.bar(
                channel,
                x="channel",
                y="fraud_transactions",
                title="Fraud Transactions by Channel"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # --------------------------------------------------------
    # Daily fraud trend
    # --------------------------------------------------------
    
    # --------------------------------------------------------
# Transaction date summary
# --------------------------------------------------------

    st.subheader(
    "📅 Transaction Date Summary"
    )

    daily = run_query(
    """
    SELECT
        DATE(transaction_time) AS transaction_date,
        COUNT(*) AS total_transactions,
        SUM(fraud_flag) AS fraud_transactions,
        SUM(
            CASE
                WHEN fraud_flag = 1
                THEN amount
                ELSE 0
            END
        ) AS fraud_amount
    FROM banktransaction
    GROUP BY DATE(transaction_time)
    ORDER BY transaction_date
    """
    )

    if not daily.empty:

     date_row = daily.iloc[0]

     col1, col2, col3, col4 = st.columns(4)
 
     col1.metric(
        "Transaction Date",
        pd.to_datetime(
            date_row["transaction_date"]
        ).strftime("%d %b %Y")
     )

     col2.metric(
        "Transactions",
        f"{int(date_row['total_transactions']):,}"
     )

     col3.metric(
        "Fraud Cases",
        f"{int(date_row['fraud_transactions']):,}"
     )

     col4.metric(
        "Fraud Amount",
        f"₹{float(date_row['fraud_amount']):,.2f}"
     )

     st.info(
        "The current FraudLens dataset contains transactions "
        "for a single transaction date. Therefore, a multi-day "
        "fraud trend is not available in the source data."
     )

    else:

     st.info(
        "No transaction date information available."
     )

    

    # --------------------------------------------------------
    # Location analysis
    # --------------------------------------------------------

    st.subheader(
        "🌍 Fraud by Location"
    )

    location = run_query(
        """
    SELECT
    city,
    total_transactions,
    fraud_transactions,
    ROUND(
        (fraud_transactions / total_transactions) * 100,
        2
    ) AS fraud_rate_percent,
    fraud_amount,
    average_fraud_score
     FROM vw_fraud_by_location
     WHERE total_transactions > 0
    ORDER BY fraud_transactions DESC, fraud_amount DESC
    LIMIT 15
        """
    )

    if not location.empty:

        st.dataframe(
    location,
    use_container_width=True,
    hide_index=True,
    column_config={
        "total_transactions": st.column_config.NumberColumn(
            "Transactions",
            format="%d"
        ),
        "fraud_transactions": st.column_config.NumberColumn(
            "Fraud Cases",
            format="%d"
        ),
        "fraud_rate_percent": st.column_config.NumberColumn(
            "Fraud Rate",
            format="%.2f%%"
        ),
        "fraud_amount": st.column_config.NumberColumn(
            "Fraud Amount",
            format="₹%.2f"
        ),
        "average_fraud_score": st.column_config.NumberColumn(
            "Avg Risk Score",
            format="%.2f"
        )
    }
)


# ============================================================
# PAGE 2 — TRANSACTION INVESTIGATION
# ============================================================

elif page == "🔎 Transaction Investigation":

    st.header(
        "🔎 Transaction Investigation"
    )

    st.write(
        "Search transactions and investigate customer, "
        "device and fraud-risk information."
    )

    search_id = st.number_input(
        "Transaction ID",
        min_value=1,
        value=1,
        step=1
    )

    if st.button(
        "Investigate Transaction",
        type="primary"
    ):

        query = f"""
        SELECT

            bt.transaction_id,
            bt.reference_number,
            bt.amount,
            bt.transaction_type,
            bt.channel,
            bt.city,
            bt.ip_address,
            bt.location,
            bt.status,
            bt.fraud_flag,
            bt.fraud_score,
            bt.remarks,
            bt.transaction_time,

            c.customer_id,

            CONCAT(
                c.first_name,
                ' ',
                c.last_name
            ) AS customer_name,

            c.phone,
            c.email,

            d.device_id,
            d.device_type,
            d.operating_system,
            d.trusted_device

        FROM banktransaction bt

        JOIN account a
            ON bt.sender_account_id =
               a.account_id

        JOIN customer c
            ON a.customer_id =
               c.customer_id

        LEFT JOIN device d
            ON bt.device_id =
               d.device_id

        WHERE bt.transaction_id =
              {search_id}

        LIMIT 1
        """

        result = run_query(query)

        if result.empty:

            st.warning(
                "No transaction found."
            )

        else:

            transaction = result.iloc[0]

            # ----------------------------------------------
            # Transaction metrics
            # ----------------------------------------------

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Amount",
                f"₹{transaction['amount']:,.2f}"
            )

            col2.metric(
                "Fraud Score",
                transaction["fraud_score"]
            )

            col3.metric(
                "Fraud Flag",
                "🚨 FRAUD"
                if transaction["fraud_flag"] == 1
                else "Normal"
            )

            col4.metric(
                "Status",
                transaction["status"]
            )

            st.divider()

            # ----------------------------------------------
            # Customer
            # ----------------------------------------------

            st.subheader(
                "👤 Customer Information"
            )

            customer_data = pd.DataFrame(
                {
                    "Field": [
                        "Customer ID",
                        "Customer Name",
                        "Phone",
                        "Email"
                    ],

                    "Value": [
                        transaction["customer_id"],
                        transaction["customer_name"],
                        transaction["phone"],
                        transaction["email"]
                    ]
                }
            )

            st.dataframe(
                customer_data,
                use_container_width=True,
                hide_index=True
            )

            # ----------------------------------------------
            # Transaction
            # ----------------------------------------------

            st.subheader(
                "💳 Transaction Information"
            )

            transaction_data = pd.DataFrame(
                {
                    "Field": [
                        "Reference",
                        "Amount",
                        "Transaction Type",
                        "Channel",
                        "City",
                        "IP Address",
                        "Location",
                        "Transaction Time",
                        "Remarks"
                    ],

                    "Value": [
                        transaction["reference_number"],
                        f"₹{transaction['amount']:,.2f}",
                        transaction["transaction_type"],
                        transaction["channel"],
                        transaction["city"],
                        transaction["ip_address"],
                        transaction["location"],
                        transaction["transaction_time"],
                        transaction["remarks"]
                    ]
                }
            )

            st.dataframe(
                transaction_data,
                use_container_width=True,
                hide_index=True
            )

            # ----------------------------------------------
            # Device
            # ----------------------------------------------

            st.subheader(
                "📱 Device Information"
            )

            device_data = pd.DataFrame(
                {
                    "Field": [
                        "Device ID",
                        "Device Type",
                        "Operating System",
                        "Trusted Device"
                    ],

                    "Value": [
                        transaction["device_id"],
                        transaction["device_type"],
                        transaction["operating_system"],
                        "Yes"
                        if transaction["trusted_device"]
                        else "No"
                    ]
                }
            )

            st.dataframe(
                device_data,
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# PAGE 3 — FRAUD ALERTS
# ============================================================

elif page == "🚨 Fraud Alerts":

    st.header(
        "🚨 Fraud Alert Center"
    )

    alerts = run_query(
        """
        SELECT

            fa.alert_id,
            fa.transaction_id,
            fa.customer_id,
            fa.risk_score,
            fa.alert_level,
            fa.reason,
            fa.status,
            fa.created_at,

            CONCAT(
                c.first_name,
                ' ',
                c.last_name
            ) AS customer_name

        FROM fraudalert fa

        LEFT JOIN customer c
            ON fa.customer_id =
               c.customer_id

        ORDER BY
            fa.risk_score DESC
        """
    )

    if alerts.empty:

        st.info(
            "No fraud alerts available."
        )

    else:

        # ----------------------------------------------------
        # Alert metrics
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Alerts",
            len(alerts)
        )

        col2.metric(
            "Critical",
            int(
                (
                    alerts["alert_level"]
                    == "Critical"
                ).sum()
            )
        )

        col3.metric(
            "High",
            int(
                (
                    alerts["alert_level"]
                    == "High"
                ).sum()
            )
        )

        col4.metric(
            "Open",
            int(
                (
                    alerts["status"]
                    == "Open"
                ).sum()
            )
        )

        st.divider()

        # ----------------------------------------------------
        # Filter
        # ----------------------------------------------------

        level_filter = st.multiselect(
            "Alert Level",
            options=sorted(
                alerts["alert_level"]
                .dropna()
                .unique()
            )
        )

        status_filter = st.multiselect(
            "Status",
            options=sorted(
                alerts["status"]
                .dropna()
                .unique()
            )
        )

        filtered = alerts.copy()

        if level_filter:

            filtered = filtered[
                filtered["alert_level"].isin(
                    level_filter
                )
            ]

        if status_filter:

            filtered = filtered[
                filtered["status"].isin(
                    status_filter
                )
            ]

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # Alert distribution
        # ----------------------------------------------------

        st.subheader(
            "Alert Distribution"
        )

        alert_chart = (
            alerts["alert_level"]
            .value_counts()
            .reset_index()
        )

        alert_chart.columns = [
            "alert_level",
            "count"
        ]

        fig = px.pie(
            alert_chart,
            names="alert_level",
            values="count",
            title="Fraud Alerts by Severity"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# PAGE 4 — ML RISK ANALYSIS
# ============================================================

elif page == "🤖 ML Risk Analysis":

    st.header(
        "🤖 Machine Learning Risk Analysis"
    )

    st.write(
        "Random Forest fraud-risk predictions generated "
        "from transaction and behavioral features."
    )

    # --------------------------------------------------------
    # Model metrics
    # --------------------------------------------------------

    if METRICS_FILE.exists():

        with open(
            METRICS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            metrics = json.load(file)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Precision",
            f"{metrics['precision']:.4f}"
        )

        col2.metric(
            "Recall",
            f"{metrics['recall']:.4f}"
        )

        col3.metric(
            "F1 Score",
            f"{metrics['f1_score']:.4f}"
        )

        col4.metric(
            "ROC-AUC",
            f"{metrics['roc_auc']:.4f}"
        )

    st.divider()

    # --------------------------------------------------------
    # Load predictions
    # --------------------------------------------------------

    if not ML_PREDICTIONS_FILE.exists():

        st.error(
            "ML_Predictions.csv not found."
        )

        st.stop()

    predictions = pd.read_csv(
        ML_PREDICTIONS_FILE
    )

    # --------------------------------------------------------
    # Prediction summary
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Transactions",
        f"{len(predictions):,}"
    )

    col2.metric(
        "ML Predicted Fraud",
        f"{int(predictions['ml_prediction'].sum()):,}"
    )

    col3.metric(
        "High Risk",
        f"{int((predictions['ml_risk_level'] == 'High').sum()):,}"
    )

    col4.metric(
        "Critical",
        f"{int((predictions['ml_risk_level'] == 'Critical').sum()):,}"
    )

    st.divider()

    # --------------------------------------------------------
    # Risk distribution
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "Risk Distribution"
        )

        risk_distribution = (
            predictions[
                "ml_risk_level"
            ]
            .value_counts()
            .reset_index()
        )

        risk_distribution.columns = [
            "risk_level",
            "count"
        ]

        fig = px.bar(
            risk_distribution,
            x="risk_level",
            y="count",
            title="ML Risk Levels"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # Probability distribution
    # --------------------------------------------------------

    with col2:

        st.subheader(
            "Fraud Probability"
        )

        fig = px.histogram(
            predictions,
            x="ml_fraud_probability",
            nbins=30,
            title="ML Fraud Probability Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # Highest-risk transactions
    # --------------------------------------------------------

    st.subheader(
        "🔥 Highest-Risk Transactions"
    )

    high_risk = (
        predictions
        .sort_values(
            "ml_risk_score",
            ascending=False
        )
        .head(50)
    )

    st.dataframe(
        high_risk,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # Confusion matrix
    # --------------------------------------------------------

    if CONFUSION_MATRIX_FILE.exists():

        st.subheader(
            "Model Confusion Matrix"
        )

        st.image(
            str(CONFUSION_MATRIX_FILE),
            width=550
        )

    # --------------------------------------------------------
    # Model information
    # --------------------------------------------------------

    st.subheader(
        "Model Information"
    )

    st.info(
        """
        Model: Random Forest Classifier

        Target: fraud_flag

        The model uses transaction, device,
        time-based and behavioral features.

        fraud_flag and fraud_score are not used
        as predictive input features.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.sidebar.divider()

st.sidebar.caption(
    "FraudLens • Banking Fraud Detection & Risk Analytics"
)

st.sidebar.caption(
    "SQL + Machine Learning + Streamlit"
)