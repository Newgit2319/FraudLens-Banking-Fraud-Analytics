# FraudLens – Machine Learning Model Evaluation Report

## 1. Introduction

The FraudLens Machine Learning module uses a Random Forest Classifier to identify transactions that may be fraudulent.

The model is trained using transaction, behavioral, device, location, and temporal features. The target variable is:

```text
fraud_flag
# FraudLens – Model Evaluation & Performance Documentation

Where:

- **`0`** represents a normal transaction[cite: 1]
- **`1`** represents a fraudulent transaction[cite: 1]

The purpose of this evaluation is to measure how effectively the trained model identifies fraudulent transactions and to understand the trade-offs between detecting fraud and generating false alarms[cite: 1].

---

## 2. Dataset Used for Training

The model was trained using the FraudLens transaction dataset containing:

- **Total transactions:** 30,000[cite: 1]

The data was divided using an 80/20 stratified train-test split[cite: 1].

| Dataset | Records |
| :--- | :--- |
| **Training** | 24,000[cite: 1] |
| **Testing** | 6,000[cite: 1] |

The test set contained:

- **Fraud transactions:** 17[cite: 1]

The stratified split was used to preserve the relative distribution of the fraud and normal classes[cite: 1].

---

## 3. Model Configuration

The selected algorithm is:

`RandomForestClassifier`[cite: 1]

The model configuration was:

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

The `balanced` class-weight setting gives greater importance to the minority fraud class during model training[cite: 1].

---

## 4. Features Used

The model uses the following features:

### Transaction Features
- `amount`[cite: 1]
- `log_amount`[cite: 1]
- `transaction_type`[cite: 1]

### Context Features
- `channel`[cite: 1]
- `city`[cite: 1]

### Device Features
- `device_type`[cite: 1]
- `operating_system`[cite: 1]
- `trusted_device`[cite: 1]

### Temporal Features
- `transaction_hour`[cite: 1]
- `transaction_dayofweek`[cite: 1]
- `is_weekend`[cite: 1]
- `is_night`[cite: 1]

### Behavioral Features
- `is_high_value`[cite: 1]
- `sender_transaction_count`[cite: 1]
- `sender_average_amount`[cite: 1]
- `device_transaction_count`[cite: 1]
- `account_pair_frequency`[cite: 1]

These features represent different characteristics of a banking transaction and its surrounding activity[cite: 1].

---

## 5. Data Leakage Prevention

The following fields were excluded from the model features:

- `fraud_flag`[cite: 1]
- `fraud_score`[cite: 1]

`fraud_flag` is the target variable and therefore cannot be used as an input feature[cite: 1].

`fraud_score` is also excluded because it is an existing fraud-related indicator generated before the ML prediction process[cite: 1].

This prevents the model from directly relying on the target or an existing fraud score when learning transaction patterns[cite: 1].

---

## 6. Evaluation Metrics

The model was evaluated using:

- Precision[cite: 1]
- Recall[cite: 1]
- F1-score[cite: 1]
- ROC-AUC[cite: 1]
- Confusion Matrix[cite: 1]

### Evaluation Results

| Metric | Result |
| :--- | :--- |
| **Precision** | 0.0524[cite: 1] |
| **Recall** | 0.8235[cite: 1] |
| **F1-score** | 0.0986[cite: 1] |
| **ROC-AUC** | 0.9521[cite: 1] |

---

## 7. Precision

- **Precision = 0.0524**[cite: 1]

Precision measures the proportion of transactions predicted as fraud that were actually fraudulent[cite: 1].
The relatively low precision indicates that the model generates a significant number of false-positive fraud predictions[cite: 1].
In practical terms, many transactions flagged by the model would require additional investigation before being classified as confirmed fraud[cite: 1].

---

## 8. Recall

- **Recall = 0.8235**[cite: 1]

Recall measures the proportion of actual fraudulent transactions that were successfully identified by the model[cite: 1].
The test set contained 17 fraudulent transactions, of which the model detected 14[cite: 1].

Therefore:

- **Detected fraud cases:** 14[cite: 1]
- **Missed fraud cases:** 3[cite: 1]

The recall result demonstrates that the model identifies a substantial proportion of the fraud cases present in the test dataset[cite: 1].

---

## 9. F1-score

- **F1-score = 0.0986**[cite: 1]

F1-score combines precision and recall into a single metric[cite: 1].
The relatively low F1-score is primarily influenced by the low precision of the current model[cite: 1].
This indicates that although the model detects many fraud cases, it also produces a considerable number of false-positive predictions[cite: 1].

---

## 10. ROC-AUC

- **ROC-AUC = 0.9521**[cite: 1]

ROC-AUC measures the model's ability to distinguish between the positive and negative classes across different classification thresholds[cite: 1].
The result indicates strong separation between the fraud and normal classes within the evaluated test data[cite: 1].
However, ROC-AUC should not be interpreted independently from precision and recall, particularly because the dataset is highly imbalanced[cite: 1].

---

## 11. Confusion Matrix

The test-set confusion matrix was:

```python
[[5730,  253],
 [   3,   14]]
