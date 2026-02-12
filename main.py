from session import Session
from transaction import TransactionHandler


def main():

    session = None

    print("Banking System")
    while True:
        command = input("> ").strip()

        # No transaction other than login should be accepted if there is no active session
        if session is None and command != "login":
            print("Please log in to perform transactions.")
            continue

        # No subsequent login should be accepted if there is already an active session
        if session is not None and command == "login":
            print("You are already logged in. Please log out before logging in again.")
            continue

        transaction_handler = TransactionHandler(session)
        
        if command == "login":
            session = handle_login()
        elif command == "logout":
            session = handle_logout(session)
        elif command == "withdrawal":
            handle_withdrawal(session, transaction_handler)


def handle_login():
    # Get the session kind from the user
    while True:
        kind = input("Enter session kind (admin/standard): ").strip().lower()
        if kind not in ["admin", "standard"]:
            print("Invalid session kind. Please enter 'admin' or 'standard'.")
            continue
        else:
            break

    # Get the account holder name if the session kind is standard
    account_holder_name = None
    if kind == "standard":
        while True:
            account_holder_name = input("Enter account holder name: ").strip()
            if not account_holder_name:
                print("Account holder name cannot be empty. Please enter a valid name.")
                continue
            else:
                break

    # Create a new session
    session = Session(kind, account_holder_name)

    return session


def handle_logout(session: Session):
    # Write the current session's transactions to the file
    session.write_transactions()
    return None


def handle_withdrawal(session: Session, transaction_handler: TransactionHandler):
    """Withdraw money from an account."""

    # Ask for the account holder's name, account number, and amount to withdraw
    if session.kind == "admin":
        account_holder_name = input("Enter account holder name: ").strip()
    else:
        account_holder_name = session.account_holder_name

    account_number = input("Enter account number: ").strip()
    if not account_number.isdigit():
        print("Invalid account number. Please enter a valid account number.")
        return
    account_number = int(account_number)

    amount = input("Enter amount to withdraw: ").strip()
    if not amount.isdigit():
        print("Invalid amount. Please enter a valid amount.")
        return
    amount = int(amount)

    transaction_handler.handle_withdrawal(account_holder_name, account_number, amount)


if __name__ == "__main__":
    main()
