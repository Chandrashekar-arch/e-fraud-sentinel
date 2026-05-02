from __future__ import annotations

from .models import Transaction


SAMPLE_TRANSACTIONS: tuple[Transaction, ...] = (
    Transaction("TXN-1001", "Asha Mehta", "Checkout", 42.50, 14, False, 380, 760, 0, 1, 8, 4, 680, 12, 0, True, "Card", "Legit"),
    Transaction("TXN-1002", "Rohan Kapoor", "Wallet", 1280, 2, True, 2, 9, 3, 9, 82, 91, 4, 2880, 1, False, "Wallet", "Fraud"),
    Transaction("TXN-1003", "Neha Rao", "Checkout", 315, 10, False, 210, 380, 0, 2, 22, 15, 350, 34, 0, True, "Card", "Legit"),
    Transaction("TXN-1004", "Omar Singh", "Transfer", 4920, 23, True, 16, 22, 2, 6, 68, 76, 18, 1920, 0, False, "Bank", "Fraud"),
    Transaction("TXN-1005", "Isha Nair", "Subscription", 19.99, 9, False, 560, 890, 0, 1, 10, 8, 820, 0, 0, True, "Card", "Legit"),
    Transaction("TXN-1006", "Dev Patel", "Marketplace", 780, 18, False, 25, 43, 1, 5, 48, 39, 65, 510, 0, True, "Wallet", "Legit"),
    Transaction("TXN-1007", "Mira Shah", "Checkout", 6320, 1, True, 1, 3, 5, 14, 88, 96, 2, 4150, 2, False, "Crypto", "Fraud"),
    Transaction("TXN-1008", "Arjun Das", "Bill Pay", 96, 16, False, 330, 510, 0, 2, 16, 12, 590, 7, 0, True, "Bank", "Legit"),
    Transaction("TXN-1009", "Sara Thomas", "Checkout", 1450, 3, True, 6, 12, 1, 7, 74, 69, 6, 1320, 0, False, "Card", "Fraud"),
    Transaction("TXN-1010", "Kabir Sen", "Marketplace", 249, 20, False, 180, 260, 0, 3, 34, 22, 190, 88, 0, True, "Wallet", "Legit"),
    Transaction("TXN-1011", "Priya Iyer", "Checkout", 2190, 4, True, 13, 31, 4, 10, 79, 88, 11, 2420, 1, False, "Card", "Fraud"),
    Transaction("TXN-1012", "Anil Verma", "Recharge", 16, 12, False, 720, 940, 0, 1, 6, 5, 860, 0, 0, True, "Wallet", "Legit"),
    Transaction("TXN-1013", "Fatima Khan", "Checkout", 875, 15, False, 62, 155, 1, 4, 42, 34, 140, 260, 0, True, "Card", "Legit"),
    Transaction("TXN-1014", "Vikram Menon", "Transfer", 3780, 0, True, 4, 17, 2, 8, 71, 81, 9, 1760, 0, False, "Bank", "Fraud"),
    Transaction("TXN-1015", "Elena Dsouza", "Subscription", 59, 11, False, 450, 620, 0, 1, 14, 10, 600, 0, 0, True, "Card", "Legit"),
    Transaction("TXN-1016", "Jay Bhat", "Marketplace", 1150, 19, False, 18, 48, 1, 5, 54, 46, 31, 840, 0, True, "Wallet", "Legit"),
    Transaction("TXN-1017", "Tara Bose", "Checkout", 5125, 2, True, 3, 5, 4, 13, 93, 94, 1, 3600, 2, False, "Crypto", "Fraud"),
    Transaction("TXN-1018", "Kiran Paul", "Bill Pay", 130, 8, False, 290, 490, 0, 2, 18, 17, 410, 18, 0, True, "Bank", "Legit"),
    Transaction("TXN-1019", "Sonal Jain", "Checkout", 980, 21, True, 10, 26, 2, 6, 66, 71, 14, 1120, 1, False, "Card", "Fraud"),
    Transaction("TXN-1020", "Manav Ghosh", "Recharge", 24, 13, False, 610, 780, 0, 1, 7, 6, 700, 0, 0, True, "Wallet", "Legit"),
    Transaction("TXN-1021", "Leah Fernandes", "Marketplace", 470, 17, False, 88, 120, 0, 3, 35, 28, 95, 145, 0, True, "Card", "Legit"),
    Transaction("TXN-1022", "Nikhil Roy", "Transfer", 2890, 23, True, 8, 18, 3, 9, 76, 83, 7, 2050, 1, False, "Bank", "Fraud"),
    Transaction("TXN-1023", "Meera Lal", "Checkout", 690, 16, False, 120, 200, 0, 3, 29, 21, 180, 75, 0, True, "Card", "Legit"),
    Transaction("TXN-1024", "Sameer Ali", "Wallet", 1640, 5, True, 12, 37, 2, 7, 63, 73, 12, 1580, 0, False, "Wallet", "Fraud"),
)


DEFAULT_TRANSACTION = Transaction(
    "LIVE-CHECK",
    "Live Customer",
    "Checkout",
    1499,
    1,
    True,
    3,
    9,
    2,
    7,
    72,
    84,
    5,
    2100,
    1,
    False,
    "Card",
)
