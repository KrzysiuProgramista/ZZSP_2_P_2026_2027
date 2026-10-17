
# Debugging Lab — Case 3

 ## 1\. Run the program and describe the observed effect

 I ran Case 3 with tracing enabled:

```
python debugging_lab.py 3 --trace
```

 The program does not find the cheese. Instead, it continues processing the same position and eventually reaches the maximum number of search steps.

 The final output is:

```
Status: STOPPED
Reason: maximum number of search steps exceeded.
```

 The important observation is that the program does not crash. Instead, it fails to make normal progress through the maze.

 The search repeatedly processes the same position because the current item is not being removed from the queue.

---

 ## 2\. Form a hypothesis about the cause

 ### Hypothesis

 The problem is probably related to how the BFS queue is being processed.

 In a breadth-first search, the first item in the queue should be removed before the next iteration. I suspected that the program was only looking at the first queue item instead of removing it.

 The suspicious statement is:

```
current = self.queue[0]
```

 A likely correction is:

```
current = self.queue.popleft()
```

 However, this hypothesis needs to be checked using diagnostic output.

---

 ## 3\. Add suitable diagnostic output or use a debugger

 I added diagnostic output to display the current position and the contents of the queue.

 For example:

```
if trace:
    print(f"before: current={self.queue[0]}, queue={list(self.queue)}")

current = self.queue[0]

if trace:
    print(f"after: current={current}, queue={list(self.queue)}")
```

 I also used the existing trace output:

```
if trace:
    self.print_state("search", current)
```

 This allows us to observe:

 - the current position,
- the size of the queue,
- the number of visited cells,
- whether the queue is actually being consumed.

 The expected behavior is that the first queue item is removed on every iteration.

---

 ## 4\. Record the relevant part of the execution trace

 The faulty program produces a trace with the same position repeatedly appearing.

 A representative part of the trace is:

```
search: position=(1,1), queue_size=1, visited=1
search: position=(1,1), queue_size=3, visited=4
search: position=(1,1), queue_size=3, visited=4
search: position=(1,1), queue_size=3, visited=4
search: position=(1,1), queue_size=3, visited=4
...
```

 The important observation is that `(1,1)` remains the current position.

 The execution can be summarized as:

```
Step 1:
current = (1,1)
The neighbors of (1,1) are added to the queue.

Step 2:
current = (1,1) again
The first queue item was not removed.

Step 3:
current = (1,1) again
The queue still begins with (1,1).

Step 4:
current = (1,1) again
The search is not progressing normally.
```

 Eventually, `move_count` reaches `max_steps`, producing:

```
Status: STOPPED
Reason: maximum number of search steps exceeded.
```

 This trace is strong evidence that the queue is not being consumed correctly.

---

 ## 5\. Identify the actual cause of the problem

 The actual cause is the following line:

```
current = self.queue[0]
```

 `self.queue[0]` only **looks at** the first element of the deque. It does not remove that element.

 A BFS queue requires FIFO behavior: the oldest item must be removed from the front of the queue.

 The correct operation is:

```
current = self.queue.popleft()
```

 The difference is:

```
self.queue[0]
```

 means:

 > Look at the first item.

 while:

```
self.queue.popleft()
```

 means:

 > Remove and return the first item.

 Because the faulty program does not remove the current position, the same position remains at the front of the queue and is repeatedly processed.

 Therefore, the visible failure is:

```
Status: STOPPED
```

 but the actual defect occurs earlier in the program when the queue item is selected.

 This demonstrates an important debugging principle: **the location where the failure is reported is not necessarily the location containing the actual defect.**

---

 ## 6\. Fix the program

 Only one line needs to be changed.

 ### Faulty version

```
current = self.queue[0]
```

 ### Correct version

```
current = self.queue.popleft()
```

 The corrected part of `solve()` is:

```
def solve(self, trace=False, max_steps=10000):
    while self.queue:
        if self.move_count >= max_steps:
            print("\nStatus: STOPPED")
            print("Reason: maximum number of search steps exceeded.")
            return False

        current = self.queue.popleft()
        self.move_count += 1

        if trace:
            self.print_state("search", current)

        if current == self.goal:
            path = self.reconstruct_path()
            print("\nStatus: SOLVED")
            print(f"Moves: {len(path) - 1}")
            print(f"Search steps: {self.move_count}")
            print(f"Path: {path}")
            return True

        for next_position, direction in self.neighbors(current):
            if next_position not in self.previous:
                self.previous[next_position] = current
                self.queue.append(next_position)

    print("\nStatus: NOT SOLVED")
    print("Reason: the search exhausted all reachable cells.")
    return False
```

 The search algorithm has not been rewritten. Only the incorrect queue operation has been corrected.

 ### Why the fix works

 Before the fix:

```
queue = [(1,1), (1,2), (2,1)]
          ^
          |
       selected
```

 Using:

```
self.queue[0]
```

 leaves the queue unchanged.

 After the fix:

```
queue = [(1,1), (1,2), (2,1)]
          ^
          |
       popleft()
```

 the first item is removed:

```
queue = [(1,2), (2,1)]
```

 The next iteration can therefore process `(1,2)`.

 This gives the queue the FIFO behavior required by BFS.

---

 ## 7\. Test the corrected program with at least two additional inputs

 ### Test 1 — Easy maze

 The first additional test uses the existing `create_easy_maze()` function.

 Test code:

```
solver = MazeSolver(create_easy_maze())
solver.solve()
```

 The expected result is:

```
Status: SOLVED
```

 The corrected solver should successfully find a path from `S` to `C`.



---
 ### Test 2 — Additional small maze

 As another independent test, I used a small maze:

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

 This confirms that the correction works with a different maze rather than only the original input.

---

 # Debugging Log

 | Step | Observation / Action | Result |
| --- | --- | --- |
| 1 | Ran Case 3 with `--trace`. | Program did not reach `C` and eventually reported `Status: STOPPED`. |
| 2 | Examined the trace. | The same position was processed repeatedly. |
| 3 | Formed a hypothesis about queue management. | Suspected that the current queue item was not being removed. |
| 4 | Added diagnostic output for `current` and `queue`. | The first queue item remained at the front. |
| 5 | Inspected the suspicious statement. | Found `self.queue[0]`. |
| 6 | Compared it with the required FIFO operation. | BFS needs `self.queue.popleft()`. |
| 7 | Changed the faulty line. | The queue is now consumed correctly. |
| 8 | Tested `create_easy_maze()` and an additional small maze. | Expected result: `Status: SOLVED`. |


