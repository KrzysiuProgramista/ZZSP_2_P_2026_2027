"""
DEBUGGING LAB
==============

Programming Principles – Chapter 19: Debugging

Student instructions
--------------------
This program searches for a path from S (start) to C (cheese) in a grid.
Five deliberately introduced bugs are included.

Run one case at a time:

    python debugging_lab.py 1
    python debugging_lab.py 2
    python debugging_lab.py 3
    python debugging_lab.py 4
    python debugging_lab.py 5

Optional diagnostic mode:

    python debugging_lab.py <case> --trace

For every case:

1. Run the program and describe the observed effect.
2. Form a hypothesis about the cause.
3. Add suitable diagnostic output or use a debugger.
4. Record the relevant part of the execution trace.
5. Identify the actual cause of the problem.
6. Fix the program.
7. Test the corrected program with at least two additional inputs.

Rules:
- Do not rewrite the whole program.
- Do not remove the search algorithm.
- Do not guess-and-check randomly.
- Keep a short debugging log describing your reasoning.
- The location where the program fails may not be the location containing
  the actual defect.

Expected correct result for every case:

    Status: SOLVED

The exercise is based on the debugging principles discussed in Chapter 19
of Tim Teitelbaum's "Principled Programming": observed effects, diagnostic
output, execution traces, error messages, and reasoning from symptoms to
causes.
"""

import sys
from collections import deque

WALL = "#"
OPEN = "."
START = "S"
CHEESE = "C"

DIRECTIONS = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]

DIRECTION_NAMES = ["UP", "RIGHT", "DOWN", "LEFT"]


class MazeSolver:
    def __init__(self, grid):
        self.grid = [row[:] for row in grid]
        self.rows = len(grid)
        self.cols = len(grid[0])

        self.start = self.find(START)
        self.goal = self.find(CHEESE)

        self.queue = deque([self.start])
        self.previous = {self.start: None}
        self.move_count = 0

    def find(self, symbol):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == symbol:
                    return (r, c)
        raise ValueError(f"Symbol {symbol!r} not found in maze.")

    def print_maze(self):
        print("\nMaze:")
        for row in self.grid:
            print(" ".join(row))

    def print_state(self, message, position=None):
        if position is None:
            position = self.start
        r, c = position
        print(
            f"{message}: position=({r},{c}), "
            f"queue_size={len(self.queue)}, visited={len(self.previous)}"
        )

    def is_open(self, row, col):
        return self.grid[row][col] != WALL

    def neighbors(self, position):
        row, col = position

        for direction, (dr, dc) in enumerate(DIRECTIONS):
            next_row = row + dr
            next_col = col + dc

            if 0 <= next_row < self.rows and 0 <= next_col < self.cols:
                if self.is_open(next_row, next_col):
                    yield (next_row, next_col), direction

    def reconstruct_path(self):
        if self.goal not in self.previous:
            return []

        path = []
        current = self.goal

        while current is not None:
            path.append(current)
            current = self.previous[current]

        path.reverse()
        return path

    def solve(self, trace=False, max_steps=10000):
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
                if next_position not in self.previous:
                    self.previous[next_position] = current
                    self.queue.append(next_position)

        print("\nStatus: NOT SOLVED")
        print("Reason: the search exhausted all reachable cells.")
        return False


def create_maze():
    return [
        list("###########"),
        list("#S...#....#"),
        list("###.#.###.#"),
        list("#...#.....#"),
        list("#.#####.###"),
        list("#.....#...#"),
        list("#.###.###.#"),
        list("#...#.....#"),
        list("###.#####.#"),
        list("#.........#"),
        list("#########C#"),
    ]


def create_easy_maze():
    return [
        list("#######"),
        list("#S....#"),
        list("#####.#"),
        list("#....C#"),
        list("#######"),
    ]

def activate_case(case_number):
    """Activate one deliberately faulty version of the program."""

    if case_number == 1:
        def faulty_solve(self, trace=False, max_steps=10000):
            while self.queue:
                if self.move_count >= max_steps:
                    print("\nStatus: STOPPED")
                    print("Reason: maximum number of search steps exceeded.")
                    return False

                current = self.queue.popleft()
                self.move_count += 1

                if trace:
                    self.print_state("search", current)

                # The target comparison is subtly wrong.
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

        MazeSolver.solve = faulty_solve

    elif case_number == 2:
        def faulty_neighbors(self, position):
            row, col = position

            for direction, (dr, dc) in enumerate(DIRECTIONS):
                next_row = row + dr
                next_col = col + dc

                if next_row >= 0 and next_col >= 0:
                    if self.is_open(next_row, next_col):
                        yield (next_row, next_col), direction

        MazeSolver.neighbors = faulty_neighbors

    elif case_number == 3:
        def faulty_solve(self, trace=False, max_steps=10000):
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
                    if next_position not in self.previous:
                        self.previous[next_position] = current
                        self.queue.append(next_position)

            print("\nStatus: NOT SOLVED")
            print("Reason: the search exhausted all reachable cells.")
            return False

        MazeSolver.solve = faulty_solve

    elif case_number == 4:
        def faulty_neighbors(self, position):
            row, col = position

            for direction, (dr, dc) in enumerate(DIRECTIONS):
                next_row = row + dr
                next_col = col + dc

                if 0 <= next_row < self.rows and 0 <= next_col < self.cols:
                    # One coordinate is updated using the wrong direction.
                    next_row = row + dr
                    if self.is_open(next_row, next_col):
                        yield (next_row, next_col), direction

        MazeSolver.neighbors = faulty_neighbors

    elif case_number == 5:
        def faulty_solve(self, trace=False, max_steps=10000):
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
                    # The membership test uses the wrong collection.
                    if next_position not in self.previous:
                        self.previous[next_position] = current
                        self.queue.append(next_position)

            print("\nStatus: NOT SOLVED")
            print("Reason: the search exhausted all reachable cells.")
            return False

        MazeSolver.solve = faulty_solve

    else:
        raise ValueError("Case number must be between 1 and 5.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python debugging_lab.py <case> [--trace]")
        print("Case must be a number from 1 to 5.")
        sys.exit(1)

    try:
        case_number = int(sys.argv[1])
    except ValueError:
        print("Case must be an integer from 1 to 5.")
        sys.exit(1)

    if case_number not in range(1, 6):
        print("Case must be a number from 1 to 5.")
        sys.exit(1)

    activate_case(case_number)

    print("=" * 60)
    print("DEBUGGING LAB")
    print(f"Case {case_number}")
    print("=" * 60)

    solver = MazeSolver(create_maze())
    solver.print_maze()

    trace = "--trace" in sys.argv

    try:
        solver.solve(trace=trace)
    except Exception as exc:
        print("\nStatus: CRASHED")
        print(f"Exception: {type(exc).__name__}: {exc}")
        raise


if __name__ == "__main__":
    main()
