"""
bank_audit.py

A tiny banking module where every deposit, withdrawal, and failed
operation is written to a log file (bank_app.log), including the account
id, the amount involved, and the resulting balance.
"""

import logging

logging.basicConfig(
    filename="bank_app.log",
    filemode="a",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

log = logging.getLogger("bank_audit")


class InsufficientFundsError(Exception):
    pass


class Account:
    def __init__(self, account_id: str, balance: float = 0.0):
        self.account_id = account_id
        self.balance = balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            log.warning(
                "FAILED deposit: account=%s amount=%s balance=%s reason=non-positive-amount",
                self.account_id, amount, self.balance,
            )
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        log.info(
            "SUCCESS deposit: account=%s amount=%s balance=%s",
            self.account_id, amount, self.balance,
        )

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            log.warning(
                "FAILED withdrawal: account=%s amount=%s balance=%s reason=non-positive-amount",
                self.account_id, amount, self.balance,
            )
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            log.warning(
                "FAILED withdrawal: account=%s amount=%s balance=%s reason=insufficient-funds",
                self.account_id, amount, self.balance,
            )
            raise InsufficientFundsError("Insufficient funds.")
        self.balance -= amount
        log.info(
            "SUCCESS withdrawal: account=%s amount=%s balance=%s",
            self.account_id, amount, self.balance,
        )


def demo():
    accounts = {
        "A100": Account("A100", balance=100),
        "A200": Account("A200", balance=50),
    }

    ops = [
        ("A100", "deposit", 50),
        ("A100", "withdraw", 30),
        ("A200", "withdraw", 1000),   # fails: insufficient funds
        ("A200", "withdraw", 1000),   # fails again
        ("A100", "deposit", -5),      # fails: non-positive
        ("A200", "deposit", 20),
        ("A100", "withdraw", 1000),   # fails: insufficient funds
        ("A200", "withdraw", 10),
    ]

    for account_id, action, amount in ops:
        account = accounts[account_id]
        try:
            if action == "deposit":
                account.deposit(amount)
            else:
                account.withdraw(amount)
        except (ValueError, InsufficientFundsError) as exc:
            print(f"{account_id}: {action}({amount}) failed -> {exc}")
        else:
            print(f"{account_id}: {action}({amount}) ok -> balance={account.balance}")


if __name__ == "__main__":
    demo()
