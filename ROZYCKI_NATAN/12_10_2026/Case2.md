# Case 2 - Debugging Log

## 1. Run the program and describe the observed effect.

Command:
```
python debug_lab.py 2
```

Output:
```text
Status: CRASHED
Exception: IndexError: list index out of range
```

The program crashes with an `IndexError` while checking whether neighboring cells are open.

---

## 2. Form a hypothesis about the cause.
### The neighbor generation logic checks lower bounds (`>= 0`) but forgets upper boundary bounds (`< rows`, `< cols`), causing an out-of-bounds grid access when exploring along the edge.

---

## 3. Add suitable diagnostic output or use a debugger.
Running it with `--trace`:
```bash
python debug_lab.py 2 --trace
```
Adding diagnostic output right inside `faulty_neighbors`:
```python
print(f"DEBUG: checking ({next_row}, {next_col}) against dimensions ({self.rows}, {self.cols})")
```

---

## 4. Record the relevant part of the execution trace.
```text
search: position=(10,9), queue_size=0, visited=38
DEBUG: checking (11, 9) against dimensions (11, 11)
Traceback (most recent call last):
  File "debug_lab.py", line 124, in is_open
    return self.grid[row][col] != WALL
IndexError: list index out of range
```
At position `(10, 9)`, the downward move calculates `next_row = 11`. Because `11 >= self.rows (11)`, `self.is_open(11, 9)` crashes when accessing `self.grid[11]`.

---

## 5. Identify the actual cause of the problem.
In `faulty_neighbors`:
```python
if next_row >= 0 and next_col >= 0:
    if self.is_open(next_row, next_col):
        yield (next_row, next_col), direction
```
The condition only guards against negative indices and misses the upper limit bounds `next_row < self.rows` and `next_col < self.cols`.

---

## 6. Fix the program.
Add the missing upper bounds checks:
```python
if 0 <= next_row < self.rows and 0 <= next_col < self.cols:
    if self.is_open(next_row, next_col):
        yield (next_row, next_col), direction
```

---

## 7. Test the corrected program with at least two additional inputs.
- ### Case 2 Maze: `Status: SOLVED`, `Moves: 23`, `Search steps: 38`.
- ### Test 1 (`create_easy_maze`): `Status: SOLVED`, `Moves: 8`.
- ### Test 2 (`Straight Corridor ["#####", "#S.C#", "#####"]`): `Status: SOLVED`, `Moves: 2`.

---