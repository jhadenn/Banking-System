from enum import Enum

from print_error import log_constraint_error


class TransactionCode(Enum):
    """Represents the different types of transactions that can be performed in the banking system."""

    WITHDRAWAL = "01"
    TRANSFER = "02"
    PAYBILL = "03"
    DEPOSIT = "04"
    CREATE = "05"
    DELETE = "06"
    DISABLE = "07"
    CHANGEPLAN = "08"


def apply_transactions(accounts, transactions):
    """Applies transactions to accounts and returns the updated accounts list"""

    for transaction in transactions:
        transaction_code = transaction["transaction_code"]
        account_name = transaction["account_name"]
        account_number = transaction["account_number"]
        amount = transaction["amount"]
        miscellaneous = transaction["miscellaneous"]

        if transaction_code == TransactionCode.WITHDRAWAL.value:
            handle_withdrawal(accounts, account_number, amount)
        elif transaction_code == TransactionCode.TRANSFER.value:
            handle_transfer(accounts, account_number, miscellaneous, amount)
        elif transaction_code == TransactionCode.PAYBILL.value:
            handle_paybill(accounts, account_number, amount)
        elif transaction_code == TransactionCode.DEPOSIT.value:
            handle_deposit(accounts, account_number, amount)
        elif transaction_code == TransactionCode.CREATE.value:
            handle_create(accounts, account_number, account_name, amount)
        elif transaction_code == TransactionCode.DELETE.value:
            handle_delete(accounts, account_number)
        elif transaction_code == TransactionCode.DISABLE.value:
            handle_disable(accounts, account_number)
        elif transaction_code == TransactionCode.CHANGEPLAN.value:
            handle_changeplan(accounts, account_number)
        else:
            # This should never happen due to prior validation, but we can log an error if it does
            log_constraint_error(
                f"Invalid transaction code '{transaction_code}' in apply_transactions",
                "apply_transactions",
                fatal=False,
            )


def handle_withdrawal(accounts, account_number, amount):
    """Handles withdrawal transactions and updates the account balance accordingly."""
    account = get_account(accounts, account_number)
    if account is None:
        log_constraint_error(
            f"Account number '{account_number}' not found for withdrawal transaction",
            TransactionCode.WITHDRAWAL.name,
            fatal=False,
        )
        return

    account["balance"] -= amount
    increment_transaction_count(account)


def handle_transfer(accounts, from_account_number, to_account_number, amount):
    """Handles transfer transactions and updates account balances accordingly."""
    from_account = get_account(accounts, from_account_number)
    to_account = get_account(accounts, to_account_number)

    if from_account is None:
        log_constraint_error(
            f"From account number '{from_account_number}' not found for transfer transaction",
            TransactionCode.TRANSFER.name,
            fatal=False,
        )
        return
    if to_account is None:
        log_constraint_error(
            f"To account number '{to_account_number}' not found for transfer transaction",
            TransactionCode.TRANSFER.name,
            fatal=False,
        )
        return

    from_account["balance"] -= amount
    to_account["balance"] += amount
    increment_transaction_count(from_account)
    increment_transaction_count(to_account)


def handle_paybill(accounts, account_number, amount):
    """Handles paybill transactions and updates the account balance accordingly."""
    account = get_account(accounts, account_number)
    if account is None:
        log_constraint_error(
            f"Account number '{account_number}' not found for paybill transaction",
            TransactionCode.PAYBILL.name,
            fatal=False,
        )
        return

    account["balance"] -= amount
    increment_transaction_count(account)


def handle_deposit(accounts, account_number, amount):
    """Handles deposit transactions and updates the account balance accordingly."""
    account = get_account(accounts, account_number)
    if account is None:
        log_constraint_error(
            f"Account number '{account_number}' not found for deposit transaction",
            TransactionCode.DEPOSIT.name,
            fatal=False,
        )
        return

    account["balance"] += amount
    increment_transaction_count(account)


def handle_create(accounts, account_number, account_name, amount):
    """Handles create transactions and adds a new account to the accounts list."""
    account = {
        "account_number": account_number,
        "name": account_name,
        "status": "A",
        "balance": amount,
        "total_transactions": 0,
        "plan": "SP",
    }
    accounts.append(account)


def handle_changeplan(accounts, account_number):
    """Handles change plan transactions and updates the account plan type."""
    account = get_account(accounts, account_number)
    if account is None:
        log_constraint_error(
            f"Account number '{account_number}' not found for change plan transaction",
            TransactionCode.CHANGEPLAN.name,
            fatal=False,
        )
        return

    account["plan"] = "SP" if account["plan"] == "NP" else "NP"
    increment_transaction_count(account)


def handle_delete(accounts, account_number):
    """Handles delete transactions and removes an account from the accounts list."""
    account = get_account(accounts, account_number)
    if account is None:
        log_constraint_error(
            f"Account number '{account_number}' not found for delete transaction",
            TransactionCode.DELETE.name,
            fatal=False,
        )
        return

    accounts.remove(account)


def handle_disable(accounts, account_number):
    """Handles disable transactions and updates the account status to 'D'."""
    account = get_account(accounts, account_number)
    if account is None:
        log_constraint_error(
            f"Account number '{account_number}' not found for disable transaction",
            TransactionCode.DISABLE.name,
            fatal=False,
        )
        return

    account["status"] = "D"
    increment_transaction_count(account)


def get_account(accounts, account_number) -> dict | None:
    """Helper function to retrieve an account by account number."""
    for account in accounts:
        if account["account_number"] == account_number:
            return account
    return None


def increment_transaction_count(account):
    """Increments the total transaction count for an account."""
    account["total_transactions"] += 1
