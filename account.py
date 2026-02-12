class Account:
    def __init__(self, account_holder_name: str, account_number: int, balance: float):
        self.account_holder_name = account_holder_name
        self.account_number = account_number
        self.balance = balance


def read_accounts() -> dict[int, Account]:
    print(NotImplemented)
