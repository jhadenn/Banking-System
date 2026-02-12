from enum import Enum
from typing import TYPE_CHECKING

# Only import the Session class for type checking, not at runtime
if TYPE_CHECKING:
    from session import Session


class TransactionCode(Enum):
    END = 0
    WITHDRAWAL = 1
    TRANSFER = 2
    PAYBILL = 3
    DEPOSIT = 4
    CREATE = 5
    DELETE = 6
    DISABLE = 7
    CHANGEPLAN = 8


class Transaction:
    def __init__(
        self,
        code: TransactionCode,
        account_holder_name: str,
        account_number: int,
        amount: float,
    ):
        self.code = code
        self.account_holder_name = account_holder_name
        self.account_number = account_number
        self.amount = amount


class TransactionHandler:
    def __init__(self, session: Session):
        self.session = session

    def handle_withdrawal(
        self, account_holder_name: str, account_number: int, amount: int
    ) -> Transaction:

        if self.session.kind == "standard":
            if account_holder_name != self.session.account_holder_name:
                print(
                    "Bank account must be a valid account for the account holder currently logged in."
                )
                return
            if amount > 500:
                print(
                    "Maximum amount that can be withdrawn in current session is $500.00 in standard mode."
                )
                return

        account = self.session.accounts.get(account_number)
        if account is None:
            print(
                "Bank account must be a valid account for the account holder currently logged in."
            )
            return

        new_balance = account.balance - amount
        if new_balance < 0:
            print("Account balance must be at least $0.00 after withdrawal.")
            return

        account.balance = new_balance
        transaction = Transaction(
            TransactionCode.WITHDRAWAL, account_holder_name, account_number, amount
        )

        print(f"Withdrawal successful. New balance: ${account.balance:.2f}")
        return transaction

    def check_for_admin_privileges(self) -> bool:
        if self.session.kind != "admin":
            print("You must log in as an admin to perform this transaction.")
            return False
        return True
