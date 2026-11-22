# Log analysis — `equipment_checkout.py` / `app.log`

`app.log` was produced by running `equipment_checkout.py`'s built-in
`automated_demo()`, which performs 10 scripted menu interactions plus one
deliberately forced unexpected error — 7 successful operations, 4 invalid
operations, and 1 exception logged with a traceback.

## 1. Which operations were recorded as successful?

All `INFO`-level lines mark a successful operation:

- Registering 4 seed items (L1, L2, P1, C1) and later a 5th (C2) — 5
  successful "add" operations.
- Borrowing L1.
- Returning L1.
- Plus the two lifecycle events "Application starting up." and
  "Application shutting down." (not equipment operations, but also INFO).

That's 7 successful equipment operations in total.

## 2. Which invalid operations generated warnings?

All `WARNING`-level lines:

- Borrowing L1 a second time while it was still checked out (`already
  borrowed`).
- Returning P1, which had never been borrowed (`not borrowed`).
- Borrowing the unknown id `ZZZ` (`invalid/unknown equipment id`).
- Entering `9` at the main menu, which isn't one of options 1-6
  (`invalid menu option`).

That's 4 invalid operations.

## 3. What information does the traceback provide?

The one `ERROR` entry (from `_force_unexpected_error`) includes a full
Python traceback:

```
Traceback (most recent call last):
  File ".../equipment_checkout.py", line 202, in _force_unexpected_error
    _ = broken_item["available"]
TypeError: 'NoneType' object is not subscriptable
```

It tells us: the exact exception type (`TypeError`), the human-readable
reason (`'NoneType' object is not subscriptable`), the file and line
number where the failing statement lives, the name of the function it
happened in (`_force_unexpected_error`), and the literal line of source
code that raised it. Combined, that's normally enough to go straight to
the bug without having to reproduce it interactively.

## 4. How can the log file help a developer reconstruct the sequence of events?

Because every entry is timestamped and ordered chronologically, and
because the `DEBUG` lines record the *entire* equipment state after every
successful change, a developer can replay the whole session from the log
alone: which items existed at each point, which ones were available or
borrowed, and exactly which user action (INFO/WARNING line immediately
above each DEBUG snapshot) caused each state transition. If something
looks wrong at a given moment, the developer can scan backwards through
the DEBUG snapshots to find the exact operation that introduced the bad
state, without needing to re-run the program with a debugger attached.

## 5. What is the difference between `log.error()` and `log.exception()`?

`log.error()` records a message at ERROR level — useful when you know
something went wrong and want to say so, but you are not necessarily
inside an `except` block (or don't need the traceback).

`log.exception()` is equivalent to calling `log.error()` but additionally
and automatically attaches the current exception's traceback to the log
record. It should only be called from inside an `except` block, where an
active exception exists to capture. Using `log.exception()` instead of
`log.error()` when handling an unexpected failure gives you the file,
line number, and call stack for free, which is exactly what made question
3's investigation possible.
