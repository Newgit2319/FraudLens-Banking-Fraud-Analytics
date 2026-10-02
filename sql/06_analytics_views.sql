USE fraudlens;

-- ============================================================
-- FRAUDLENS SQL ANALYTICS VIEWS
-- ============================================================


-- ============================================================
-- 1. OVERALL FRAUD SUMMARY
-- ============================================================

DROP VIEW IF EXISTS vw_fraud_summary;

CREATE VIEW vw_fraud_summary AS
SELECT
    COUNT(*) AS total_transactions,

    ROUND(
        SUM(amount),
        2
    ) AS total_transaction_value,

    SUM(
        CASE
            WHEN fraud_flag = 1 THEN 1
            ELSE 0
        END
    ) AS fraud_transactions,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN fraud_flag = 1 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS fraud_rate_percent,

    ROUND(
        SUM(
            CASE
                WHEN fraud_flag = 1 THEN amount
                ELSE 0
            END
        ),
        2
    ) AS total_fraud_amount,

    ROUND(
        AVG(fraud_score),
        2
    ) AS average_fraud_score

FROM banktransaction;


-- ============================================================
-- 2. FRAUD BY TRANSACTION TYPE
-- ============================================================

DROP VIEW IF EXISTS vw_fraud_by_type;

CREATE VIEW vw_fraud_by_type AS
SELECT
    transaction_type,

    COUNT(*) AS total_transactions,

    SUM(
        CASE
            WHEN fraud_flag = 1 THEN 1
            ELSE 0
        END
    ) AS fraud_transactions,

    ROUND(
        SUM(amount),
        2
    ) AS total_amount,

    ROUND(
        SUM(
            CASE
                WHEN fraud_flag = 1 THEN amount
                ELSE 0
            END
        ),
        2
    ) AS fraud_amount,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN fraud_flag = 1 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS fraud_rate_percent

FROM banktransaction

GROUP BY transaction_type

ORDER BY fraud_transactions DESC;


-- ============================================================
-- 3. FRAUD BY CHANNEL
-- ============================================================

DROP VIEW IF EXISTS vw_fraud_by_channel;

CREATE VIEW vw_fraud_by_channel AS
SELECT
    channel,

    COUNT(*) AS total_transactions,

    SUM(
        CASE
            WHEN fraud_flag = 1 THEN 1
            ELSE 0
        END
    ) AS fraud_transactions,

    ROUND(
        SUM(amount),
        2
    ) AS total_amount,

    ROUND(
        SUM(
            CASE
                WHEN fraud_flag = 1 THEN amount
                ELSE 0
            END
        ),
        2
    ) AS fraud_amount,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN fraud_flag = 1 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS fraud_rate_percent

FROM banktransaction

GROUP BY channel

ORDER BY fraud_transactions DESC;


-- ============================================================
-- 4. FRAUD BY LOCATION
-- ============================================================

DROP VIEW IF EXISTS vw_fraud_by_location;

CREATE VIEW vw_fraud_by_location AS
SELECT
    city,

    COUNT(*) AS total_transactions,

    SUM(
        CASE
            WHEN fraud_flag = 1 THEN 1
            ELSE 0
        END
    ) AS fraud_transactions,

    ROUND(
        SUM(amount),
        2
    ) AS total_amount,

    ROUND(
        SUM(
            CASE
                WHEN fraud_flag = 1 THEN amount
                ELSE 0
            END
        ),
        2
    ) AS fraud_amount,

    ROUND(
        AVG(fraud_score),
        2
    ) AS average_fraud_score

FROM banktransaction

GROUP BY city

ORDER BY fraud_transactions DESC;


-- ============================================================
-- 5. HIGH-RISK TRANSACTIONS
-- ============================================================

DROP VIEW IF EXISTS vw_high_risk_transactions;

CREATE VIEW vw_high_risk_transactions AS
SELECT

    bt.transaction_id,

    bt.reference_number,

    bt.amount,

    bt.transaction_type,

    bt.channel,

    bt.city,

    bt.status,

    bt.fraud_flag,

    bt.fraud_score,

    bt.remarks,

    bt.transaction_time,

    bt.sender_account_id,

    bt.receiver_account_id,

    c.customer_id,

    CONCAT(
        c.first_name,
        ' ',
        c.last_name
    ) AS customer_name,

    d.device_type,

    d.trusted_device

FROM banktransaction bt