```[cite: 1]

### Matrix Breakdown

| Actual / Predicted | Normal | Fraud |
| :--- | :--- | :--- |
| **Normal** | 5,730 | 253 |
| **Fraud** | 3 | 14 |

### Summary Results

| Classification Result | Count |
| :--- | :--- |
| **True Negatives (TN)** | 5,730[cite: 1] |
| **False Positives (FP)** | 253[cite: 1] |
| **False Negatives (FN)** | 3[cite: 1] |
| **True Positives (TP)** | 14[cite: 1] |

---

## 12. Confusion Matrix Interpretation

### True Negatives (5,730)
These are normal transactions correctly classified as normal[cite: 1].

### True Positives (14)
These are fraudulent transactions correctly identified as fraud[cite: 1].

### False Positives (253)
These are normal transactions incorrectly classified as fraud[cite: 1]. False positives are the main reason for the low precision observed in the current evaluation[cite: 1].

### False Negatives (3)
These are fraudulent transactions that the model failed to identify[cite: 1]. Reducing false negatives is particularly important in fraud detection because missed fraudulent transactions may require further investigation[cite: 1].

---

## 13. Precision-Recall Trade-off

The model demonstrates an important precision-recall trade-off[cite: 1].

The current results are:

- **Precision:** 0.0524[cite: 1]
- **Recall:** 0.8235[cite: 1]

The model identifies most of the fraud cases in the test set, but it also flags many normal transactions[cite: 1].
This means the current model configuration is oriented toward identifying potential fraud cases rather than minimizing the number of investigations generated by the system[cite: 1].
The appropriate balance between precision and recall would depend on the operational requirements of a real fraud detection environment[cite: 1].

---

## 14. Full Dataset Predictions

After evaluation, the trained model was applied to all 30,000 transactions[cite: 1].

The model generated:

- **Predicted fraud transactions:** 1,311[cite: 1]

This should not be interpreted as 1,311 confirmed fraudulent transactions[cite: 1].
The 1,311 records represent transactions that the ML model classified as potentially fraudulent according to its learned decision boundary[cite: 1].

---

## 15. ML Risk Distribution

The model assigned risk categories to the transactions[cite: 1].

| Risk Level | Number of Transactions |
| :--- | :--- |
| **Low** | 25,779[cite: 1] |
| **Medium** | 3,490[cite: 1] |
| **High** | 650[cite: 1] |
| **Critical** | 81[cite: 1] |
| **Total** | **30,000**[cite: 1] |

The risk distribution provides a more detailed view of the model's output than the binary fraud prediction alone[cite: 1].

---

## 16. Comparison with Rule-Based Fraud Results

The database contains:

- **Confirmed / rule-based fraud transactions:** 84[cite: 1]

The ML model generated:

- **Potential ML fraud predictions:** 1,311[cite: 1]

These figures are different because they represent different analytical mechanisms[cite: 1].

### Rule-Based / Dataset Fraud
The `fraud_flag` field represents the fraud classification available in the project dataset[cite: 1].

### Machine Learning Prediction
The ML model independently evaluates transaction features and generates its own prediction[cite: 1].

Therefore:

$$\text{Confirmed Fraud (84)} \neq \text{Predicted Fraud (1,311)}$$
[cite: 1]

The ML prediction count should not be interpreted as a replacement for the existing fraud labels[cite: 1]. Instead, ML predictions can be used to identify additional transactions for review[cite: 1].

---

## 17. Model Outputs

The training process generated the following files:

```text
models/
├── fraud_model.pkl
├── model_metrics.json
└── confusion_matrix.png

