import unittest

from bank_account import BankAccount


class TestBankAccount(unittest.TestCase):
    """Exercise 1: refactored with setUp -- every test used to start by
    creating `self.account = BankAccount(...)`; that's now done once here
    instead of being duplicated in every test method."""

    def setUp(self):
        self.account = BankAccount("Alice", balance=100)

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 100)

    def test_deposit_increases_balance(self):
        self.account.deposit(50)
        self.assertEqual(self.account.balance, 150)

    def test_withdraw_decreases_balance(self):
        self.account.withdraw(30)
        self.assertEqual(self.account.balance, 70)

    def test_withdraw_more_than_balance_raises(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(1000)

    def test_deposit_non_positive_raises(self):
        with self.assertRaises(ValueError):
            self.account.deposit(0)

    def test_deposit_non_numeric_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.account.deposit("ten")

    def test_empty_owner_name_rejected(self):
        with self.assertRaises(ValueError):
            BankAccount("   ", balance=10)

    def test_negative_starting_balance_rejected(self):
        with self.assertRaises(ValueError):
            BankAccount("Bob", balance=-5)


class TestIsolationSetUp(unittest.TestCase):
    """Exercise 2: proving test isolation with setUp."""

    def setUp(self):
        self.account = BankAccount("Carol", balance=100)

    def test_a_deposit_1000(self):
        self.account.deposit(1000)
        self.assertEqual(self.account.balance, 1100)

    def test_b_balance_is_still_starting_value(self):
        # If this still reads 100, setUp() built a brand-new BankAccount
        # for *this* test method, completely independent of whatever
        # test_a_deposit_1000 did to its own account. unittest calls
        # setUp() again before every single test method, so each test
        # gets a fresh, isolated instance -- that's why both tests pass
        # regardless of execution order.
        self.assertEqual(self.account.balance, 100)


class TestIsolationSetUpClass(unittest.TestCase):
    """Same experiment, but creating the account once in setUpClass
    instead of setUp.

    What breaks: setUpClass runs exactly ONCE for the whole class (before
    any test in it), and the created object is shared via a class
    attribute across every test method. Since BankAccount instances are
    mutable, test_a_deposit_1000 (whichever test method runs first,
    alphabetically "test_a_..." in this suite) mutates the SAME shared
    account that test_b_balance_is_still_starting_value later inspects --
    so the "still the starting balance" assertion now fails, because the
    deposit from the other test leaked into it. This is exactly the kind
    of order-dependent, non-isolated test setUp() is meant to prevent.
    """

    @classmethod
    def setUpClass(cls):
        cls.account = BankAccount("Carol", balance=100)

    def test_a_deposit_1000(self):
        type(self).account.deposit(1000)
        self.assertEqual(type(self).account.balance, 1100)

    def test_b_balance_is_no_longer_the_starting_value(self):
        # Documenting the breakage rather than hiding it: with
        # setUpClass, the deposit from test_a leaks into this test.
        self.assertEqual(type(self).account.balance, 1100)


if __name__ == "__main__":
    unittest.main()
