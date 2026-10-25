# Log Analysis – Equipment Checkout (`app.log`)

The test session performed 13 menu operations (6 successful, 4 invalid, 1 forced exception, plus startup/exit). Startup also registered 3 sample items.

## 1. Which operations were recorded as successful?

Successful operations appear as `INFO` entries, each followed by a `DEBUG` state snapshot:

- Application start and shutdown.
- Registration of Laptop `L-001`, Projector `P-001`, Camera `C-001` at startup, and later Tripod `T-001`.
- `L-001` borrowed by Alice, then returned by Alice.
- `C-001` borrowed by Bob.

Display operations (options 1 and 5) are read-only, so they produce only a `DEBUG` line.

## 2. Which invalid operations generated warnings?

| Action | WARNING message |
|---|---|
| Borrowing `L-001` while Alice had it | `Borrow attempted for unavailable item L-001 (held by Alice)` |
| Returning `P-001`, which was never borrowed | `Return attempted for item P-001 which is not borrowed` |
| Adding a second item with ID `L-001` | `Attempt to add duplicate equipment ID L-001` |
| Borrowing non-existent ID `ZZZ` | `Borrow attempted with unknown ID ZZZ` |
| Entering menu option `9` | `Invalid menu option: '9'` |

## 3. What information does the traceback provide?

```
ERROR - Unexpected failure while running menu option 5
Traceback (most recent call last):
  File "equipment_checkout.py", line 171, in main
    display_status()
  File "equipment_checkout.py", line 104, in display_status
    if item["available"]:
KeyError: 'available'
```

It gives:
- **The exception type and value:** `KeyError: 'available'` – a dictionary key was missing.
- **The call chain:** `main()` called `display_status()`, and the failure happened inside it.
- **The exact file, line number and source line** where the error occurred.
- **Context from the log message:** it happened while running menu option 5.

Together these point straight to the cause: one equipment record had lost its `available` field (the test deliberately corrupted the `T-001` record). The application did not crash; it reported the problem to the user and continued to a clean shutdown.

## 4. How can the log file help a developer reconstruct the sequence of events?

- Every line has a **timestamp**, so events can be put in exact order and timed.
- `INFO` lines show *what happened* (who borrowed/returned what), `WARNING` lines show *what was refused and why*, and `DEBUG` lines show the *full inventory state* after each change.
- Comparing consecutive `DEBUG` snapshots shows how the state evolved. For example, `L-001` goes `available → borrowed → available`, and `C-001` becomes `borrowed` for the rest of the session.
- The last `DEBUG` snapshot before the `ERROR` shows the state just before the failure, and the traceback shows where it failed. A developer can replay the session without the original user.

## 5. What is the difference between `log.error()` and `log.exception()`?

- `log.error(msg)` writes the message at `ERROR` level only. It can be used anywhere, and no traceback is included unless you pass `exc_info=True`.
- `log.exception(msg)` is equivalent to `log.error(msg, exc_info=True)`. It also writes the **full traceback** of the exception currently being handled, so it should be called only inside an `except` block.

In this application `log.exception()` is used in the `except Exception` handler in `main()`, which is why the log contains the full `KeyError` traceback and not just a message saying something failed.