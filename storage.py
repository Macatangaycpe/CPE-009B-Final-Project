import json
import os
import tempfile
from datetime import date

from user import User, register
from transaction import (confirm_deposit, confirm_withdraw,
                         confirm_transaction, confirm_payment)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "users.json")
TRANSACTIONS_FILE = os.path.join(BASE_DIR, "transactions.json")


class StorageError(Exception):
    """Raised when a data file is corrupted or in an unexpected format."""


# low-level file helpers

def _load(filename):
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        backup = filename + ".bak"
        os.replace(filename, backup)
        raise StorageError(f"{os.path.basename(filename)} is corrupted. "
                           f"A copy was saved as {os.path.basename(backup)}.")
    if not isinstance(data, list):
        raise StorageError(f"{os.path.basename(filename)} must contain a JSON list.")
    return data


def _save(filename, data):
    # write to a temp file first, then swap it in, so a crash can't leave half a file
    fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(filename), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        os.replace(temp_path, filename)
    except Exception:
        os.remove(temp_path)
        raise


# users

def load_users():
    try:
        return [User.fromDict(d) for d in _load(USERS_FILE)]
    except (KeyError, TypeError, AttributeError):
        raise StorageError("users.json is not in the expected format.")


def save_users(users):
    _save(USERS_FILE, [u.toDict() for u in users])


# transactions

def load_transactions():
    return _load(TRANSACTIONS_FILE)


def next_transaction_id():
    return max((t["transaction_id"] for t in load_transactions()), default=0) + 1


def add_transaction(mobile_number, txn_type, amount):
    txn = {
        "transaction_id": next_transaction_id(),
        "mobile_number": User.normalize_mobile(mobile_number),
        "type": txn_type,
        "amount": round(float(amount), 2),
        "date": date.today().isoformat(),
    }
    _save(TRANSACTIONS_FILE, load_transactions() + [txn])
    return txn


def get_transactions(mobile_number):
    mobile = User.normalize_mobile(mobile_number)
    return [t for t in load_transactions() if t["mobile_number"] == mobile]


# actions: validate -> change balance -> save -> log -> return receipt

def _process(user, users, txn_type, details, confirm, change_balance):
    receipt = confirm(details, next_transaction_id())  # raises ValueError if invalid
    change_balance(details.amount)  # raises InsufficientFundsError before anything is saved
    save_users(users)
    add_transaction(user.mobile_number, txn_type, details.amount)
    return receipt


def register_and_save(name, mobile_number, pin, users):
    user = register(name, mobile_number, pin, users)
    save_users(users)
    return user


def deposit_and_save(user, details, users):
    return _process(user, users, "deposit", details, confirm_deposit, user.deposit)


def withdraw_and_save(user, details, users):
    return _process(user, users, "withdrawal", details, confirm_withdraw, user.withdraw)


def send_and_save(user, details, users):
    return _process(user, users, "send", details, confirm_transaction, user.withdraw)


def pay_and_save(user, details, users):
    return _process(user, users, "payment", details, confirm_payment, user.withdraw)