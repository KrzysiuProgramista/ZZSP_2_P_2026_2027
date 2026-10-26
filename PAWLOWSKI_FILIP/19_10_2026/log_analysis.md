# Log analysis

I ran the program twice and both runs ended up in the same `app.log`. In the first run I went through 13 menu actions: some normal use, and then a bunch of mistakes on purpose. In the second run I started the program with `SIMULATE_FAILURE=borrow`, a switch I added for testing that makes the borrow function crash, so I could see how an unexpected error gets logged.

## 1. Which operations were recorded as successful?

Three operations changed something and were logged at INFO level: adding the Tripod (id 4), Anna borrowing the Laptop (id 1), and Anna returning it. Each of them is followed by a DEBUG line listing every item and whether it is available or borrowed. Starting and closing the program are also logged as INFO. Displaying the equipment (options 1 and 5) works fine but doesn't change anything, so I didn't log it.

## 2. Which invalid operations generated warnings?

All of these ended up as WARNING lines:

- Borrowing the Laptop while Anna still had it: "Borrow refused: id=1 is held by Anna"
- Returning the Projector, which was never borrowed: "Return refused: id=2 is not borrowed"
- Borrowing ID 99: "Invalid ID: no equipment with id=99"
- Adding a second item with ID 4: "Duplicate ID rejected"
- Typing `abc` instead of an ID: "Invalid ID entered"
- Choosing menu option 8: "Invalid menu option"

In every case the user only saw a short error message on screen. The details went to the log.

## 3. What information does the traceback provide?

The traceback at the end of the file comes from the second run. The last line tells me what went wrong: `RuntimeError: Simulated failure during 'borrow'`. Above it is the chain of calls that led there: `main`, then `handle`, then `borrow`, then `_maybe_fail`, each with a file name and line number. So I can see which function actually failed and which menu action started it, without having to guess or reproduce it. The line above the traceback ("Unexpected failure while handling the request") adds a bit of context. The program didn't crash, it printed a message and carried on until I exited. The crash happened before the item was changed, so the Projector stayed available.

## 4. How can the log file help a developer reconstruct the sequence of events?

Every line starts with a timestamp, so the file is basically a timeline. For example, you can read that the Laptop was borrowed by Anna, someone then tried to borrow it again and was refused, and after that it was returned. The DEBUG lines are useful too, because after each change they show the state of the whole inventory, so you can tell what it looked like at any moment even if you weren't watching. The levels also help when searching: WARNING for mistakes made by users, ERROR for real problems, INFO for a general overview. The two runs are easy to tell apart because each starts with "Application started".

## 5. What is the difference between `log.error()` and `log.exception()`?

Both write an ERROR message. `log.error()` only writes the text you give it. `log.exception()` also adds the full traceback of the exception being handled, which is why it has to be used inside an `except` block. For unexpected failures I used `log.exception()`, since the message alone wouldn't tell me where the problem happened.
