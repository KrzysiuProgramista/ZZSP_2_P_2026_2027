## Exercise 2: Isolation (`setUp` vs `setUpClass`)
- With `setUp`, each test gets a fresh `BankAccount`, so depositing 1000 in one test does not affect the next.
- Moving account creation to `setUpClass` makes all tests share one instance, so `test_02_balance_is_still_starting_value` fails (`1100 != 100`).

## Exercise 5: Organising with `-v`
- Splitting into `TestAddingBooks`, `TestRemovingBooks`, `TestSearching`, and `TestBorrowing` displays the class name beside each test in `-v` output, making failures easy to locate by feature.

## Exercise 6: `subTest`
- Breaking one case (e.g. `(1, True)`) reports the exact failing subtest parameters `(number=1, expected=True)` while still running all remaining inputs.

## Exercise 7: `skip` and `expectedFailure`
- Skipped tests appear as `skipped '...'` in `-v` output (or `s` without `-v`), and the final summary reports `OK (skipped=1)` (or `skipped=2` on Windows).
- `@unittest.expectedFailure` reports `expected failure` (`x`) without failing the suite.