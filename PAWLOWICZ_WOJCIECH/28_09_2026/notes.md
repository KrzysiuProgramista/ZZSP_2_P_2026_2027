# Debugging exercises — notes (28.09.2026)

## Exercise 1: Traceback reading

| # | Snippet | Predicted exception | Actual exception | Why |
|---|---------|---------------------|-------------------|-----|
| a | `numbers[3]` on a 3-item list | `IndexError` | `IndexError: list index out of range` | Valid indices are 0-2; 3 is out of range. |
| b | `data["b"]` on `{"a": 1}` | `KeyError` | `KeyError: 'b'` | Key `"b"` is not in the dict. |
| c | `f("5")` where `f(x): return x + 1` | `TypeError` | `TypeError: can only concatenate str (not "int") to str` | Can't add an `int` to a `str` with `+`. |
| d | `g([{"value": 1}, {"val": 2}])` | `KeyError` | `KeyError: 'value'` | The second dict has key `"val"`, not `"value"`. |
| e | `int("12a")` | `ValueError` | `ValueError: invalid literal for int() with base 10: '12a'` | `"12a"` is not a valid base-10 integer literal. |
| f | `open("does_not_exist.txt")` | `FileNotFoundError` | `FileNotFoundError: [Errno 2] No such file or directory: 'does_not_exist.txt'` | The file doesn't exist in the current directory. |

Takeaway: the exception *type* usually tells you the category of mistake
(index math, missing key, wrong type, bad format, missing resource), while
the message gives the exact offending value.

## Exercise 2: The call chain

See `exercises.py`, `exercise2_demo()`. In the printed traceback:

- The line that **raised**: `return 1 / 0` inside `c()`.
- The line that **called it**: `return c()` inside `b()`.
- The line that **started the whole thing**: `a()` inside `exercise2_demo()`.

A traceback is read top-to-bottom as "how we got here", and the actual
error is always on the last frame.

## Exercise 5: The off-by-one hunt

a) `return items[len(items) - 4:]`
   Wrong: a slice of the *last three* items should start at `len - 3`, not
   `len - 4` (which gives the last **four**). Fix: `items[len(items) - 3:]`.

b) `for i in range(1, n): print(i)` for "count up to n"
   Wrong: `range(1, n)` stops at `n - 1`, so `n` itself is never printed.
   Fix: `range(1, n + 1)`.

c) `return items[len(items) // 2 + 1]`
   Wrong: the extra `+ 1` skips the true middle element. For a list of
   length 5, the middle index is `5 // 2 == 2`, not `2 + 1 == 3`.
   Fix: `items[len(items) // 2]`.

## Exercise 6: The mutation bug

`remove_evens` iterates over `numbers` with a `for` loop while calling
`numbers.remove(n)` inside the loop. A `for` loop over a list tracks a
position index internally; removing an item shifts every later item one
slot to the left, but the loop's index still advances by one, so the
element that slid into the freed slot is skipped.

Example: `[1, 2, 4, 6, 7]`
- index 0 -> `1` (odd, kept)
- index 1 -> `2` (even, removed) -> list becomes `[1, 4, 6, 7]`
- index 2 -> now points at `6` (because `4` slid left into index 1) -> `4`
  is never checked and stays in the output, which is still wrong but for
  the opposite reason students usually expect (it isn't removed when it
  should be, not an IndexError).

Fix: never mutate a list while iterating over it. Build a new list instead
(see `remove_evens_fixed` in `exercises.py`), or iterate over a copy
(`for n in numbers[:]`).

## Exercise 7: The default argument trap

```python
def add_item(item, basket=[]):
    basket.append(item)
    return basket
```

Predicted/actual output:

```
['a']
['a', 'b']
['a', 'b', 'c']
```

Not three independent one-item lists. In Python, a default argument value
is evaluated **once**, when the function is defined, and the same object
is reused on every call that doesn't supply its own value for that
argument. Since lists are mutable, every call that relies on the default
is appending to the *same* list.

Fix: use an immutable sentinel (`None`) as the default and create a fresh
list inside the function body when needed:

```python
def add_item(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket
```
