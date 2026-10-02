# FraudLens – Machine Learning Documentation

## 1. Overview

FraudLens uses a Machine Learning module to identify banking transactions that may be fraudulent and assign risk levels to transactions.

The ML pipeline uses a **Random Forest Classifier** trained on transaction-level features derived from the FraudLens banking transaction dataset.

The model predicts the target variable:

```text
fraud_flag
Where:

- **`0`** = Normal transaction[cite: 1]
- **`1`** = Fraudulent transaction[cite: 1]

The trained model is also integrated into the Streamlit dashboard to display transaction risk predictions and probability-based risk categories[cite: 1].

---

## 2. Machine Learning Objective

The objective of the ML module is to:

- Detect potentially fraudulent banking transactions[cite: 1].
- Learn patterns associated with fraudulent transactions[cite: 1].
- Generate fraud probability scores for transactions[cite: 1].
- Categorize transactions into different risk levels[cite: 1].
- Provide risk information for investigation through the dashboard[cite: 1].
- Demonstrate how machine learning can complement SQL-based fraud analytics[cite: 1].

The model is intended as a portfolio/prototype fraud detection system, not as a production banking fraud detection solution[cite: 1].

---

## 3. Dataset

The model uses the FraudLens transaction dataset generated from the PaySim-based source dataset[cite: 1].

### Dataset Size
- **Total transactions:** 30,000[cite: 1]

The dataset contains transaction, customer, account, device, channel, location, and behavioral information[cite: 1].

The target variable is:

`fraud_flag`[cite: 1]

The dataset contains relatively few fraudulent transactions compared with normal transactions, making fraud detection an imbalanced classification problem[cite: 1].

---

## 4. Target Variable

The classification target is:

`fraud_flag`[cite: 1]

### Target Interpretation

| Value | Meaning |
| :--- | :--- |
| **0** | Normal transaction[cite: 1] |
| **1** | Fraudulent transaction[cite: 1] |

The model learns patterns in transaction and behavioral features to predict whether a transaction belongs to the fraud class[cite: 1].

---

## 5. Feature Engineering

The model uses transaction-level, behavioral, device, and contextual features[cite: 1].

### Transaction Features
- `amount`[cite: 1]
- `log_amount`[cite: 1]
- `transaction_type`[cite: 1]

`log_amount` is derived from the transaction amount to provide a transformed representation of transaction value[cite: 1].

### Channel and Location Features
- `channel`[cite: 1]
- `city`[cite: 1]

These features provide contextual information about how and where a transaction occurred[cite: 1].

### Device Features
- `device_type`[cite: 1]
- `operating_system`[cite: 1]
- `trusted_device`[cite: 1]

These features help represent the device context associated with a transaction[cite: 1].

### Time Features
The transaction timestamp is transformed into:

- `transaction_hour`[cite: 1]
- `transaction_dayofweek`[cite: 1]
- `is_weekend`[cite: 1]
- `is_night`[cite: 1]

These features allow the model to identify potentially unusual transaction timing patterns[cite: 1].

### Transaction Behavior Features
- `is_high_value`[cite: 1]
- `sender_transaction_count`[cite: 1]
- `sender_average_amount`[cite: 1]
- `device_transaction_count`[cite: 1]
- `account_pair_frequency`[cite: 1]

These features capture transaction frequency, historical transaction behavior, device activity, and repeated account-pair relationships[cite: 1].

---

## 6. Prevention of Data Leakage

Two existing fraud-related fields were deliberately excluded from the ML feature set:

- `fraud_flag`[cite: 1]
- `fraud_score`[cite: 1]

`fraud_flag` is the prediction target and therefore cannot be used as an input feature[cite: 1].

`fraud_score` was also excluded because it is an existing rule-based fraud indicator[cite: 1]. Including it as a feature could allow the model to rely directly on an already-derived fraud signal rather than learning independently from the underlying transaction characteristics[cite: 1].

Therefore, the ML model learns from transaction, behavioral, device, time, and contextual features[cite: 1].

---

## 7. Machine Learning Pipeline

The ML workflow is:

```text
BankTransaction Data
        |
        v
Feature Selection
        |
        v
Feature Engineering
        |
        v
Categorical / Numerical Processing
        |
        v
Train-Test Split
        |
        v
Random Forest Classifier
        |
        v
Fraud Probability Prediction
        |
        v
Risk Classification
        |
        v
ML_Predictions.csv
        |
        v
