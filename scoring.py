from __future__ import annotations

from collections import Counter
from typing import Iterable

from .models import RiskFactor, RiskResult, Transaction


def clamp(value: float, minimum: int = 0, maximum: int = 100) -> int:
    return round(min(max(value, minimum), maximum))


def money(value: float) -> str:
    return f"Rs. {value:,.2f}" if value < 100 else f"Rs. {value:,.0f}"


def compute_risk(transaction: Transaction) -> RiskResult:
    factors: list[RiskFactor] = []

    def add(name: str, points: float, detail: str) -> None:
        rounded = round(points)
        if rounded:
            factors.append(RiskFactor(name, rounded, detail))

    base_score = 8

    if transaction.amount >= 5000:
        add("High-value transaction", 18, f"{money(transaction.amount)} exceeds the emergency review band.")
    elif transaction.amount >= 2000:
        add("Elevated amount", 12, f"{money(transaction.amount)} is above normal checkout behavior.")
    elif transaction.amount >= 1000:
        add("Medium-high amount", 7, f"{money(transaction.amount)} is above the routine threshold.")

    if transaction.country_mismatch:
        add("Country mismatch", 16, "Billing country, IP country, or shipping country do not align.")
    if not transaction.card_country_match:
        add("Card country mismatch", 9, "Issued card country differs from the transaction region.")

    if transaction.device_age <= 7:
        add("New device", 12, f"{transaction.device_age} day device history.")
    elif transaction.device_age <= 30:
        add("Recently seen device", 6, f"{transaction.device_age} day device history.")
    elif transaction.device_age >= 180:
        add("Trusted device age", -3, f"{transaction.device_age} days of device reputation.")

    if transaction.account_age <= 14:
        add("New account", 11, f"{transaction.account_age} day account age.")
    elif transaction.account_age <= 60:
        add("Young account", 5, f"{transaction.account_age} day account age.")
    elif transaction.account_age >= 365:
        add("Mature account", -4, f"{transaction.account_age} days of account history.")

    add("Failed login signal", min(transaction.failed_logins * 4, 14), f"{transaction.failed_logins} failed login attempts near checkout.")

    if transaction.velocity_24h >= 10:
        add("Velocity spike", 16, f"{transaction.velocity_24h} transactions in the last 24 hours.")
    elif transaction.velocity_24h >= 5:
        add("Raised velocity", 9, f"{transaction.velocity_24h} transactions in the last 24 hours.")

    add("Merchant risk index", transaction.merchant_risk * 0.18, f"{transaction.merchant_risk}/100 merchant dispute and abuse score.")
    add("IP reputation index", transaction.ip_risk * 0.20, f"{transaction.ip_risk}/100 proxy, abuse, and location risk score.")

    if transaction.email_age <= 7:
        add("New email identity", 8, f"{transaction.email_age} day email age.")
    elif transaction.email_age <= 30:
        add("Young email identity", 4, f"{transaction.email_age} day email age.")

    if transaction.shipping_distance >= 2500:
        add("Long shipping jump", 15, f"{transaction.shipping_distance} km between billing and delivery regions.")
    elif transaction.shipping_distance >= 1000:
        add("Shipping distance risk", 9, f"{transaction.shipping_distance} km between billing and delivery regions.")

    add("Chargeback history", min(transaction.chargebacks * 10, 20), f"{transaction.chargebacks} previous chargeback records.")

    if transaction.hour <= 5 or transaction.hour >= 23:
        add("Unusual hour", 4, f"{transaction.hour:02d}:00 transaction time.")

    if transaction.payment_method == "Crypto":
        add("Crypto settlement", 8, "Low reversibility payment rail.")
    elif transaction.payment_method == "Wallet":
        add("Wallet payment", 3, "Wallet flow adds moderate identity distance.")

    if not transaction.country_mismatch and transaction.card_country_match:
        add("Region consistency", -2, "Billing, card, and network region are aligned.")

    score = clamp(base_score + sum(factor.points for factor in factors))
    level = "Low"
    action = "Approve with monitoring"
    narrative = "Risk indicators are within the normal payment range."

    if score >= 75:
        level = "Critical"
        action = "Block and escalate"
        narrative = "Multiple high-confidence fraud indicators align in the same transaction."
    elif score >= 55:
        level = "High"
        action = "Manual review required"
        narrative = "The transaction should be held until ownership signals are verified."
    elif score >= 35:
        level = "Watch"
        action = "Step-up authentication"
        narrative = "The transaction is plausible but needs stronger customer verification."

    return RiskResult(
        score=score,
        level=level,
        action=action,
        narrative=narrative,
        factors=tuple(sorted(factors, key=lambda factor: abs(factor.points), reverse=True)),
    )


def summarize_transactions(transactions: Iterable[Transaction]) -> dict[str, object]:
    rows = list(transactions)
    scores = [compute_risk(transaction) for transaction in rows]
    bucket_counts = Counter(result.level for result in scores)
    high_risk = sum(1 for result in scores if result.score >= 55)
    critical = sum(1 for result in scores if result.score >= 75)
    auto_approval = sum(1 for result in scores if result.score < 35)
    average_score = round(sum(result.score for result in scores) / max(len(scores), 1))

    return {
        "total": len(rows),
        "high_risk": high_risk,
        "critical": critical,
        "auto_approval_rate": auto_approval / max(len(scores), 1),
        "average_score": average_score,
        "buckets": {level: bucket_counts.get(level, 0) for level in ("Low", "Watch", "High", "Critical")},
    }


def evaluate_dataset(transactions: Iterable[Transaction], fraud_threshold: int = 55) -> dict[str, float | int]:
    true_positive = false_positive = false_negative = true_negative = 0

    for transaction in transactions:
        predicted_fraud = compute_risk(transaction).score >= fraud_threshold
        actual_fraud = transaction.label == "Fraud"
        if predicted_fraud and actual_fraud:
            true_positive += 1
        elif predicted_fraud and not actual_fraud:
            false_positive += 1
        elif not predicted_fraud and actual_fraud:
            false_negative += 1
        else:
            true_negative += 1

    total = true_positive + false_positive + false_negative + true_negative
    accuracy = (true_positive + true_negative) / max(total, 1)
    precision = true_positive / max(true_positive + false_positive, 1)
    recall = true_positive / max(true_positive + false_negative, 1)

    return {
        "true_positive": true_positive,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "true_negative": true_negative,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
    }
