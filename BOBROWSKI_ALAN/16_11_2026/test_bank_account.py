import unittest
from bank_account import BankAccount


class TestBankAccount(unittest.TestCase):

    def setUp(self):
        # A new account is created before every test.
        self.account = BankAccount("Krzysztof", 500)

    def test_starting_balance(self):
        self.assertEqual(self.account.balance, 500)

    def test_deposit(self):
        self.account.deposit(1000)
        self.assertEqual(self.account.balance, 1500)

    def test_withdraw(self):
        self.account.withdraw(200)
        self.assertEqual(self.account.balance, 300)

    def test_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(1000)

    def test_invalid_deposit(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-100)

    def test_isolation_after_deposit(self):
        self.account.deposit(1000)
        self.assertEqual(self.account.balance, 1500)

    def test_isolation_starting_balance(self):
        # Every test gets a fresh account from setUp().
        # Deposits made in other tests cannot affect this account.
        self.assertEqual(self.account.balance, 500)


if __name__ == "__main__":
    unittest.main()