Streamlit Dashboard
```[cite: 1]

---

## 8. Train-Test Split

The dataset is divided into training and testing subsets[cite: 1].

### Configuration
- **Training data:** 80%[cite: 1]
- **Testing data:** 20%[cite: 1]

The split is stratified to preserve the distribution of the fraud and normal classes[cite: 1].

### Actual Records
- **Training records:** 24,000[cite: 1]
- **Testing records:** 6,000[cite: 1]

The test dataset contained:

- **Fraudulent transactions:** 17[cite: 1]

This relatively small fraud count is an important limitation when interpreting classification metrics[cite: 1].

---

## 9. Model Used

FraudLens uses:

`RandomForestClassifier`[cite: 1]

Random Forest is an ensemble learning algorithm that combines multiple decision trees to make a classification decision[cite: 1].

### Model Configuration

```python
RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    min_samples_leaf=2,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)
```[cite: 1]

### Explanation
- **`n_estimators = 300`**: Uses 300 decision trees[cite: 1].
- **`max_depth = 12`**: Limits the maximum depth of individual trees[cite: 1].
- **`min_samples_leaf = 2`**: Requires at least two samples in a leaf node[cite: 1].
- **`class_weight = balanced`**: Gives additional importance to the minority fraud class during training[cite: 1].
- **`random_state = 42`**: Provides reproducible results[cite: 1].
- **`n_jobs = -1`**: Allows the model to use available CPU cores during training[cite: 1].

---

## 10. Model Evaluation

The model was evaluated using:

- Precision[cite: 1]
- Recall[cite: 1]
- F1-score[cite: 1]
- ROC-AUC[cite: 1]
- Confusion Matrix[cite: 1]

### Test Results

| Metric | Result |
| :--- | :--- |
| **Precision** | 0.0524[cite: 1] |
| **Recall** | 0.8235[cite: 1] |
| **F1-score** | 0.0986[cite: 1] |
| **ROC-AUC** | 0.9521[cite: 1] |

### Interpretation
- The model detected a large proportion of the fraudulent transactions in the test set[cite: 1].
- The recall of **0.8235** means that the model detected approximately 82.35% of the fraud cases in the test set[cite: 1].
- However, precision was relatively low at **0.0524**[cite: 1]. This means that many transactions predicted as fraud were actually normal transactions[cite: 1].
- Therefore, the current model is more effective at finding potential fraud cases than at producing a small, highly precise set of fraud alerts[cite: 1].
- This trade-off is important for interpreting the model's results[cite: 1].

---

## 11. Confusion Matrix

The test-set confusion matrix was:

```python
[[5730,  253],
 [   3,   14]]
