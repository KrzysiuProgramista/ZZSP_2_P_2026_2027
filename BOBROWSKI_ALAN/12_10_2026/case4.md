# Debugging Lab — Case 4

 ## 1\. Run the program and describe the observed effect

 Run Case 4 with tracing:

```
python debugging_lab.py 4 --trace
```

 The program produces a result similar to:

```
search: position=(1,1), queue_size=0, visited=1

Status: NOT SOLVED
Reason: the search exhausted all reachable cells.
```

 The expected result was:

```
Status: SOLVED
```

 but the program immediately reports `NOT SOLVED`.

 ### Observed effect

 The search starts at `(1,1)`, but it does not discover any new positions.

 This suggests that the problem is probably in the `neighbors()` function, because that function is responsible for generating the next positions.

---

 # 2\. Form a hypothesis about the cause

 The suspicious section is:

```
wrong_row = row + dc

if self.is_open(wrong_row, next_col):
    yield (wrong_row, next_col), direction
```

 The variable `wrong_row` is a strong clue.

 The program correctly calculates:

```
next_row = row + dr
next_col = col + dc
```

 but then ignores `next_row` and instead calculates:

```
wrong_row = row + dc
```

 ### Hypothesis

 The program is using the **column change (`dc`) to calculate the row**, instead of using the **row change (`dr`)**.

 This means the coordinates of neighboring cells are calculated incorrectly.

---

 # 3\. Add suitable diagnostic output

 To investigate, add diagnostic output inside `neighbors()`:

```
def faulty_neighbors(self, position):
    row, col = position

    for direction, (dr, dc) in enumerate(DIRECTIONS):
        next_row = row + dr
        next_col = col + dc

        if 0 <= next_row < self.rows and 0 <= next_col < self.cols:
            wrong_row = row + dc

            print(
                f"position=({row},{col}), "
                f"direction={DIRECTION_NAMES[direction]}, "
                f"dr={dr}, dc={dc}, "
                f"correct=({next_row},{next_col}), "
                f"wrong=({wrong_row},{next_col})"
            )

            if self.is_open(wrong_row, next_col):
                yield (wrong_row, next_col), direction
```

 This lets us compare the coordinates the program **should** calculate with the coordinates it actually uses.

---

 # 4\. Record the relevant part of the execution trace

 At the starting position:

```
(1,1)
```

 the directions are:

```
DIRECTIONS = [
    (-1, 0),  # UP
    (0, 1),   # RIGHT
    (1, 0),   # DOWN
    (0, -1),  # LEFT
]
```

 The diagnostic output will show the problem.

 ### UP

```
position=(1,1), direction=UP, dr=-1, dc=0,
correct=(0,1), wrong=(1,1)
```

 The correct neighbor should be:

```
(0,1)
```

 but the program checks:

```
(1,1)
```

---

 ### RIGHT

```
position=(1,1), direction=RIGHT, dr=0, dc=1,
correct=(1,2), wrong=(2,2)
```

 The correct neighbor should be:

```
(1,2)
```

 but the program checks:

```
(2,2)
```

 which is a wall.

---

 ### DOWN

```
position=(1,1), direction=DOWN, dr=1, dc=0,
correct=(2,1), wrong=(1,1)
```

 The correct neighbor should be:

```
(2,1)
```

 but the program checks:

```
(1,1)
```

 again.

---

 ### LEFT

```
position=(1,1), direction=LEFT, dr=0, dc=-1,
correct=(1,0), wrong=(0,0)
```

 Again, the calculated row is incorrect.

---

 # 5\. Identify the actual cause of the problem

 The actual bug is this line:

```
wrong_row = row + dc
```

 The program is using `dc` to calculate the row.

 The correct calculation was already made earlier:

```
next_row = row + dr
next_col = col + dc
```

 Therefore, the program should use:

```
next_row
```

 instead of:

```
wrong_row
```

 The bug is essentially:

```
Correct:

next_row = row + dr
next_col = col + dc

Incorrect:

wrong_row = row + dc
next_col = col + dc
```

 The row coordinate must use `dr`, while the column coordinate must use `dc`.

 ### Why the program doesn't crash

 This is an important debugging observation.

 The problem is not an exception. The program simply generates incorrect neighbors.

 Because the starting position is already in `self.previous`, the incorrectly generated `(1,1)` position is not added to the queue:

```
if next_position not in self.previous:
    self.previous[next_position] = current
    self.queue.append(next_position)
```

 Therefore, after processing the start, the queue becomes empty.

 The search then reports:

```
Status: NOT SOLVED
Reason: the search exhausted all reachable cells.
```

 The location where the program reports failure is therefore **not** where the defect exists.

---

 # 6\. Fix the program

 The smallest fix is to replace:

```
wrong_row = row + dc
```

 with:

```
wrong_row = row + dr
```

 However, since the variable is no longer wrong, it is clearer to use `next_row` directly.

 ### Faulty code

```
wrong_row = row + dc

if self.is_open(wrong_row, next_col):
    yield (wrong_row, next_col), direction
```

 ### Corrected code

```
if self.is_open(next_row, next_col):
    yield (next_row, next_col), direction
```

 So the corrected `neighbors()` method is:

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

 This is essentially the original correct version of `neighbors()`.

 The search algorithm itself has **not** been rewritten.

---

 # 7\. Test the corrected program with additional inputs

 

 ## Test 1 — Easy maze

 Test the corrected `MazeSolver` using `create_easy_maze()`:

```
solver = MazeSolver(create_easy_maze())
solver.solve()
```

 Expected result:

```
Status: SOLVED
```

 This confirms that the neighbor calculation works on a simpler maze as well.

---

 ## Test 2 — Small additional maze

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

 This gives another independent test of the corrected neighbor calculation.

---

 # Debugging Log

 | Step | Observation / Action | Result |
| --- | --- | --- |
| 1 | Ran Case 4 with `--trace`. | Program reported `Status: NOT SOLVED`. |
| 2 | Observed that only the starting position was processed. | Search did not discover new cells. |
| 3 | Suspected a problem in `neighbors()`. | Neighbor generation controls movement through the maze. |
| 4 | Added diagnostic output for `row`, `col`, `dr`, `dc`, `next_row`, and `next_col`. | Incorrect coordinates were revealed. |
| 5 | Compared correct and incorrect coordinates. | `wrong_row` was calculated using `dc` instead of `dr`. |
| 6 | Identified the faulty statement. | `wrong_row = row + dc`. |
| 7 | Corrected the coordinate calculation. | Changed it to use `next_row = row + dr`. |
| 8 | Tested `create_easy_maze()` and an additional small maze. | Expected result: `Status: SOLVED`. |

---
