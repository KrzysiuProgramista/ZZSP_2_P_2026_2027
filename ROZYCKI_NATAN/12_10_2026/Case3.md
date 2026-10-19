# Case 3 - Debugging Log

## 1. Run the program and describe the observed effect.

Command:
```bash
python debug_lab.py 3
```

Output:
```text
Status: STOPPED
Reason: maximum number of search steps exceeded.
```

The search hits the safety threshold (10,000 steps) and stops without making any forward progress.

---

## 2. Form a hypothesis about the cause.
### The algorithm is trapped in a loop because the current node is never dequeued, repeatedly processing the first item without advancing the frontier.

---

## 3. Add suitable diagnostic output or use a debugger.
Running it with `--trace`:
```bash
python debug_lab.py 3 --trace
```

---

## 4. Record the relevant part of the execution trace.
```text
search: position=(1,1), queue_size=1, visited=1
search: position=(1,1), queue_size=2, visited=2
search: position=(1,1), queue_size=2, visited=2
search: position=(1,1), queue_size=2, visited=2
... (repeats 10,000 times)
```
The search position remains stuck at `(1, 1)` on every step while `move_count` increments until it terminates at 10,000.

---

## 5. Identify the actual cause of the problem.
In `faulty_solve`:
```python
current = self.queue[0]
```
`self.queue[0]` inspects the head node without removing it. On iteration 1, neighbors of `(1, 1)` are added. On subsequent iterations, `current` is still `(1, 1)`, whose neighbors are already in `previous`, so the queue never progresses.

---

## 6. Fix the program.
Change index peeking to `popleft()`:
```python
current = self.queue.popleft()
```

---

## 7. Test the corrected program with at least two additional inputs.
- ### Case 3 Maze: `Status: SOLVED`, `Moves: 23`, `Search steps: 38`.
- ### Test 1 (`create_easy_maze`): `Status: SOLVED`, `Moves: 8`.
- ### Test 2 (`Straight Corridor ["#####", "#S.C#", "#####"]`): `Status: SOLVED`, `Moves: 2`.

---