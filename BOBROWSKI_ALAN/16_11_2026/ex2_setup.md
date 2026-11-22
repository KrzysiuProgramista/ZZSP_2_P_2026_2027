# Exercise 2: Proving isolation

## Replace `setUp()` with `setUpClass()`

Try this:

python

```python
@classmethod
def setUpClass(cls):
    cls.account = BankAccount("Alice", 1000)
```

Remove the original `setUp()`.

Now both tests share the same account.

What breaks?

The tests are no longer isolated.

If the deposit test runs first:

- Initial balance: 1000
- Deposit: 1000
- New balance: 2000
- The second test expects 1000 but receives 2000.
- The second test fails.

`setUpClass()` runs only once for the entire test class, whereas `setUp()` runs before every test.

Key lessonUse `setUp()` when each test needs its own independent objects. Use `setUpClass()` for expensive resources that can safely be shared between tests.