import unittest

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("deposit amount must be positive")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("withdraw amount must be positive")
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount

class TestBankAccount(unittest.TestCase):
    def setUp(self):
        # runs before every test -> each test gets its own fresh account
        self.account = BankAccount("Anna", 100)

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 100)

    def test_deposit_increases_balance(self):
        self.account.deposit(50)
        self.assertEqual(self.account.balance, 150)

    def test_withdraw_decreases_balance(self):
        self.account.withdraw(20)
        self.assertEqual(self.account.balance, 80)

    def test_withdraw_too_much_raises(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(1000)

    def test_deposit_rejects_non_positive_amount(self):
        with self.assertRaises(ValueError):
            self.account.deposit(0)


if __name__ == "__main__":
    unittest.main()