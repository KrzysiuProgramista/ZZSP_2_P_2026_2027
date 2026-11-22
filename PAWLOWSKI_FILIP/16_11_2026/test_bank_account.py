import unittest

from bank_account import BankAccount


class TestBankAccount(unittest.TestCase):

    def setUp(self):
        self.account = BankAccount("Marta", 800)

    
    def test_starting_balance(self):
        self.assertEqual(self.account.balance, 800)

    def test_owner_is_stored(self):
        self.assertEqual(self.account.owner, "Marta")

    def test_deposit(self):
        self.account.deposit(250)
        self.assertEqual(self.account.balance, 1050)

    def test_withdraw(self):
        self.account.withdraw(300)
        self.assertEqual(self.account.balance, 500)

    def test_withdraw_whole_balance(self):
        self.account.withdraw(800)
        self.assertEqual(self.account.balance, 0)

    def test_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(801)

        self.assertEqual(self.account.balance, 800)

    def test_negative_deposit_is_rejected(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-50)

    def test_deposit_of_text_is_rejected(self):
        with self.assertRaises(TypeError):
            self.account.deposit("100")

    def test_empty_owner_is_rejected(self):
        with self.assertRaises(ValueError):
            BankAccount("   ", 100)

    
    def test_deposit_1000_into_account(self):
        self.account.deposit(1000)
        self.assertEqual(self.account.balance, 1800)

    def test_starting_value_is_unchanged(self):
        self.assertEqual(self.account.balance, 800)


if __name__ == "__main__":
    unittest.main()
