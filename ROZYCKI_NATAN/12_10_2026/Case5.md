# Case 5 - Debugging Log

## 1. Run the program and describe the observed effect.

Command:
```bash
python debug_lab.py 5
```

Output:
```text
Status: STOPPED
Reason: maximum number of search steps exceeded.
```

The search hits the maximum limit of 10,000 steps without reaching the goal.

---

## 2. Form a hypothesis about the cause.
### Visited states are not tracked properly, causing nodes that have already been expanded to be repeatedly re-added to the frontier in an infinite cycle.

---

## 3. Add suitable diagnostic output or use a debugger.
Running it with `--trace`:
```bash
python debug_lab.py 5 --trace
```

---

## 4. Record the relevant part of the execution trace.
```text
search: position=(1,1), queue_size=1, visited=1
search: position=(1,2), queue_size=1, visited=2
search: position=(1,1), queue_size=2, visited=2
search: position=(1,3), queue_size=2, visited=3
search: position=(1,2), queue_size=2, visited=3
... (cycles back and forth indefinitely between adjacent cells)
```
The solver endlessly bounces back and forth between previously visited adjacent cells.

---

## 5. Identify the actual cause of the problem.
In `faulty_solve`:
```python
for next_position, direction in self.neighbors(current):
    if next_position not in self.queue:
        self.previous[next_position] = current
        self.queue.append(next_position)
```
The condition tests `self.queue` instead of `self.previous`. Once a node is popped from `self.queue`, it is no longer in `self.queue`, allowing its neighbors to re-enqueue it.

---

## 6. Fix the program.
Check membership against the visited dictionary (`self.previous`):
```python
if next_position not in self.previous:
    self.previous[next_position] = current
    self.queue.append(next_position)
```

---

## 7. Test the corrected program with at least two additional inputs.
- ### Case 5 Maze: `Status: SOLVED`, `Moves: 23`, `Search steps: 38`.
- ### Test 1 (`create_easy_maze`): `Status: SOLVED`, `Moves: 8`.
- ### Test 2 (`Straight Corridor ["#####", "#S.C#", "#####"]`): `Status: SOLVED`, `Moves: 2`.