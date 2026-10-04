# Case 4 - Debugging Log

## 1. Run the program and describe the observed effect.

Command:
```bash
python debug_lab.py 4
```

Output:
```text
Status: NOT SOLVED
Reason: the search exhausted all reachable cells.
```

The search terminates immediately after step 1, failing to find a path.

---

## 2. Form a hypothesis about the cause.
### The neighbor calculation applies directional offsets incorrectly (e.g., swapping row/column deltas), calculating invalid or diagonal coordinates that lead into walls or loops.

---

## 3. Add suitable diagnostic output or use a debugger.
Running it with `--trace`:
```bash
python debug_lab.py 4 --trace
```
Adding diagnostic output in `faulty_neighbors`:
```python
print(f"DEBUG: pos=({row},{col}), dir={DIRECTION_NAMES[direction]}, candidate=({wrong_row},{next_col})")
```

---

## 4. Record the relevant part of the execution trace.
```text
search: position=(1,1), queue_size=1, visited=1
DEBUG: pos=(1,1), dir=UP, candidate=(1,1)
DEBUG: pos=(1,1), dir=RIGHT, candidate=(2,2)
DEBUG: pos=(1,1), dir=DOWN, candidate=(1,1)
DEBUG: pos=(1,1), dir=LEFT, candidate=(0,0)
Status: NOT SOLVED
```
From `(1, 1)`, `UP` and `DOWN` produce `(1, 1)` (self-loop), `RIGHT` produces `(2, 2)` (wall), and `LEFT` produces `(0, 0)` (wall). No valid neighbors are added, and the queue empties on step 1.

---

## 5. Identify the actual cause of the problem.
In `faulty_neighbors`:
```python
wrong_row = row + dc
if self.is_open(wrong_row, next_col):
    yield (wrong_row, next_col), direction
```
The row coordinate is incremented by `dc` (column delta) instead of `dr` (row delta), generating invalid diagonal and stationary moves.

---

## 6. Fix the program.
Use `next_row = row + dr` for checking and yielding:
```python
if 0 <= next_row < self.rows and 0 <= next_col < self.cols:
    if self.is_open(next_row, next_col):
        yield (next_row, next_col), direction
```

---

## 7. Test the corrected program with at least two additional inputs.
- ### Case 4 Maze: `Status: SOLVED`, `Moves: 23`, `Search steps: 38`.
- ### Test 1 (`create_easy_maze`): `Status: SOLVED`, `Moves: 8`.
- ### Test 2 (`Straight Corridor ["#####", "#S.C#", "#####"]`): `Status: SOLVED`, `Moves: 2`.

---