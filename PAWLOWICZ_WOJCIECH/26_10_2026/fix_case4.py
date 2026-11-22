"""
Debugging Lab -- Case 4
=======================

1. Observed effect: `python debugging_lab.py 4` prints
   "Status: NOT SOLVED / Reason: the search exhausted all reachable
   cells." even though the maze has an obvious path.

2. Hypothesis: `neighbors()` is yielding the wrong cells, so the BFS
   thinks it has explored everything when it hasn't actually walked the
   real corridors.

3. Diagnostic output: printing the neighbors of the start cell (1, 1)
   shows coordinates that don't correspond to any of the four cells
   actually touching (1, 1) in the printed maze.

4. Forward trace: for direction RIGHT (dr=0, dc=1) from (1, 1), the code
   computes `next_row = 1, next_col = 2` for the *bounds check*, but then
   yields `(wrong_row, next_col)` where `wrong_row = row + dc = 1 + 1 = 2`
   -- i.e. it reports the neighbor as (2, 2) instead of (1, 2). The row
   component is being shifted by the COLUMN delta.

5. Root cause:

       wrong_row = row + dc
       if self.is_open(wrong_row, next_col):
           yield (wrong_row, next_col), direction

   `wrong_row` reuses `dc` (the column delta) instead of `dr` (the row
   delta), so most "neighbors" reported are actually diagonal or
   duplicate cells, and genuine neighbors are missed -- the BFS silently
   walks a maze that isn't the one on screen.

6. Fix: yield `(next_row, next_col)`, exactly as computed from `dr`/`dc`
   at the top of the loop (see `fixed_neighbors` below).

7. Tested on the full maze and the easy maze.
"""

import debugging_lab as lab


def fixed_neighbors(self, position):
    row, col = position
    for direction, (dr, dc) in enumerate(lab.DIRECTIONS):
        next_row = row + dr
        next_col = col + dc
        if 0 <= next_row < self.rows and 0 <= next_col < self.cols:
            if self.is_open(next_row, next_col):  # <-- fix: use next_row
                yield (next_row, next_col), direction


def run(maze_factory, label):
    print(f"\n--- {label} (buggy) ---")
    lab.activate_case(4)
    solver = lab.MazeSolver(maze_factory())
    print(f"neighbors(start) = {list(solver.neighbors(solver.start))}")
    solver.solve()

    print(f"\n--- {label} (fixed) ---")
    lab.MazeSolver.neighbors = fixed_neighbors
    solver = lab.MazeSolver(maze_factory())
    print(f"neighbors(start) = {list(solver.neighbors(solver.start))}")
    solver.solve()


if __name__ == "__main__":
    run(lab.create_maze, "Full maze")
    run(lab.create_easy_maze, "Easy maze")
