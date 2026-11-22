"""
Debugging Lab -- Case 1
=======================

1. Observed effect: running `python debugging_lab.py 1` prints
   "Status: NOT SOLVED / Reason: the search exhausted all reachable cells."
   even though the maze clearly has a path from S to C.

2. Hypothesis: the goal check itself is wrong, so the solver never
   recognises that it has reached the cheese.

3. Diagnostic output: re-running with `--trace` shows the BFS visiting
   every reachable cell, including the goal's neighbour (10, 8), but it
   never reports SOLVED.

4. Forward trace (relevant excerpt, via solver.print_state): the last
   cells visited before the queue empties are the ones along the bottom
   corridor, (10, 7) and (10, 8) among them -- but (10, 9), the actual
   cheese cell, is never printed as "current", which would be the case if
   the goal check matched it correctly.

5. Root cause: inside the patched `solve`, the win condition is

       if current == (self.goal[0], self.goal[1] - 1):

   instead of

       if current == self.goal:

   It compares against the cell one column to the LEFT of the cheese.
   In this maze that cell, (10, 8), is a wall ('#'), so it is never
   visited and the search always runs out of cells to explore -- the
   failure shows up as "exhausted all reachable cells" even though a
   valid path to the real goal exists.

6. Fix: compare `current` to `self.goal` directly (see
   `fixed_solve` below).

7. Tested on both the full maze and the easy maze (see `__main__`).
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

        if current == self.goal:  # <-- fix: compare with the real goal
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
    print(f"\n--- {label} (buggy) ---")
    lab.activate_case(1)
    solver = lab.MazeSolver(maze_factory())
    solver.solve()

    print(f"\n--- {label} (fixed) ---")
    lab.MazeSolver.solve = fixed_solve
    solver = lab.MazeSolver(maze_factory())
    solver.solve()


if __name__ == "__main__":
    run(lab.create_maze, "Full maze")
    run(lab.create_easy_maze, "Easy maze")
