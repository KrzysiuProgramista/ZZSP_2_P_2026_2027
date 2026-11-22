"""
Exercises 1-7: reasoning about bugs, tracebacks and debugging technique.

Run this file directly to see Exercise 2 (call chain), Exercise 3/4
(hypothesis-driven + print debugging), Exercise 6 (mutation bug) and
Exercise 7 (default-argument trap) in action. Exercises 1 and 5 are pure
reasoning and are answered in notes.md.
"""


# ---------------------------------------------------------------------------
# Exercise 2: The call chain
# ---------------------------------------------------------------------------
def a():
    return b()


def b():
    return c()


def c():
    return 1 / 0  # raises ZeroDivisionError


def exercise2_demo():
    print("Exercise 2: the call chain")
    try:
        a()
    except ZeroDivisionError:
        import traceback
        traceback.print_exc()
    # Traceback reading:
    #   - the line that RAISED: "return 1 / 0" inside c()
    #   - the line that CALLED it: "return c()" inside b()
    #   - the line that STARTED it all: "a()" inside exercise2_demo()
    print()


# ---------------------------------------------------------------------------
# Exercise 3 & 4: hypothesis-driven debugging + print debugging
# ---------------------------------------------------------------------------
def average_positive_buggy(numbers):
    total = 0
    count = 0
    for n in numbers:
        if n > 0:
            total += n
            count += 1
    return total / count
    # Hypothesis: if `numbers` contains no positive values, `count` stays 0
    # and the final division raises ZeroDivisionError. Proven below with a
    # single print, then fixed.


def average_positive_fixed(numbers):
    """Return the average of the positive numbers in `numbers`.

    Returns 0.0 if there are no positive numbers (documented choice).
    """
    total = 0
    count = 0
    for n in numbers:
        print(f"[average_positive_fixed] n={n} total={total} count={count}")
        if n > 0:
            total += n
            count += 1
    if count == 0:
        return 0.0
    return total / count


def exercise3_4_demo():
    print("Exercise 3: hypothesis-driven debugging")
    data = [-1, -2, -3]
    print(f"[hypothesis check] about to call average_positive_buggy({data})")
    try:
        average_positive_buggy(data)
    except ZeroDivisionError as exc:
        print(f"Confirmed hypothesis: {type(exc).__name__}: {exc}")

    print("\nExercise 4: print debugging done properly")
    result = average_positive_fixed(data)
    print(f"Result for {data}: {result}")

    result2 = average_positive_fixed([1, -2, 3, 4])
    print(f"Result for [1, -2, 3, 4]: {result2}")
    print()


# ---------------------------------------------------------------------------
# Exercise 6: the mutation bug
# ---------------------------------------------------------------------------
def remove_evens_buggy(numbers):
    """BUGGY: mutates the list while iterating over it.

    Removing an element shifts every later element one index to the left,
    but the for-loop's internal index keeps advancing, so it skips the
    element that slid into the spot just vacated. E.g. for [1, 2, 4, 6, 7]:
    index 1 is 2 (even, removed) -> list becomes [1, 4, 6, 7], index moves to
    2, which is now 6 (4 got skipped entirely).
    """
    for n in numbers:
        if n % 2 == 0:
            numbers.remove(n)
    return numbers


def remove_evens_fixed(numbers):
    """Build a new list instead of mutating the one being iterated."""
    return [n for n in numbers if n % 2 != 0]


def exercise6_demo():
    print("Exercise 6: the mutation bug")
    print("Buggy:", remove_evens_buggy([1, 2, 4, 6, 7]))  # misses 4
    print("Fixed:", remove_evens_fixed([1, 2, 4, 6, 7]))
    print()


# ---------------------------------------------------------------------------
# Exercise 7: the default argument trap
# ---------------------------------------------------------------------------
def add_item_buggy(item, basket=[]):
    """BUGGY: the default list is created ONCE, at function-definition
    time, and is reused (and mutated) on every call that doesn't pass its
    own basket. Prediction: ['a'], ['a', 'b'], ['a', 'b', 'c'] -- not three
    independent single-item lists.
    """
    basket.append(item)
    return basket


def add_item_fixed(item, basket=None):
    """FIXED: use None as the sentinel default and create a fresh list
    per call when the caller doesn't supply one."""
    if basket is None:
        basket = []
    basket.append(item)
    return basket


def exercise7_demo():
    print("Exercise 7: the default argument trap")
    print(add_item_buggy("a"))
    print(add_item_buggy("b"))
    print(add_item_buggy("c"))
    print("(all three calls above share the SAME hidden list)")

    print(add_item_fixed("a"))
    print(add_item_fixed("b"))
    print(add_item_fixed("c"))
    print("(each call above gets its own fresh list)")
    print()


if __name__ == "__main__":
    exercise2_demo()
    exercise3_4_demo()
    exercise6_demo()
    exercise7_demo()
