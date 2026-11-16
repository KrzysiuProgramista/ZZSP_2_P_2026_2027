import unittest
from bank_account import BankAccount

#ex1
class TestBankAccount(unittest.TestCase):

    def setUp(self):
        self.account = BankAccount("Alice", 100)

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 100)

    def test_deposit(self):
        self.account.deposit(50)
        self.assertEqual(self.account.balance, 150)

    def test_withdraw(self):
        self.account.withdraw(30)
        self.assertEqual(self.account.balance, 70)

    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(200)

    def test_deposit_negative_amount(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-10)

    def test_withdraw_zero_amount(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(0)

if __name__ == "__main__":
    unittest.main()

#ex2
class TestBankAccount(unittest.TestCase):

    def setUp(self):
        self.account = BankAccount("Alice", 100)

    def test_deposit_1000(self):
        self.account.deposit(1000)
        self.assertEqual(self.account.balance, 1100)

    def test_balance_is_still_100(self):
        self.assertEqual(self.account.balance, 100)


if __name__ == "__main__":
    unittest.main()
# setUpClass() creates the account only once, so both tests use the same account.
# After depositing 1000, the balance changes and affects the next test.
# With setUp(), every test gets a fresh account.

