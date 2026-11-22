"""
Debugging Lab -- Case 5
=======================

1. Observed effect: `python debugging_lab.py 5` never finishes and
   eventually gets killed by the OS (out of memory) instead of printing
   any status line at all -- the failure doesn't even look like the
   other cases' clean "STOPPED"/"NOT SOLVED" messages.

2. Hypothesis: the search frontier (`self.queue`) is growing without
   bound, because cells are being re-added after they've already been
   dequeued and fully processed.

3. Diagnostic output: printing `len(self.queue)` and `len(self.previous)`
   every iteration (with a tiny step cap) shows `queue` growing much
   faster than `previous` -- i.e. duplicate entries are being queued for
   cells that are already marked visited.

4. Forward trace: once a cell's neighbors have been queued and the cell
   itself is popped and discarded, it is no longer *in* `self.queue`
   (even though it's still a key of `self.previous`). The dedup check

       if next_position not in self.queue:

   therefore stops working the moment a cell leaves the queue: its
   neighbors keep re-adding it, each addition spawns more neighbor
   lookups, and the frontier grows combinatorially.

5. Root cause: the membership test is against the wrong collection.
   "Have I ever seen this cell?" is answered by `self.previous`
   (populated once and never shrunk), not by `self.queue` (which shrinks
   every time a cell is popped).

6. Fix: check `self.previous`, exactly as in the original `solve` (see
   `fixed_solve` below).

7. Tested on the full maze and the easy maze (with a step cap first, to
   safely show the buggy version's queue exploding before running the
   fixed version to completion).
"""

import debugging_lab as lab


def fixed_solve(self, trace=False, max_steps=10000):
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
            if next_position not in self.previous:  # <-- fix
                self.previous[next_position] = current
                self.queue.append(next_position)

    print("\nStatus: NOT SOLVED")
    print("Reason: the search exhausted all reachable cells.")
    return False


def demonstrate_queue_blowup(maze_factory, label, steps=12):
    print(f"\n--- {label} (buggy, queue growth over {steps} steps) ---")
    lab.activate_case(5)
    solver = lab.MazeSolver(maze_factory())
    for _ in range(steps):
        if not solver.queue:
            break
        before = len(solver.queue)
        solver.solve(max_steps=solver.move_count + 1)
        after = len(solver.queue)
        print(f"queue size: {before} -> {after} (visited={len(solver.previous)})")


def run_fixed(maze_factory, label):
    print(f"\n--- {label} (fixed) ---")
    lab.MazeSolver.solve = fixed_solve
    solver = lab.MazeSolver(maze_factory())
    solver.solve()


if __name__ == "__main__":
    demonstrate_queue_blowup(lab.create_easy_maze, "Easy maze")
    run_fixed(lab.create_maze, "Full maze")
    run_fixed(lab.create_easy_maze, "Easy maze")
