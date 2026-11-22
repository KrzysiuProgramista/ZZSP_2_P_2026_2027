# Exercise 2: Making a test fail on purpose

Steps performed:

1. Broke `subtract` deliberately, changing it to `return a + b` instead of
   `return a - b`.
2. Ran `python3 -m unittest -v` and read the failure:

   ```
   test_subtracting (test_calculator.TestCalculator.test_subtracting) ... FAIL

   ======================================================================
   FAIL: test_subtracting (test_calculator.TestCalculator.test_subtracting)
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File ".../test_calculator.py", line 19, in test_subtracting
       self.assertEqual(subtract(10, 4), 6)
   AssertionError: 14 != 6
   ```

3. Which test failed: `test_subtracting`.
   Expected: `6` (i.e. `10 - 4`).
   Received: `14` (i.e. `10 + 4`, because of the introduced bug).
4. Fixed `subtract` back to `return a - b`.
5. Re-ran the suite: all 10 tests passed (`OK`).

This confirms the test suite actually exercises the code: a single
one-character-equivalent mistake (`+` instead of `-`) was caught
immediately, with the assertion message pinpointing exactly which value
was wrong.
