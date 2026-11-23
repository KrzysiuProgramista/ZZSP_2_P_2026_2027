import unittest
from bank_account import BankAccount


class TestBankAccount(unittest.TestCase):
    '''
    @classmethod
    def setUpClass(cls):
        cls.account = BankAccount("Alice", 100)
    '''
    def setUp(self) -> None:
        self.account = BankAccount("Alice", 100.0)

    def test_initial_state(self) -> None:
        self.assertEqual(self.account.owner, "Alice")
        self.assertEqual(self.account.balance, 100.0)

    def test_deposit_increases_balance(self) -> None:
        self.account.deposit(50.0)
        self.assertEqual(self.account.balance, 150.0)

    def test_deposit_invalid_amount_raises(self) -> None:
        with self.assertRaises(ValueError):
            self.account.deposit(-10)
        with self.assertRaises(TypeError):
            self.account.deposit("50")  # type: ignore[arg-type]

    def test_withdraw_decreases_balance(self) -> None:
        self.account.withdraw(40.0)
        self.assertEqual(self.account.balance, 60.0)

    def test_withdraw_insufficient_funds_raises(self) -> None:
        with self.assertRaises(ValueError):
            self.account.withdraw(200.0)

    def test_invalid_constructor_arguments_raise(self) -> None:
        with self.assertRaises(ValueError):
            BankAccount("   ", 50)
        with self.assertRaises(ValueError):
            BankAccount("Bob", -1)
        with self.assertRaises(TypeError):
            BankAccount("Bob", True)

    def test_01_deposit_1000(self):
            self.account.deposit(1000)
            self.assertEqual(self.account.balance, 1100)

    def test_02_balance_is_still_starting_value(self):
            self.assertEqual(self.account.balance, 100)

'''
    Ex2 note:
    Moving account creation to setUpClass caused test_02_balance_is_still_starting_value
    (and subsequent tests) to fail with 1100 != 100, because all tests shared one
    BankAccount instance and mutations from test_01 leaked into later tests.
'''

if __name__ == "__main__":
    unittest.main()