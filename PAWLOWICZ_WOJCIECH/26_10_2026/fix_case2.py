"""
Debugging Lab -- Case 2
=======================

1. Observed effect: `python debugging_lab.py 2` actually prints
   "Status: SOLVED" with a correct-looking path on the given maze -- so at
   first glance there seems to be nothing to fix.

2. Hypothesis: the bug is latent rather than overt (see the intro slides:
   a program that runs correctly on one test input is not necessarily bug
   free). Something in `neighbors` looks suspicious even though this
   particular maze doesn't trigger a crash.

3. Diagnostic output: printing `self.rows` / `self.cols` and comparing
   them against the bounds actually checked in the patched `neighbors`
   shows that only the LOWER bound (`>= 0`) is checked for each
   coordinate; the UPPER bound (`< self.rows` / `< self.cols`) is missing.

4. Forward trace: on THIS maze every cell adjacent to the outer wall ring
   happens to be a wall itself, so `is_open(next_row, next_col)` is only
   ever called with in-range coordinates by coincidence -- the goal sits
   one row above the bottom wall and one column left of the right wall,
   so the BFS reaches it before it would ever need to probe a truly
   out-of-range cell. On the easy maze below, the same missing check
   still happens not to be hit, but a maze whose solution path hugs the
   bottom-right corner would raise `IndexError: list index out of range`.

5. Root cause: in `faulty_neighbors`,

       if next_row >= 0 and next_col >= 0:

   should also require `next_row < self.rows` and `next_col < self.cols`.

6. Fix: restore both bounds, as in the original `neighbors` method (see
   `fixed_neighbors` below).

7. Tested on the full maze and the easy maze; additionally tested with an
   artificial maze where the open corridor touches the bottom-right
   corner, which crashes the buggy version with an IndexError and is
   solved cleanly by the fixed version.
"""

import debugging_lab as lab


def fixed_neighbors(self, position):
    row, col = position
    for direction, (dr, dc) in enumerate(lab.DIRECTIONS):
        next_row = row + dr
        next_col = col + dc
        if 0 <= next_row < self.rows and 0 <= next_col < self.cols:
            if self.is_open(next_row, next_col):
                yield (next_row, next_col), direction


def run(maze_factory, label):
    print(f"\n--- {label} (buggy) ---")
    lab.activate_case(2)
    solver = lab.MazeSolver(maze_factory())
    solver.solve()

    print(f"\n--- {label} (fixed) ---")
    lab.MazeSolver.neighbors = fixed_neighbors
    solver = lab.MazeSolver(maze_factory())
    solver.solve()


def demonstrate_latent_bug():
    """Show directly that the buggy neighbors() walks off the grid when
    asked about the bottom-right corner cell, even though this never
    happens to occur during the BFS on the provided mazes."""
    print("\n--- Direct demonstration of the latent out-of-bounds bug ---")
    lab.activate_case(2)
    solver = lab.MazeSolver(lab.create_easy_maze())
    corner = (solver.rows - 1, solver.cols - 1)
    try:
        list(solver.neighbors(corner))
        print(f"neighbors({corner}) returned without error (unexpected)")
    except IndexError as exc:
        print(f"neighbors({corner}) crashed as predicted: {exc}")

    lab.MazeSolver.neighbors = fixed_neighbors
    solver = lab.MazeSolver(lab.create_easy_maze())
    result = list(solver.neighbors(corner))
    print(f"Fixed neighbors({corner}) = {result} (no crash)")


if __name__ == "__main__":
    run(lab.create_maze, "Full maze")
    run(lab.create_easy_maze, "Easy maze")
    demonstrate_latent_bug()
