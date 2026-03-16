import sys

from read import read_old_bank_accounts, read_transactions
from transactions import apply_transactions


def main():

    # Parse command line arguments
    master_bank_accounts_path = sys.argv[1]
    merged_transactions_path = sys.argv[2]

    # Read accounts and transactions, then apply transactions to accounts
    accounts = read_old_bank_accounts(master_bank_accounts_path)
    transactions = read_transactions(merged_transactions_path)
    apply_transactions(accounts, transactions)


if __name__ == "__main__":
    main()
