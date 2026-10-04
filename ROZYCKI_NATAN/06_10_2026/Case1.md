# Case 1 - Debugging Log

## 1. Run the program and describe the observed effect.

Command:
```bash
python debug_lab.py 1
```

Output:
```text
Status: NOT SOLVED
Reason: the search exhausted all reachable cells.
```

The solver searches all reachable cells in the maze and terminates **without** finding the cheese C, even though an open path visibly **exists**.

---

## 2. Form a hypothesis about the cause.
### The search algorithm explores valid cells, but the termination condition checking whether the goal has been reached either never evaluates to `True` or checks an unreachable/wrong coordinate.

---

## 3. Add suitable diagnostic output or use a debugger.
Running it with **--trace**
```bash
python debug_lab.py 1 --trace
```
Adding diagnostic output right before the goal check in `solve`:

```python
if trace:
    print(f"DEBUG: current={current}, target={(self.goal[0], self.goal[1] - 1)}, actual_goal={self.goal}")
```

---

## 4. Record the relevant part of the execution trace.

```text
search: position=(10,9), queue_size=0, visited=38
DEBUG: current=(10, 9), target=(10, 8), actual_goal=(10, 9)
```
The search actually visits the cheese cell at `(10, 9)`, but it does not stop because it compares current to `(10, 8)`. Position `(10, 8)` is a wall `(#)`, which is never enqueued. Once `(10, 9)` is popped, the queue empties.

---

## 5. Identify the actual cause of the problem.

In `faulty_solve`:
```python
if current == (self.goal[0], self.goal[1] - 1):
```

The goal condition offsets the column by -1. Additionally, `reconstruct_path()` expects `self.goal` in self.previous, so even if `(self.goal[0], self.goal[1] - 1)` were reachable, the reconstructed path to `self.goal` would fail.

---

## 6. Fix the program.

Compare `current` directly with `self.goal`:

```python
if current == self.goal:
    path = self.reconstruct_path()
    ...
```

---

## 7. Test the corrected program with at least two additional inputs.

- ### Case 1 Maze: Status: `SOLVED`, `Moves: 23`, `Search steps: 38`.
- ### Test 1 (`create_easy_maze`): `Status: SOLVED`, `Moves: 8`.
- ### Test 2 (`Straight Corridor ["#####", "#S.C#", "#####"]`): `Status: SOLVED`, `Moves: 2`.
