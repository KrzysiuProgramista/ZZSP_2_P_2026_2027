# Debugging Lab — Case 5

 ## 1\. Run the program and describe the observed effect

 Run Case 5 with tracing enabled:

```
python debugging_lab.py 5 --trace
```

 The program does not behave like a normal BFS. It may continue processing many positions and eventually reach:

```
Status: STOPPED
Reason: maximum number of search steps exceeded.
```

 The important symptom is that the search can add the **same position to the queue multiple times**.

 The program is supposed to keep track of every position it has already visited. However, Case 5 uses the queue itself for this check.

 The suspicious code is:

```
if next_position not in self.queue:
```

---

 # 2\. Form a hypothesis about the cause

 ### Hypothesis

 The program is using the wrong collection to determine whether a position has already been visited.

 The correct program uses:

```
if next_position not in self.previous:
```

 But Case 5 uses:

```
if next_position not in self.queue:
```

 A queue only contains positions that are **currently waiting to be processed**.

 It does not contain positions that have already been processed.

 Therefore, once a position has been removed from the queue, it is no longer in `self.queue`, even though it has already been visited.

 The hypothesis is that this allows already-visited positions to be added to the queue again.

---

 # 3. Add suitable diagnostic output or use a debugger

 Add diagnostic output inside the loop:

```
for next_position, direction in self.neighbors(current):
    print(
        f"current={current}, "
        f"next={next_position}, "
        f"in_queue={next_position in self.queue}, "
        f"in_previous={next_position in self.previous}"
    )

    if next_position not in self.queue:
        self.previous[next_position] = current
        self.queue.append(next_position)
```

 This allows us to compare:

```
next_position in self.queue
```

 with:

```
next_position in self.previous
```

 The important observation is that these two conditions mean different things.

 ### `self.queue`

 Contains positions that are **waiting to be processed**.

 ### `self.previous`

 Contains positions that have **already been discovered/visited**.

 Therefore, `self.previous` is the correct collection for the visited check.

---

 # 4\. Record the relevant execution trace

 A representative trace can look like this:

```
current=(1,1), next=(1,2), in_queue=False, in_previous=False
current=(1,1), next=(2,1), in_queue=False, in_previous=False

current=(1,2), next=(1,1), in_queue=False, in_previous=True
```

 The last line is the important one.

 We have:

```
next = (1,1)
in_queue = False
in_previous = True
```

 The position `(1,1)` has already been visited.

 However, because it has already been removed from the queue, it is no longer in `self.queue`.

 Therefore:

```
next_position not in self.queue
```

 evaluates to:

```
True
```

 and the program incorrectly adds `(1,1)` to the queue again.

 The correct test would be:

```
next_position not in self.previous
```

 which evaluates to:

```
False
```

 because `(1,1)` has already been visited.

---

 # 5\. Identify the actual cause of the problem

 The actual bug is:

```
if next_position not in self.queue:
```

 The program is using the **queue** as if it were the visited set.

 That is incorrect.

 The queue answers:

 > Which positions are waiting to be processed?

 The `previous` dictionary answers:

 > Which positions have already been discovered?

 These are not the same thing.

 For example:

```
Queue:
[(2,3), (3,4)]
```

 A position such as `(1,1)` might not be in the queue because it has already been processed.

 But:

```
previous:
{
    (1,1): None,
    (1,2): (1,1),
    ...
}
```

 still contains `(1,1)`.

 So:

```
next_position not in self.queue
```

 can incorrectly say:

```
True
```

 while:

```
next_position not in self.previous
```

 correctly says:

```
False
```

 ### Why this causes a problem

 The maze is a graph. Cells can have connections back to cells that have already been visited.

 Without a proper visited check, the algorithm can repeatedly add previously visited cells to the queue.

 This causes unnecessary processing and can lead to the search exceeding:

```
max_steps
```

 The failure is therefore caused by incorrect **visited-state management**, not by the queue itself.

---

 # 6\. Fix the program

 Only one line needs to be changed.

 ### Faulty code

```
for next_position, direction in self.neighbors(current):
    if next_position not in self.queue:
        self.previous[next_position] = current
        self.queue.append(next_position)
```

 ### Correct code

```
for next_position, direction in self.neighbors(current):
    if next_position not in self.previous:
        self.previous[next_position] = current
        self.queue.append(next_position)
```

 The corrected `solve()` section is:

```
for next_position, direction in self.neighbors(current):
    if next_position not in self.previous:
        self.previous[next_position] = current
        self.queue.append(next_position)
```

 ### Why this fixes the problem

 When a position is first discovered, it is immediately added to `self.previous`:

```
self.previous[next_position] = current
```

 Therefore, if the same position is encountered again later:

```
next_position not in self.previous
```

 will be `False`.

 The position will not be added to the queue again.

 This prevents duplicate visits and allows BFS to progress normally.

---

 # 7\. Test the corrected program with at least two additional inputs

 ## Test 1 — Easy maze

 Test the corrected solver using the easy maze:

```
solver = MazeSolver(create_easy_maze())
solver.solve()
```

 Expected result:

```
Status: SOLVED
```

 This confirms that the visited-state correction works on a simpler maze.

---

 ## Test 2 — Additional small maze

 Use another maze:

```
small_maze = [
    list("#####"),
    list("#S..#"),
    list("###.#"),
    list("#..C#"),
    list("#####"),
]

solver = MazeSolver(small_maze)
solver.solve()
```

 Expected result:

```
Status: SOLVED
```

 This provides another independent test of the corrected search.

---

 # Debugging Log

 | Step | Observation / Action | Result |
| --- | --- | --- |
| 1 | Ran Case 5 with `--trace`. | Search did not behave normally and could exceed the maximum search steps. |
| 2 | Observed repeated processing of positions. | Suspected that already-visited cells were being added again. |
| 3 | Inspected the membership test. | Found `next_position not in self.queue`. |
| 4 | Added diagnostic output for `in_queue` and `in_previous`. | Found positions that were not in the queue but were already in `previous`. |
| 5 | Compared the two collections. | Queue contains waiting positions; `previous` contains discovered positions. |
| 6 | Identified the actual cause. | The queue was incorrectly being used as the visited check. |
| 7 | Changed the membership test. | Replaced `self.queue` with `self.previous`. |
| 8 | Tested `create_easy_maze()` and an additional small maze. | Expected result: `Status: SOLVED`. |

---
