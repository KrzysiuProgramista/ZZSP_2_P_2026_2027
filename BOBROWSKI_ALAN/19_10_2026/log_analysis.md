# Equipment Checkout Application — Log Analysis

## 1. Which operations were recorded as successful?

The log records the following successful operations:

- Registration of equipment ID 104 (Tablet).
- Borrowing and returning equipment ID 101 (Laptop).
- Borrowing and returning equipment ID 104 (Tablet).
- Registration of equipment ID 105 (Microphone).
- A subsequent successful borrowing of equipment ID 101.


## 2. Which invalid operations generated warnings?

The following invalid operations generated WARNING messages:
- Attempting to borrow equipment that was already borrowed (ID 101).
- Attempting to return equipment that was not borrowed (ID 102).
- Attempting to borrow a nonexistent equipment ID (999).
- Selecting an invalid menu option (9).
- Attempting to borrow equipment using an invalid negative ID (-5).


## 3. What information does the traceback provide?

The traceback identifies the exception type, the error message, and the location in the source code where the failure occurred.

In this test, the exception is `KeyError: 'available'`. The deliberately corrupted equipment record for ID 106 does not contain the `available` field. When the borrowing method tries to access this missing dictionary key, Python raises a KeyError.

The traceback helps the developer locate the failing statement and investigate why the inventory data was incomplete.

## 4. How can the log file help a developer reconstruct the sequence of events?

Each log entry includes a timestamp, severity level, and descriptive message. By examining these entries in chronological order, a developer can reconstruct equipment registrations, borrowing and returning operations, changes in availability, invalid actions, and unexpected failures.

DEBUG messages provide snapshots of the inventory after successful changes. WARNING messages identify invalid operations, while ERROR messages and tracebacks help diagnose failures.

This information is useful for debugging, auditing equipment usage, and identifying recurring problems.

## 5. What is the difference between `log.error()` and `log.exception()`?

Both methods record errors, but they differ in how they handle exception details.

- `log.error()` records an error message. It does not automatically include the active exception's traceback.
- `log.exception()` records an error message and automatically includes the traceback of the active exception. It should normally be called inside an `except` block.
