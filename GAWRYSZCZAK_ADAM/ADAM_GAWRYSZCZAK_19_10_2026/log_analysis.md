# Log File Analysis (`app.log`)

### 1. Which operations were recorded as successful?
The following operations were recorded as successful at the `INFO` level (and followed by a `DEBUG` state log after each change):
- Application startup (`Application started`).
- Borrowing item ID `101` (`Laptop`).
- Borrowing item ID `102` (`Projector`).
- Registering new equipment with ID `104` (`Microphone`).
- Returning item ID `101` (`Laptop`).
- Borrowing item ID `104` (`Microphone`).
- Application shutdown (`Application shut down`).

### 2. Which invalid operations generated warnings?
Five invalid operations generated `WARNING` messages:
- Attempting to borrow item ID `101` when it was already borrowed (`Attempt to borrow unavailable item ID 101`).
- Attempting to return item ID `103` when it was not borrowed (`Attempt to return item ID 103 which is not borrowed`).
- Entering a non-existent item ID `999` (`Invalid ID: 999 does not exist`).
- Attempting to add new equipment with an existing ID `104` (`Invalid ID: duplicate item ID 104`).
- Choosing an invalid menu option `8` (`Invalid menu option selected: 8`).

### 3. What information does the traceback provide?
The traceback provides details about the unexpected error:
- The file name (`equipment_checkout.py`), line number (`line 40`), and function name (`borrow_item`) where the error happened.
- The exact line of code that failed: `item_id = int(raw_id)`.
- The exception type and message: `ValueError: invalid literal for int() with base 10: 'abc'`, which shows that the user typed `'abc'` instead of an integer.

### 4. How can the log file help a developer reconstruct the sequence of events?
- **Timestamps:** Every log entry has an exact date and time, showing the chronological order of actions from startup to shutdown.
- **Event levels (`INFO`, `WARNING`, `ERROR`):** The developer can see which user operations succeeded and which failed or were rejected in between.
- **State snapshots (`DEBUG`):** After every successful change, a `DEBUG` message records all item IDs and their `True`/`False` availability status, so the developer knows the exact state of the program at each step.

### 5. What is the difference between `log.error()` and `log.exception()`?
- `log.error()` only writes the error message text to the log file (unless `exc_info=True` is added manually).
- `log.exception()` is used inside an `except` block and automatically attaches the full exception traceback to the error message.