```[cite: 1]

### Matrix Interpretation

| | Predicted Normal | Predicted Fraud |
| :--- | :--- | :--- |
| **Actual Normal** | 5,730 | 253 |
| **Actual Fraud** | 3 | 14 |

Therefore:

- **True Negatives (TN):** 5,730[cite: 1]
- **False Positives (FP):** 253[cite: 1]
- **False Negatives (FN):** 3[cite: 1]
- **True Positives (TP):** 14[cite: 1]

The model detected 14 of the 17 fraudulent transactions in the test set[cite: 1].

---

## 12. Full Dataset Prediction

After training and evaluation, the trained model was applied to the complete set of 30,000 transactions[cite: 1].

The model predicted:

- **Predicted fraud transactions:** 1,311[cite: 1]

### Risk Distribution

| Risk Level | Transactions |
| :--- | :--- |
| **Low** | 25,779[cite: 1] |
| **Medium** | 3,490[cite: 1] |
| **High** | 650[cite: 1] |
| **Critical** | 81[cite: 1] |

These risk categories are based on the probability generated by the trained classification model[cite: 1].

The predicted fraud count is higher than the actual rule-based fraud count because the ML model identifies transactions that it considers potentially suspicious based on learned patterns[cite: 1]. These predictions therefore require investigation rather than being treated as confirmed fraud[cite: 1].

---

## 13. Model Outputs

The training process generates the following files:

### Trained Model
`models/fraud_model.pkl`[cite: 1]  
Contains the trained Random Forest model and processing components required for prediction[cite: 1].

### Model Metrics
`models/model_metrics.json`[cite: 1]  
Stores the evaluation metrics generated during model training[cite: 1].

### Confusion Matrix
`models/confusion_matrix.png`[cite: 1]  
Provides a visual representation of classification results[cite: 1].

### ML Predictions
`output/ML_Predictions.csv`[cite: 1]  
Contains transaction-level ML predictions and risk information used by the dashboard[cite: 1].

---

## 14. Dashboard Integration

The trained ML model is integrated with the FraudLens Streamlit dashboard[cite: 1].

The **ML Risk Analysis** page displays:

- Total transactions[cite: 1]
- Predicted fraud transactions[cite: 1]
- High-risk transactions[cite: 1]
- Critical-risk transactions[cite: 1]
- Precision[cite: 1]
- Recall[cite: 1]
- F1-score[cite: 1]
- ROC-AUC[cite: 1]
- Risk distribution[cite: 1]
- Fraud probability distribution[cite: 1]
- Highest-risk transactions[cite: 1]
- Confusion matrix[cite: 1]
- Model information[cite: 1]

This allows users to examine both the overall model performance and individual transaction risk[cite: 1].

---

## 15. Risk Classification

The model produces a probability associated with the fraud class[cite: 1].
This probability is used to categorize transactions into risk levels:

- Low[cite: 1]
- Medium[cite: 1]
- High[cite: 1]
- Critical[cite: 1]

The risk category provides a more understandable representation of the numerical model output and can be used by analysts to prioritize transactions for investigation[cite: 1].

A high or critical ML risk prediction does not automatically mean that a transaction is confirmed fraudulent[cite: 1].

---

## 16. SQL and ML Integration

FraudLens combines SQL analytics with machine learning[cite: 1].

### SQL Layer
SQL views provide:

- Fraud summaries[cite: 1]
- Fraud by transaction type[cite: 1]
- Fraud by channel[cite: 1]
- Fraud by location[cite: 1]
- High-risk transactions[cite: 1]
- Customer fraud risk[cite: 1]
- Alert summaries[cite: 1]
- Device risk[cite: 1]
- Daily/date-based fraud analysis[cite: 1]
- Login risk[cite: 1]

### ML Layer
Machine learning provides:

- Fraud probability[cite: 1]
- Predicted fraud class[cite: 1]
- Risk classification[cite: 1]
- Behavioral pattern detection[cite: 1]
- Model-based transaction prioritization[cite: 1]

The combination provides both rule/query-based analysis and predictive analysis[cite: 1].

---

## 17. Model Limitations

The current model has several limitations:

- **Limited Dataset Size:** The model is trained using 30,000 transaction records[cite: 1]. A production fraud detection system would normally require much larger and continuously updated transaction data[cite: 1].
- **Class Imbalance:** Fraud represents a small portion of the dataset[cite: 1]. This makes the classification problem highly imbalanced and can make metrics such as accuracy less informative[cite: 1].
- **False Positives:** The current model produces a relatively large number of false positives[cite: 1]. The precision of 0.0524 indicates that many transactions classified as fraud are actually normal[cite: 1].
- **Single Transaction Date:** The current transaction dataset contains transactions on one calendar date[cite: 1]. Therefore, the project cannot currently demonstrate genuine multi-day or long-term temporal fraud trends[cite: 1].
- **Synthetic / Enriched Data:** The project is based on a PaySim-derived dataset with additional generated banking entities and attributes[cite: 1]. It does not represent a real bank's confidential transaction environment[cite: 1].
- **Prototype Model:** The model is designed for academic and portfolio demonstration[cite: 1]. It should not be treated as a production-ready banking fraud detection system without additional validation, monitoring, security controls, threshold tuning, and real-world data[cite: 1].

---

## 18. Future Improvements

Potential improvements include:

- Training with a larger and more diverse transaction dataset[cite: 1].
- Collecting transactions across multiple dates and longer time periods[cite: 1].
- Hyperparameter tuning[cite: 1].
- Optimizing the classification threshold for the required precision-recall trade-off[cite: 1].
- Testing additional algorithms such as XGBoost or LightGBM[cite: 1].
- Applying advanced imbalance-handling techniques[cite: 1].
- Adding more behavioral and temporal features[cite: 1].
- Implementing model monitoring and drift detection[cite: 1].
- Periodically retraining the model with new confirmed fraud cases[cite: 1].
- Adding explainable AI techniques to show why a transaction received a high-risk prediction[cite: 1].
- Evaluating the model using time-based validation for realistic transaction-stream scenarios[cite: 1].

---

## 19. Conclusion

The FraudLens Machine Learning module demonstrates an end-to-end fraud prediction workflow using transaction, behavioral, device, location, and temporal features[cite: 1].

A Random Forest classifier is trained using a stratified 80/20 train-test split and evaluated using precision, recall, F1-score, ROC-AUC, and a confusion matrix[cite: 1].

The model achieved a ROC-AUC of **0.9521** and recall of **0.8235** on the test set, while its precision of **0.0524** shows that the current model generates a substantial number of false positives[cite: 1].

The resulting ML predictions are integrated into the FraudLens Streamlit dashboard, allowing users to explore transaction risk and prioritize potentially suspicious transactions for further investigation[cite: 1].