import sys
from collections import deque

WALL = "#"
OPEN = "."
START = "S"
CHEESE = "C"

DIRECTIONS = [
    (-1, 0),  # UP
    (0, 1),   # RIGHT
    (1, 0),   # DOWN
    (0, -1),  # LEFT
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

            # Bug 2 & Bug 4 Fix: Proper boundary check & correct row/col deltas
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

            # Bug 3 Fix: Pop head element instead of peeking
            current = self.queue.popleft()
            self.move_count += 1

            if trace:
                self.print_state("search", current)

            # Bug 1 Fix: Correct goal target
            if current == self.goal:
                path = self.reconstruct_path()
                print("\nStatus: SOLVED")
                print(f"Moves: {len(path) - 1}")
                print(f"Search steps: {self.move_count}")
                print(f"Path: {path}")
                return True

            for next_position, direction in self.neighbors(current):
                # Bug 5 Fix: Membership check against visited set (self.previous)
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


def create_corridor_maze():
    return [
        list("#####"),
        list("#S.C#"),
        list("#####"),
    ]


def run_tests():
    print("=" * 60)
    print("RUNNING ADDITIONAL TEST INPUTS")
    print("=" * 60)

    print("\n--- Additional Input 1: Easy Maze ---")
    easy_solver = MazeSolver(create_easy_maze())
    assert easy_solver.solve() is True, "Test 1 Failed"

    print("\n--- Additional Input 2: Corridor Maze ---")
    corridor_solver = MazeSolver(create_corridor_maze())
    assert corridor_solver.solve() is True, "Test 2 Failed"

    print("\nAll additional tests passed successfully!")


def main():
    trace = "--trace" in sys.argv
    args = [arg for arg in sys.argv[1:] if arg != "--trace"]

    case_number = int(args[0]) if args else 1

    print("=" * 60)
    print("DEBUGGING LAB (CORRECTED)")
    print(f"Running Case {case_number}")
    print("=" * 60)

    solver = MazeSolver(create_maze())
    solver.print_maze()
    solver.solve(trace=trace)

    run_tests()


if __name__ == "__main__":
    main()