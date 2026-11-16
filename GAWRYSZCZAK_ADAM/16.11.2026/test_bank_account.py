import unittest
from bank_account import BankAccount


class TestBankAccount(unittest.TestCase):

    def setUp(self):
        self.account = BankAccount("Jan Kowalski", 500)

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 500)

    def test_withdraw(self):
        self.account.withdraw(200)
        self.assertEqual(self.account.balance, 300)

    def test_withdraw_too_much(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(1000)

    def test_deposit_1000(self):
        self.account.deposit(1000)
        self.assertEqual(self.account.balance, 1500)

    def test_balance_is_still_starting_value(self):
        self.assertEqual(self.account.balance, 500)


if __name__ == "__main__":
    unittest.main()