"""
Debugging Lab -- Case 3
=======================

1. Observed effect: `python debugging_lab.py 3` prints
   "Status: STOPPED / Reason: maximum number of search steps exceeded."
   -- the program doesn't crash, it just never finishes.

2. Hypothesis: the search is stuck processing the same cell over and over
   (an infinite loop), rather than genuinely exploring new ground.

3. Diagnostic output: running with `--trace` shows the exact same
   `position=(1,1)` printed thousands of times in a row, with
   `queue_size` growing every iteration instead of shrinking.

4. Forward trace: `move_count` increases every iteration (so the loop
   isn't truly stuck), but `current` never changes and `visited` only
   grows by the handful of neighbors of (1,1) before leveling off --
   proving the same cell is reprocessed indefinitely.

5. Root cause:

       current = self.queue[0]

   peeks at the front of the queue instead of removing it. The real BFS
   invariant is "process a cell once, then remove it from the frontier";
   here the first cell is inspected again and again because it is never
   popped off.

6. Fix: use `self.queue.popleft()`, as in the original `solve` (see
   `fixed_solve` below).

7. Tested on the full maze and the easy maze.
"""

import debugging_lab as lab


def fixed_solve(self, trace=False, max_steps=10000):
    while self.queue:
        if self.move_count >= max_steps:
            print("\nStatus: STOPPED")
            print("Reason: maximum number of search steps exceeded.")
            return False

        current = self.queue.popleft()  # <-- fix: actually dequeue
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
            if next_position not in self.previous:
                self.previous[next_position] = current
                self.queue.append(next_position)

    print("\nStatus: NOT SOLVED")
    print("Reason: the search exhausted all reachable cells.")
    return False


def run(maze_factory, label):
    print(f"\n--- {label} (buggy, trace shows it stalling) ---")
    lab.activate_case(3)
    solver = lab.MazeSolver(maze_factory())
    solver.solve(trace=True, max_steps=10)  # small cap to show the stall quickly
    print(f"(note: position above never advances past the start cell)")

    print(f"\n--- {label} (fixed) ---")
    lab.MazeSolver.solve = fixed_solve
    solver = lab.MazeSolver(maze_factory())
    solver.solve()


if __name__ == "__main__":
    run(lab.create_maze, "Full maze")
    run(lab.create_easy_maze, "Easy maze")
