from datetime import datetime
from dataclasses import dataclass
from typing import Any

global_sequence = 1

#reference number generator 
def generate_reference_number(transaction_type: str, sequence_value: int) -> str:
    prefix = transaction_type[:3].upper()
    return f"{prefix}-{sequence_value:012d}"


def next_sequence() -> int:
    global global_sequence
    current = global_sequence
    global_sequence += 1
    return current

#transaction info (receipt) 
def create_receipt(transaction_type: str, name: str, amount: float, account_details: str, sequence_value: int) -> dict[str, Any]:
    """Generating The Transaction Receipt..."""
    return {
        "Status": "Success",
        "Transaction Type": transaction_type,
        "Transaction Number": generate_reference_number(transaction_type, sequence_value),
        "Name": name,
        "Amount": amount,
        "Account Details": account_details,
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Time": datetime.now().strftime("%H:%M:%S")
    }


def failed(message: str) -> dict[str, str | None]:
    return {"Status": "Failed", "Message": message, "Data": None}

#amount //checks if the amount is not zero or less than 0
def validate_amount(amount: float) -> bool:
    return amount > 0


# SEND TRANSACTION

#storing account details using data class instead of the usual class declaration
@dataclass
class account_details:
    account_number: str
    account_name: str
    amount: float

#enter account details
def validate_account(account_number: str, account_name: str) -> bool:
    #validation via number or name
    return bool(account_number and account_name)

#confirmation //check transaction details, returns the receipt dictionary
def confirm_transaction(details: account_details) -> dict[str, Any]:
    is_valid_account = validate_account(details.account_number, details.account_name)
    is_valid_amount = validate_amount(details.amount)

    if not (is_valid_account and is_valid_amount):
        return failed("Invalid Transaction")

    return create_receipt(
        transaction_type="Send",
        name=details.account_name,
        amount=details.amount,
        account_details=details.account_number,
        sequence_value=next_sequence()
    )


# PAYMENT TRANSACTION

#bills: government, electricity, internet, water
#bank: loans, transfer
#credits: shopping, games, load
PAYMENT_STRUCTURE = {
    "Bills": ["government", "electricity", "internet", "water"],
    "Bank": ["loans", "transfer"],
    "Credits": ["shopping", "games", "load"]
}

@dataclass
class payment_details:
    category: str
    subcategory: str
    biller: str
    account_reference: str
    amount: float

def validate_payment(details: payment_details) -> bool:
    cat = details.category.capitalize() if details.category else ""
    subcat = details.subcategory.lower() if details.subcategory else ""

    if cat not in PAYMENT_STRUCTURE or subcat not in PAYMENT_STRUCTURE[cat]:
        return False
    if not details.biller or not details.account_reference or not validate_amount(details.amount):
        return False
    return True

def confirm_payment(details: payment_details) -> dict[str, Any]:
    if not validate_payment(details):
        return failed("Invalid Payment Category or Details")

    return create_receipt(
        transaction_type="Payment",
        name=details.biller,
        amount=details.amount,
        account_details=f"Category: {details.category.capitalize()} / Sub: {details.subcategory.title()} / Ref: {details.account_reference}",
        sequence_value=next_sequence()
    )


# DEPOSIT TRANSACTION //amount, confirmation, transaction info

@dataclass
class deposit_details:
    source: str
    account_name: str
    amount: float

def confirm_deposit(details: deposit_details) -> dict[str, Any]:
    if not details.source or not details.account_name or not validate_amount(details.amount):
        return failed("Invalid Deposit Details")

    return create_receipt(
        transaction_type="Deposit",
        name=details.account_name,
        amount=details.amount,
        account_details=f"Source: {details.source}",
        sequence_value=next_sequence()
    )


# WITHDRAW TRANSACTION //amount, confirmation, transaction info

@dataclass
class withdraw_details:
    destination: str
    account_name: str
    account_number: str
    amount: float

def confirm_withdraw(details: withdraw_details) -> dict[str, Any]:
    if not details.destination or not details.account_name or not details.account_number or not validate_amount(details.amount):
        return failed("Invalid Withdrawal Details")

    return create_receipt(
        transaction_type="Withdraw",
        name=details.account_name,
        amount=details.amount,
        account_details=f"Destination: {details.destination} / Account No: {details.account_number}",
        sequence_value=next_sequence()
    )