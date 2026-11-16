#zad 1
import unittest


class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount


class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.account = BankAccount("Anna", 100)

    def test_deposit(self):
        self.account.deposit(50)
        self.assertEqual(self.account.balance, 150)

    def test_withdraw(self):
        self.account.withdraw(20)
        self.assertEqual(self.account.balance, 80)

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 100)


if __name__ == "__main__":
    unittest.main(verbosity=2)
