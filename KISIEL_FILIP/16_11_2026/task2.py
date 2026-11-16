#zad 2
import unittest


class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount


class TestIsolation(unittest.TestCase):
    def setUp(self):
        self.account = BankAccount("Anna", 100)

    def test_deposit_1000(self):
        self.account.deposit(1000)
        self.assertEqual(self.account.balance, 1100)

    def test_starts_at_100(self):
        self.assertEqual(self.account.balance, 100)
        # setUp creates a new account for every test.


class TestSetUpClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.account = BankAccount("Anna", 100)

    def test_1_deposit_1000(self):
        self.account.deposit(1000)
        self.assertEqual(self.account.balance, 1100)

    @unittest.expectedFailure
    def test_2_starts_at_100(self):
        self.assertEqual(self.account.balance, 100)


if __name__ == "__main__":
    unittest.main(verbosity=2)
