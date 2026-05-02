# E-Fraud Detection Project Report

## Title

E-Fraud Sentinel: Explainable Online Transaction Fraud Detection System Using Python

## Abstract

E-Fraud Sentinel is a Python-based fraud detection system for online payment transactions. The project evaluates each transaction using transaction, account, device, location, and behavior signals. It assigns a risk score from 0 to 100 and recommends one of four actions: approve, step-up authentication, manual review, or block and escalate. The system includes a Python scoring model, a browser dashboard served through Python, a synthetic dataset, testing, and a PowerPoint presentation.

## Problem Statement

Online payment platforms face fraud attempts such as stolen card usage, account takeover, fake accounts, suspicious international purchases, high-velocity checkout abuse, and chargeback fraud. Manual review is slow and may miss risky patterns. A fraud detection system is needed to identify suspicious transactions early while allowing legitimate users to complete payments smoothly.

## Objectives

- Detect suspicious online transactions before settlement.
- Reduce financial loss from fraudulent payments.
- Provide explainable fraud evidence for every decision.
- Support analysts with a ranked review queue.
- Build the project in Python with a clean and study-friendly structure.

## Technologies Used

| Component | Technology |
| --- | --- |
| Programming language | Python 3 |
| Web server | Python standard library `http.server` |
| Data model | Python dataclasses |
| Testing | Python `unittest` |
| Frontend rendering | Server-generated HTML and CSS |
| Dataset | Synthetic CSV and Python sample data |

## Proposed System

The proposed system uses a transparent rule-weighted risk model. Each transaction starts with a base score. Fraud indicators add points, and trusted behavior signals subtract points. The final score is limited to a 0-100 range and mapped to a decision threshold.

## System Modules

1. Dashboard
   - Displays total transactions, high-risk cases, average risk score, auto-approval rate, risk distribution, channel exposure, and review queue.

2. Transaction Check
   - Allows the user to enter transaction details.
   - Calculates fraud risk using the Python model.
   - Displays the strongest risk evidence.

3. Case Dataset
   - Shows synthetic online payment cases.
   - Supports search, filtering, and case inspection.

4. Model Study
   - Explains architecture, features, thresholds, and sample evaluation metrics.

5. API Endpoint
   - `/api/score` returns JSON output for a transaction risk calculation.

## Input Features

| Feature | Purpose |
| --- | --- |
| Amount | Detects unusually large purchases or transfers. |
| Hour | Highlights transactions made at unusual times. |
| Payment method | Measures payment reversibility and identity distance. |
| Channel | Identifies checkout, wallet, transfer, or marketplace context. |
| Device age | New devices are riskier than trusted devices. |
| Account age | New accounts have less trust history. |
| Email age | Fresh email identities may indicate fake identity usage. |
| Failed logins | Repeated failures can indicate account takeover. |
| 24h velocity | Many recent transactions can indicate automated abuse. |
| Merchant risk | Represents merchant dispute and abuse history. |
| IP risk | Captures proxy, VPN, abuse, and location risk. |
| Shipping distance | Large billing-to-shipping distance can indicate reshipping fraud. |
| Chargebacks | Past chargebacks increase future fraud risk. |
| Country mismatch | Flags mismatch between billing, card, IP, or shipping region. |
| Card country match | Rewards consistency between card country and transaction region. |

## Scoring Logic

The model calculates a score using weighted indicators:

- High amount increases risk.
- Country mismatch increases risk.
- New account, new device, and new email increase risk.
- Failed logins and high transaction velocity increase risk.
- High merchant risk and IP risk increase risk.
- Shipping distance and chargeback history increase risk.
- Mature account, trusted device, and region consistency reduce risk.

## Decision Thresholds

| Score Range | Level | Action |
| --- | --- | --- |
| 0-34 | Low | Approve with monitoring |
| 35-54 | Watch | Step-up authentication |
| 55-74 | High | Manual review required |
| 75-100 | Critical | Block and escalate |

## Evaluation

The project includes a synthetic dataset of online payment cases. The sample evaluation uses a fraud threshold of 55 and displays:

- True fraud alerts
- False alerts
- Missed fraud cases
- Correct approvals
- Accuracy
- Precision
- Recall

The dataset is for academic demonstration. A production system should use real labeled transaction data and should be validated carefully before deployment.

## Advantages

- Built in Python.
- Runs without external packages.
- Clean browser interface.
- Explainable scoring.
- Easy to study and present.
- Includes tests and documentation.
- Can be upgraded into a machine learning project.

## Limitations

- Uses synthetic data.
- Uses weighted rules instead of a trained model.
- Does not connect to a real payment gateway.
- Does not include database persistence.
- Does not include live identity verification.

## Future Enhancements

- Train a supervised machine learning model using real fraud labels.
- Add anomaly detection for new fraud patterns.
- Store transaction history in a database.
- Add investigator notes and case assignment.
- Add OTP, email, biometric, or device verification.
- Integrate with a payment gateway sandbox.

## Conclusion

E-Fraud Sentinel demonstrates a complete Python-based fraud detection workflow. It combines risk scoring, explainability, dashboard monitoring, transaction review, dataset evaluation, and presentation material in a clean project structure. The system is suitable for academic submission, demonstration, and future machine learning expansion.