JOIN account a
    ON bt.sender_account_id = a.account_id

JOIN customer c
    ON a.customer_id = c.customer_id

JOIN device d
    ON bt.device_id = d.device_id

WHERE bt.fraud_score >= 70

ORDER BY
    bt.fraud_score DESC,
    bt.amount DESC;


-- ============================================================
-- 6. CUSTOMER FRAUD RISK
-- ============================================================

DROP VIEW IF EXISTS vw_customer_fraud_risk;

CREATE VIEW vw_customer_fraud_risk AS
SELECT

    c.customer_id,

    CONCAT(
        c.first_name,
        ' ',
        c.last_name
    ) AS customer_name,

    c.city,

    c.state,

    COUNT(bt.transaction_id)
        AS total_transactions,

    SUM(
        CASE
            WHEN bt.fraud_flag = 1 THEN 1
            ELSE 0
        END
    ) AS fraud_transactions,

    ROUND(
        SUM(bt.amount),
        2
    ) AS total_transaction_amount,

    ROUND(
        SUM(
            CASE
                WHEN bt.fraud_flag = 1
                THEN bt.amount
                ELSE 0
            END
        ),
        2
    ) AS fraud_amount,

    ROUND(
        AVG(bt.fraud_score),
        2
    ) AS average_fraud_score

FROM customer c

JOIN account a
    ON c.customer_id = a.customer_id

JOIN banktransaction bt
    ON a.account_id =
       bt.sender_account_id

GROUP BY

    c.customer_id,
    c.first_name,
    c.last_name,
    c.city,
    c.state

HAVING fraud_transactions > 0

ORDER BY
    fraud_transactions DESC,
    fraud_amount DESC;


-- ============================================================
-- 7. FRAUD ALERT SUMMARY
-- ============================================================

DROP VIEW IF EXISTS vw_alert_summary;

CREATE VIEW vw_alert_summary AS
SELECT

    fa.alert_level,

    fa.status,

    COUNT(*) AS alert_count,

    ROUND(
        AVG(fa.risk_score),
        2
    ) AS average_risk_score,

    ROUND(
        MAX(fa.risk_score),
        2
    ) AS maximum_risk_score

FROM fraudalert fa

GROUP BY

    fa.alert_level,
    fa.status

ORDER BY
    fa.alert_level,
    fa.status;


-- ============================================================
-- 8. DEVICE RISK ANALYSIS
-- ============================================================

DROP VIEW IF EXISTS vw_device_risk;

CREATE VIEW vw_device_risk AS
SELECT

    d.device_id,

    d.customer_id,

    d.device_type,

    d.operating_system,

    d.trusted_device,

    COUNT(bt.transaction_id)
        AS total_transactions,

    SUM(
        CASE
            WHEN bt.fraud_flag = 1
            THEN 1
            ELSE 0
        END
    ) AS fraud_transactions,

    ROUND(
        SUM(bt.amount),
        2
    ) AS total_amount,

    ROUND(
        AVG(bt.fraud_score),
        2
    ) AS average_fraud_score

FROM device d

LEFT JOIN banktransaction bt
    ON d.device_id = bt.device_id

GROUP BY

    d.device_id,
    d.customer_id,
    d.device_type,
    d.operating_system,
    d.trusted_device

HAVING total_transactions > 0

ORDER BY
    fraud_transactions DESC,
    average_fraud_score DESC;


-- ============================================================
-- 9. DAILY FRAUD TREND
-- ============================================================

DROP VIEW IF EXISTS vw_daily_fraud_trend;

CREATE VIEW vw_daily_fraud_trend AS
SELECT
    DATE(transaction_time) AS transaction_date,
    COUNT(*) AS total_transactions,
    SUM(CASE WHEN fraud_flag = 1 THEN 1 ELSE 0 END) AS fraud_transactions,
    SUM(
        CASE
            WHEN fraud_flag = 1 THEN amount
            ELSE 0
        END
    ) AS fraud_amount,
    ROUND(
        AVG(
            CASE
                WHEN fraud_flag = 1 THEN fraud_score
                ELSE NULL
            END
        ),
        2
    ) AS average_fraud_score
FROM banktransaction
GROUP BY DATE(transaction_time)
ORDER BY DATE(transaction_time);


-- ============================================================
-- COMPLETE
-- ============================================================

SELECT
    'FraudLens analytics views created successfully'
    AS message;