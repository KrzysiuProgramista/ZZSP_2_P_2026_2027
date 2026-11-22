# Debugging log — `debugging_lab.py` (Chapter 19 exercise)

Each case follows the same discipline used in the Chapter 19 slides:
observed effect -> hypothesis -> instrumentation / forward trace -> root
cause -> fix -> re-test. The full reasoning for each case lives as a
docstring at the top of its own script (`fix_case1.py` .. `fix_case5.py`);
this file is the short summary table.

| Case | Observed effect | Root cause | Where the defect lives relative to where it fails |
|------|------------------|------------|----------------------------------------------------|
| 1 | "NOT SOLVED", search exhausts all cells | Goal check compares against `(goal_row, goal_col - 1)` instead of `goal` — that cell is a wall, so it's never reached | Fails in `solve`'s goal test; the defect *is* at the failure site this time, but only inspection of the comparison (not the crash) reveals it |
| 2 | "SOLVED" with a correct path (looks fine!) | `neighbors` only checks the lower bound (`>= 0`), not the upper bound (`< rows`/`< cols`) — a **latent** bug that this particular maze never triggers | No visible failure at all; found by code reading / direct unit-level testing of `neighbors`, not by running `solve` |
| 3 | "STOPPED", max steps exceeded, trace shows the same position forever | `current = self.queue[0]` peeks instead of `popleft()`-ing | Fails in the loop that uses `current`, and the defect is on the very same line — the one case where cause and effect coincide |
| 4 | "NOT SOLVED", search exhausts all cells | `wrong_row = row + dc` mixes up the row/column deltas, so `neighbors` yields the wrong cells | Fails in `solve` (can't find a path), but the defect is one call away, inside `neighbors` |
| 5 | No clean status — process killed (OOM) | Dedup check is `next_position not in self.queue` instead of `not in self.previous`; cells already popped are no longer "in the queue" so they get re-enqueued forever | Fails catastrophically (no diagnostic message at all) far downstream of the single wrong word (`queue` vs. `previous`) |

## General technique used across all five cases

1. **Reproduce** the exact reported effect first (never guess).
2. **Instrument before assuming** — `print_state`/`print` calls inserted at
   the one place that matters (the BFS loop, or inside `neighbors`) turn
   "something is wrong" into "here is exactly what the state looks like
   right before/after the mistake fires".
3. **Keep the instrumentation minimal** — one well-chosen trace line
   (position, queue size, visited count) told us more than dumping the
   entire state every iteration.
4. **Read tracebacks and reasoning top-down**: the frame where an
   exception is raised is not always where the mistake was made (classic
   in cases 2 and 4: the defect and the symptom are in different
   functions).
5. **Confirm, don't just assume, the fix** — every case is re-run on both
   the provided maze and a second ("easy") maze after the fix, and case 2
   additionally gets a direct, targeted test of the exact code path that
   was unsafe but never actually exercised by the given maze.
