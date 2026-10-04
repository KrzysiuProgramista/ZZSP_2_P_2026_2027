
# Case 1 — Debugging Log

 ## 1\. Run the program and describe the observed effect

 I ran:

```
python debugging_lab.py 1
```

 The program displayed the maze and then ended with:

```
Status: NOT SOLVED
Reason: the search exhausted all reachable cells.
```

 There was **no crash**. The search explored the reachable cells but did not recognize the cheese as the goal.

---

 ## 2\. Form a hypothesis about the cause

 My hypothesis is that the **BFS search itself is working correctly**, but the program is checking the wrong position when deciding whether the cheese has been found.

 The suspicious condition is:

```
if current == (self.goal[0], self.goal[1] - 1):
```

 This suggests a possible **off-by-one error** in the goal comparison.

---

 ## 3\. Add suitable diagnostic output or use a debugger

 I ran the program in trace mode:

```
python debugging_lab.py 1 --trace
```

 The existing diagnostic output shows the position being searched.

 To make the goal comparison clearer, I could temporarily add:

```
if trace:
    print(f"current={current}, goal={self.goal}")
```

 immediately before the faulty `if` statement.

 This allows me to compare the current search position directly with the actual goal position.

---

 ## 4\. Record the relevant part of the execution trace

 The actual cheese position is:

```
goal = (10, 9)
```

 However, the faulty condition checks:

```
(10, 9 - 1)
```

 which evaluates to:

```
(10, 8)
```

 Therefore, when the search reaches the cheese at `(10, 9)`, the condition is false:

```
current = (10, 9)
goal    = (10, 9)

expected: current == goal       → True
actual:   current == (10, 8)    → False
```

 The search therefore continues until the queue becomes empty.

 The program then reports:

```
Status: NOT SOLVED
Reason: the search exhausted all reachable cells.
```

---

 ## 5\. Identify the actual cause of the problem

 The actual cause is an **off-by-one error** in the goal comparison.

 The program uses:

```
if current == (self.goal[0], self.goal[1] - 1):
```

 This checks the square **immediately to the left of the cheese** rather than the cheese itself.

 ### Root Cause

 > The problem is in the **goal-detection condition**, not in the BFS search algorithm.

---

 ## 6\. Fix the program

 I changed:

```
if current == (self.goal[0], self.goal[1] - 1):
```

 to:

```
if current == self.goal:
```

 The corrected section is:

```
if current == self.goal:
    path = self.reconstruct_path()
    print("\nStatus: SOLVED")
    print(f"Moves: {len(path) - 1}")
    print(f"Search steps: {self.move_count}")
    print(f"Path: {path}")
    return True
```

 No other part of the search algorithm needs to be changed.

---

 ## 7\. Test the corrected program

 The corrected program was tested with **two additional inputs**.

 ### Test 1 — Easy Maze

 The program already contains an additional maze called `create_easy_maze()`:

```
def create_easy_maze():
    return [
        list("#######"),
        list("#S....#"),
        list("#####.#"),
        list("#....C#"),
        list("#######"),
    ]
```

 To test it, I temporarily changed:

```
solver = MazeSolver(create_maze())
```

 to:

```
solver = MazeSolver(create_easy_maze())
```

 Then I ran:

```
python debugging_lab.py 1
```

 The corrected program reported:

```
Status: SOLVED
```

 **Expected result:** The corrected goal comparison works with another maze.

---

 ### Test 2 — Maze with a Different Goal Location

 I added another test maze:

```
def create_test_maze():
    return [
        list("#######"),
        list("#S....#"),
        list("###.#.#"),
        list("#...#C#"),
        list("#######"),
    ]
```

 I then temporarily changed:

```
solver = MazeSolver(create_maze())
```

 to:

```
solver = MazeSolver(create_test_maze())
```

 and ran:

```
python debugging_lab.py 1
```

 The corrected program reported:

```
Status: SOLVED
```

 Expected result: This test confirms that the program correctly recognizes the cheese when it is located at different coordinates.

---

 # Debugging log

 | Step | Finding |
| --- | --- |
| 1 | The program reports `NOT SOLVED` even though a path to the cheese exists. |
| 2 | The goal-detection condition is checking the wrong coordinate. |
| 3 | Trace output was used to compare `current` with `self.goal`. |
| 4 | An off-by-one error changes the target from `self.goal` to the cell immediately to its left. |
| 5 | Replace the incorrect comparison with `if current == self.goal:` |
| 6 | The corrected program was tested with `create_easy_maze()` and an additional maze with a different cheese location. |
| 7 | Both tests reported `Status: SOLVED`. |
