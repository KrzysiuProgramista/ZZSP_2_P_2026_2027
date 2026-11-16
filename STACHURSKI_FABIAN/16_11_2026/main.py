import unittest
class BankAccount:
    """A basic bank account with a name and a balance."""

    def __init__(self, owner: str, balance: float = 0):
        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("Owner name cannot be empty.")

        if not isinstance(balance, (int, float)) or isinstance(balance, bool):
            raise TypeError("Balance must be a number.")

        if balance < 0:
            raise ValueError("Starting balance cannot be negative.")

        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float) -> None:
        """Add money to the account."""
        self._validate_amount(amount)
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        """Withdraw money if the account has sufficient funds."""
        self._validate_amount(amount)
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount

    @staticmethod
    def _validate_amount(amount: float) -> None:
        """Validate a deposit or withdrawal amount."""
        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            raise TypeError("Amount must be a number.")
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")


#task 1
class TestBankAccount(unittest.TestCase):

    def setUp(self):
        self.account = BankAccount("Alice", 100)

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 100)

    def test_deposit(self):
        self.account.deposit(50)
        self.assertEqual(self.account.balance, 150)

    def test_withdraw(self):
        self.account.withdraw(40)
        self.assertEqual(self.account.balance, 60)

    def test_withdraw_too_much(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(200)

    def test_negative_deposit(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-10)


if __name__ == "__main__":
    unittest.main()