output/
└── ML_Predictions.csv
```[cite: 1]

- **`fraud_model.pkl`**: Contains the trained Random Forest model and associated processing components[cite: 1].
- **`model_metrics.json`**: Contains the model evaluation metrics[cite: 1].
- **`confusion_matrix.png`**: Provides a visual representation of the test-set classification results[cite: 1].
- **`ML_Predictions.csv`**: Contains transaction-level ML predictions and risk information[cite: 1].

---

## 18. Dashboard Integration

The trained model is integrated into the FraudLens Streamlit dashboard[cite: 1].

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

This allows the model results to be explored interactively[cite: 1].

---

## 19. Important Findings

The model evaluation produced several important findings:

- **Finding 1 – Fraud Detection:** The model identified 14 out of 17 fraud cases in the test dataset[cite: 1].
- **Finding 2 – False Positives:** The model produced 253 false positives in the test set[cite: 1].
- **Finding 3 – Recall:** The recall of 0.8235 indicates that most of the fraud cases in the test set were detected[cite: 1].
- **Finding 4 – Precision:** The precision of 0.0524 indicates that a large proportion of model-generated fraud alerts are false positives[cite: 1].
- **Finding 5 – ROC-AUC:** The ROC-AUC of 0.9521 indicates strong class-separation performance on this test set[cite: 1].
- **Finding 6 – Class Imbalance:** Only 17 fraud cases were present in the test set, making the evaluation sensitive to the small number of positive examples[cite: 1].

---

## 20. Limitations of the Evaluation

The evaluation results should be interpreted with the following limitations:

- **Small Number of Fraud Cases:** Only 17 fraud cases were present in the test set[cite: 1]. As a result, small changes in the classification of a few transactions can significantly affect precision, recall, and F1-score[cite: 1].
- **Class Imbalance:** Fraud represents a small fraction of the total dataset[cite: 1]. This makes conventional accuracy less useful as the primary evaluation metric[cite: 1].
- **Single-Date Dataset:** All transactions currently occur on one calendar date[cite: 1]. Therefore, the evaluation does not measure performance across different time periods or changing fraud patterns[cite: 1].
- **Synthetic / Enriched Data:** The dataset is based on PaySim and includes generated banking attributes[cite: 1]. The results therefore should not be interpreted as representative of performance on real-world bank transaction data[cite: 1].
- **Prototype Model:** The model is intended for academic and portfolio demonstration rather than production deployment[cite: 1].

---

## 21. Future Evaluation Improvements

Future versions of FraudLens can improve model evaluation by:

- Increasing the size of the training dataset[cite: 1].
- Adding transactions across multiple dates[cite: 1].
- Using time-based train-test validation[cite: 1].
- Testing additional classification algorithms[cite: 1].
- Performing hyperparameter tuning[cite: 1].
- Optimizing the classification threshold[cite: 1].
- Comparing precision-recall curves[cite: 1].
- Measuring PR-AUC[cite: 1].
- Performing cross-validation where appropriate[cite: 1].
- Evaluating model performance on newly collected data[cite: 1].
- Monitoring changes in fraud patterns over time[cite: 1].

---

## 22. Conclusion

The FraudLens Random Forest model provides an end-to-end demonstration of machine learning-based fraud prediction[cite: 1].

### Final Evaluation Summary
- **Precision:** 0.0524[cite: 1]
- **Recall:** 0.8235[cite: 1]
- **F1-score:** 0.0986[cite: 1]
- **ROC-AUC:** 0.9521[cite: 1]

The model detected 14 of the 17 fraudulent transactions in the test set while producing 253 false positives[cite: 1].

The results demonstrate the practical trade-off between detecting fraudulent transactions and limiting false alarms[cite: 1]. The current model is therefore best viewed as a prototype risk-ranking component that can help prioritize transactions for further investigation rather than as a standalone fraud confirmation system[cite: 1].