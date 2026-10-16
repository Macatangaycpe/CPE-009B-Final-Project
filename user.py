from dataclasses import dataclass
from datetime import datetime


def create_receipt(transaction_type, name, amount, account_details, sequence_value):
    now = datetime.now()
    return {
        "Status": "Success",
        "Transaction Type": transaction_type,
        "Transaction Number": f"{transaction_type[:3].upper()}-{sequence_value:09d}",
        "Name": name,
        "Amount": amount,
        "Account Details": account_details,
        "Date": now.strftime("%Y-%m-%d"),
        "Time": now.strftime("%H:%M:%S"),
    }


# Each confirm_* function checks the details and returns a receipt.
# Invalid details raise ValueError.

# PAYMENT

PAYMENT_STRUCTURE = {
    "Bills": ["government", "electricity", "internet", "water"],
    "Bank": ["loans", "transfer"],
    "Credits": ["shopping", "games", "load"],
}


@dataclass
class payment_details:
    category: str
    subcategory: str
    biller: str
    account_reference: str
    amount: float


def confirm_payment(details, sequence_value):
    category = details.category.capitalize()
    subcategory = details.subcategory.lower()
    if subcategory not in PAYMENT_STRUCTURE.get(category, []):
        raise ValueError("Invalid payment category.")
    if not details.biller or not details.account_reference or details.amount <= 0:
        raise ValueError("Invalid payment details.")
    return create_receipt(
        "Payment", details.biller, details.amount,
        f"Category: {category} / Sub: {subcategory.title()} / Ref: {details.account_reference}",
        sequence_value,
    )


# SEND

@dataclass
class account_details:
    account_number: str
    account_name: str
    amount: float


def confirm_transaction(details, sequence_value):
    if not details.account_number or not details.account_name or details.amount <= 0:
        raise ValueError("Invalid send details.")
    return create_receipt(
        "Send", details.account_name, details.amount,
        details.account_number, sequence_value,
    )


# DEPOSIT

@dataclass
class deposit_details:
    source: str
    account_name: str
    amount: float


def confirm_deposit(details, sequence_value):
    if not details.source or not details.account_name or details.amount <= 0:
        raise ValueError("Invalid deposit details.")
    return create_receipt(
        "Deposit", details.account_name, details.amount,
        f"Source: {details.source}", sequence_value,
    )


# WITHDRAW

@dataclass
class withdraw_details:
    destination: str
    account_name: str
    account_number: str
    amount: float


def confirm_withdraw(details, sequence_value):
    if (not details.destination or not details.account_name
            or not details.account_number or details.amount <= 0):
        raise ValueError("Invalid withdrawal details.")
    return create_receipt(
        "Withdraw", details.account_name, details.amount,
        f"Destination: {details.destination} / Account No: {details.account_number}",
        sequence_value,
    )