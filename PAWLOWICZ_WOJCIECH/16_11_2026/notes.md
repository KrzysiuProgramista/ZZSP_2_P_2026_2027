# Session notes — 16.11.2026

## Exercise 1-2: setUp / isolation
See `test_bank_account.py`. `TestBankAccount` refactors the earlier
duplicated "create an account" code into `setUp()`. `TestIsolationSetUp`
and `TestIsolationSetUpClass` are the isolation experiment: with
`setUp()`, each test method gets its own fresh `BankAccount`, so
depositing in one test never leaks into another (both tests pass
regardless of order). Switching the same account creation to
`setUpClass()` breaks that: the account becomes a single object shared by
the whole class, so a deposit made by one test method is still there
when a later test method inspects the balance.

## Exercise 3: FileStore + tearDown
See `file_store.py` / `test_file_store.py`. `setUp()` creates a unique
temporary filename (without creating the file); `tearDown()` deletes it
if it exists, regardless of whether the test passed, failed, or raised.
Running the suite repeatedly leaves no stray `*.json` files behind.

## Exercises 4-7: LibraryCatalog
See `library_catalog.py` / `test_library_catalog.py`.

- Exercise 4: full implementation + a test suite with >=2 tests per
  method (success and failure), a borrow-then-return round trip, and
  tests proving failed operations don't change the catalogue.
- Exercise 5: the tests are already organised as
  `TestAddingBooks`, `TestRemovingBooks`, `TestSearching`,
  `TestBorrowing`, each with its own `setUp`. Running with `-v` groups
  the output by class and makes it immediately clear which *kind* of
  operation a failure would belong to.
- Exercise 6: `TestIsEven.test_is_even_over_many_inputs` uses `subTest`
  over 10 inputs (negative, positive, and zero). Breaking one entry on
  purpose (example: changing the expected value for `n=2` to `False`)
  makes `unittest -v` report precisely `AssertionError` for the
  `(n=2)` sub-test while every other sub-test in the same test method
  still runs and still passes -- the summary line shows exactly which
  input failed instead of aborting the whole test on the first mismatch.
- Exercise 7: `TestNotYetImplemented` shows `@unittest.skip(...)`,
  `@unittest.skipIf(...)`, and `@unittest.expectedFailure`. The final run
  summary reports them distinctly: `OK (skipped=1, expected failures=1)`
  instead of simply `OK` or `FAILED`.
