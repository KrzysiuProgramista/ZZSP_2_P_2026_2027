# Exercise 1 – Refactor with setUp

### Before

Every test started by building its own account:

```python
def test_deposit(self):
    account = BankAccount("Marta", 800)
    account.deposit(250)
    self.assertEqual(account.balance, 1050)

def test_withdraw(self):
    account = BankAccount("Marta", 800)
    account.withdraw(300)
    self.assertEqual(account.balance, 500)
```

### After

The creation line was moved into `setUp()` and the duplication was deleted:

```python
def setUp(self):
    self.account = BankAccount("Marta", 800)

def test_deposit(self):
    self.account.deposit(250)
    self.assertEqual(self.account.balance, 1050)
```

Running the suite:

```text
Ran 11 tests in 0.001s

OK
```

**Observation:** The suite still passes. `setUp()` runs before every test method, so each test still receives a fresh account.

---

# Exercise 2 – Proving isolation

### Steps 1–3: two tests, one deposit

- `test_deposit_1000_into_account` deposits 1000, so the balance becomes 1800.
- `test_starting_value_is_unchanged` deposits nothing and still expects 800.

Both pass. The reason (also written as a comment in the test file):

`setUp()` builds a **new** `BankAccount` before every test. The 1000 was deposited into an object that is discarded after the first test, so the second test never sees it. The order of the tests does not matter.

### Step 4: account creation moved to `setUpClass()`

```python
@classmethod
def setUpClass(cls):
    cls.account = BankAccount("Marta", 800)
```

The `setUp()` method was removed. This version lives in `test_bank_account_setupclass.py`, so the main suite stays green.

Result:

```text
Ran 11 tests in 0.002s

FAILED (failures=6)
```

Some of the failure messages:

```text
AssertionError: 2050 != 1800     (test_deposit_1000_into_account)
AssertionError: 1249 != 800      (test_starting_balance)
AssertionError: 1249 != 800      (test_starting_value_is_unchanged)
AssertionError: 949 != 500       (test_withdraw)
AssertionError: 149 != 0         (test_withdraw_whole_balance)
AssertionError: ValueError not raised   (test_insufficient_funds)
```

**What breaks and why:**

All tests now share one account, and `unittest` runs the tests in alphabetical order. Each test changes the balance and the next test starts from that changed value. `test_deposit` runs first and leaves 1050, so `test_deposit_1000_into_account` sees 2050 instead of 1800. After that the balance keeps drifting (1249, 949, 149) and the remaining tests fail.

`test_insufficient_funds` fails differently: by the time it runs the balance is high enough, so withdrawing 801 does not raise an error any more.

The tests are no longer isolated, because the result of one test depends on which tests ran before it.

**Key lesson:** Use `setUp()` when every test needs its own independent object. Use `setUpClass()` only for expensive resources that are read-only or otherwise safe to share (for example a database connection or a large file that is never modified).
