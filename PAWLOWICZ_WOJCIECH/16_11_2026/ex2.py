import unittest
from ex1 import BankAccount

class TestBankAccountIsolation(unittest.TestCase):
    def setUp(self):
        self.account = BankAccount("Anna", 100)

    def test_1_deposit_big_amount(self):
        self.account.deposit(1000)
        self.assertEqual(self.account.balance, 1100)

    def test_2_balance_still_starting_value(self):
        self.assertEqual(self.account.balance, 100)

    # Both tests pass regardless of order: setUp() runs again before each
    # test method, so test_1 and test_2 each get their OWN BankAccount
    # object. Depositing in test_1 can't affect test_2's object.


# setUpClass() runs ONCE for the whole class, so every test shares the
# same cls.account instead of getting a fresh one -> test_2 now sees
# test_1's deposit and fails.
class TestBankAccountIsolationBroken(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.account = BankAccount("Anna", 100)

    def test_1_deposit_big_amount(self):
        self.account.deposit(1000)
        self.assertEqual(self.account.balance, 1100)

    def test_2_balance_still_starting_value(self):
        # fails: balance is 1100 here, not 100, because this is the same
        # account object test_1 already deposited into
        self.assertEqual(self.account.balance, 100)


if __name__ == "__main__":
    unittest.main()