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

    # No bank account should ever have a negative balance
    if account["balance"] < amount:
        log_constraint_error(
            f"Insufficient funds in account '{account_number}' for withdrawal transaction",
            TransactionCode.WITHDRAWAL.name,
            fatal=False,
        )
        return

    account["balance"] -= amount
    increment_transaction_count(account)
    apply_transaction_cost(account)


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

    # No bank account should ever have a negative balance
    if from_account["balance"] < amount:
        log_constraint_error(
            f"Insufficient funds in account '{from_account_number}' for transfer transaction",
            TransactionCode.TRANSFER.name,
            fatal=False,
        )
        return

    from_account["balance"] -= amount
    to_account["balance"] += amount
    increment_transaction_count(from_account)
    apply_transaction_cost(from_account)


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

    # No bank account should ever have a negative balance
    if account["balance"] < amount:
        log_constraint_error(
            f"Insufficient funds in account '{account_number}' for paybill transaction",
            TransactionCode.PAYBILL.name,
            fatal=False,
        )
        return

    account["balance"] -= amount
    increment_transaction_count(account)
    apply_transaction_cost(account)


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
    apply_transaction_cost(account)


def handle_create(accounts, account_number, account_name, amount):
    """Handles create transactions and adds a new account to the accounts list."""
    # A newly created account must have a unique account number
    if get_account(accounts, account_number) is not None:
        log_constraint_error(
            f"Account number '{account_number}' already exists for create transaction",
            TransactionCode.CREATE.name,
            fatal=False,
        )
        return

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
    apply_transaction_cost(account)


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
    apply_transaction_cost(account)


def get_account(accounts, account_number) -> dict | None:
    """Helper function to retrieve an account by account number."""
    for account in accounts:
        if account["account_number"] == account_number:
            return account
    return None


def increment_transaction_count(account):
    """Increments the total transaction count for an account."""
    account["total_transactions"] += 1


def apply_transaction_cost(account):
    """Deducts $0.05 for SP accounts and $0.10 for NP accounts from the account balance."""
    SP_COST = 0.05
    NP_COST = 0.10

    if account["plan"] == "SP":
        cost = SP_COST
    else:
        cost = NP_COST

    if account["balance"] < cost:
        log_constraint_error(
            f"Insufficient funds in account '{account['account_number']}' to apply transaction cost for SP plan",
            "apply_transaction_cost",
            fatal=False,
        )
        return
    account["balance"] -= cost
