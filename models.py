from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Transaction:
    transaction_id: str
    customer: str
    channel: str
    amount: float
    hour: int
    country_mismatch: bool
    device_age: int
    account_age: int
    failed_logins: int
    velocity_24h: int
    merchant_risk: int
    ip_risk: int
    email_age: int
    shipping_distance: int
    chargebacks: int
    card_country_match: bool
    payment_method: str
    label: str = "Unverified"


@dataclass(frozen=True)
class RiskFactor:
    name: str
    points: int
    detail: str


@dataclass(frozen=True)
class RiskResult:
    score: int
    level: str
    action: str
    narrative: str
    factors: tuple[RiskFactor, ...]
