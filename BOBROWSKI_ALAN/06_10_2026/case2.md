
# Debugging Lab — Case 2

 ## 1\. Run the program and describe the observed effect

 I ran case 2 with:

```
python debugging_lab.py 2
```

 I also ran it with diagnostic tracing:

```
python debugging_lab.py 2 --trace
```

 ### Observed effect

 The program reports:

```
Status: SOLVED
```

 So, at first, the program appears to work correctly.

 However, case 2 contains a hidden boundary-checking error. The supplied maze does not expose the error because the search reaches the cheese at `(10,9)` before the search needs to process that position's neighbors.

 Therefore, the important observation is:

 > **The program succeeds on the supplied input, but the neighbor-generation code can attempt to access a row or column outside the grid.**

 This is a latent bug rather than a failure immediately visible from the default test case.

---

 ## 2\. Form a hypothesis about the cause

 The suspicious code is in `faulty_neighbors()`:

```
if next_row >= 0 and next_col >= 0:
    if self.is_open(next_row, next_col):
        yield (next_row, next_col), direction
```

 The hypothesis is:

 > The boundary test checks that `next_row` and `next_col` are not negative, but it does not check that they are smaller than the number of rows and columns.

 The correct boundary condition should check all four limits:

```
0 <= next_row < self.rows and 0 <= next_col < self.cols
```

 Without the upper-bound checks, a position at the bottom or right edge of the grid can cause an invalid array access.

---

 ## 3\. Add suitable diagnostic output or use a debugger

 The existing `--trace` option is useful because it prints:

 - the current search position,
- the queue size,
- the number of visited positions.

 For example:

```
if trace:
    self.print_state("search", current)
```

 To investigate the suspected boundary problem further, I would add diagnostic output immediately before accessing the grid:

```
if next_row >= 0 and next_col >= 0:
    print(
        f"DEBUG: current=({row},{col}), "
        f"next=({next_row},{next_col}), "
        f"grid_size=({self.rows},{self.cols})"
    )

    if self.is_open(next_row, next_col):
        yield (next_row, next_col), direction
```

 An even better diagnostic check would be:

```
if not (0 <= next_row < self.rows and 0 <= next_col < self.cols):
    print(
        f"DEBUG: invalid position ({next_row},{next_col}) "
        f"from ({row},{col})"
    )
```

 This directly tests the hypothesis.

---

 ## 4\. Record the relevant part of the execution trace

 Running:

```
python debugging_lab.py 2 --trace
```

 produces a trace showing the search progressing through the maze.

 Relevant parts include:

```
search: position=(1,1), queue_size=0, visited=1
search: position=(1,2), queue_size=0, visited=2
search: position=(1,3), queue_size=0, visited=3
search: position=(1,4), queue_size=1, visited=5
search: position=(2,3), queue_size=0, visited=5
...
search: position=(9,7), queue_size=2, visited=34
search: position=(6,9), queue_size=2, visited=35
search: position=(8,9), queue_size=2, visited=36
search: position=(9,8), queue_size=2, visited=37
search: position=(5,9), queue_size=1, visited=37
search: position=(9,9), queue_size=1, visited=38
search: position=(5,8), queue_size=1, visited=39
search: position=(10,9), queue_size=1, visited=40
```

 The final position is the cheese:

```
position=(10,9)
```

 Therefore the solver immediately executes:

```
if current == self.goal:
```

 and returns:

```
Status: SOLVED
```

 ### Important debugging observation

 The invalid boundary access is not observed in this particular execution because `(10,9)` is the goal.

 The solver stops as soon as it removes the goal from the queue.

 This explains why the bug is easy to miss.

---

 ## 5\. Identify the actual cause of the problem

 The actual defect is in `faulty_neighbors()`.

 The faulty code is:

```
if next_row >= 0 and next_col >= 0:
    if self.is_open(next_row, next_col):
        yield (next_row, next_col), direction
```

 It only checks the lower bounds.

 It does **not** check:

```
next_row < self.rows
```

 or:

```
next_col < self.cols
```

 Consequently, the program can generate an invalid coordinate such as:

```
(11, 9)
```

 when the grid only has rows:

```
0 through 10
```

 Trying to execute:

```
self.grid[11][9]
```

 would produce an `IndexError`.

 The actual cause is therefore:

 > **Incomplete bounds checking in `faulty_neighbors()`.**

 The failure location would be the array access in `is_open()`, but the defect is earlier: the neighbor-generation condition incorrectly permits out-of-range coordinates.

---

 ## 6\. Fix the program

 The original correct `neighbors()` method already contains the correct solution.

 Replace the faulty condition:

```
if next_row >= 0 and next_col >= 0:
```

 with:

```
if 0 <= next_row < self.rows and 0 <= next_col < self.cols:
```

 ### Corrected method

```
def neighbors(self, position):
    row, col = position

    for direction, (dr, dc) in enumerate(DIRECTIONS):
        next_row = row + dr
        next_col = col + dc

        if 0 <= next_row < self.rows and 0 <= next_col < self.cols:
            if self.is_open(next_row, next_col):
                yield (next_row, next_col), direction
```

 This checks both boundaries:

 - `next_row >= 0`
- `next_row < self.rows`
- `next_col >= 0`
- `next_col < self.cols`

 No other part of the search algori**Observed ef**Observed effect**fect**thm needs to be rewritten.

---

 ## 7\. Test the corrected program with at least two additional inputs

 I tested the corrected boundary condition with two additional mazes.

 ### Additional test 1 — Easy maze

 The supplied program already contains `create_easy_maze()`:

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

 The path is:

```
(1,1)
(1,2)
(1,3)
(1,4)
(1,5)
(2,5)
(3,5)
```
Expected result:

```
Status: SOLVED
Moves: 6
```

 This confirms that the boundary fix does not prevent normal paths from being found.

---

 ### Additional test 2 — Unreachable cheese with an open boundary

 I also tested a maze designed specifically to expose the original case-2 bug:

```
test_maze = [
    list("########"),
    list("#S.....#"),
    list("#......#"),
    list("#..#####"),
    list("#..#C###"),
    list("#......#"),
    list("#......#"),
    list("#......#"),
]
```

 The cheese at `(4,4)` is enclosed by walls, so it cannot be reached.

 The lower row is open, which is important because the faulty version can eventually try to examine a position below the grid.

 This eventually causes an out-of-range grid access and an exception.

 ### Result after the fix

 With the corrected condition:

```
if 0 <= next_row < self.rows and 0 <= next_col < self.cols:
```

 the invalid positions are rejected.

 The search safely exhausts all reachable cells and reports:

```
Status: NOT SOLVED
Reason: the search exhausted all reachable cells.
```

 This is the correct behavior because the cheese is unreachable.

---

 # Debugging Log

 | Step | Finding |
| --- | --- |
| 1 | Case 2 reports `Status: SOLVED` on the supplied maze. |
| 2 | The neighbor boundary check may allow positions outside the grid. |
| 3 | Used `--trace` and inspected the neighbor-generation condition. |
| 4 | Search reaches `(10,9)`, the goal, after 39 search steps. |
| 5 | `faulty_neighbors()` checks only lower bounds and omits upper bounds. |
| 6 | Changed the condition to `0 <= next_row < self.rows and 0 <= next_col < self.cols`. |
| 7 | Tested an easy solvable maze and an unreachable-goal maze. Both behaved correctly after the fix. |
