"""
tasks.py

A small task-management module demonstrating abstraction with the `abc`
module: an abstract base class `Task`, three concrete subclasses, and a
`TaskList` container that works with any Task polymorphically.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime


class Task(ABC):
    """Abstract base class for all kinds of tasks."""

    def __init__(self, title: str):
        self.title = title
        self.created_at = datetime.now()
        self._done = False

    @abstractmethod
    def estimate_minutes(self) -> float:
        """Return how many minutes this task is estimated to take."""
        raise NotImplementedError

    def complete(self) -> None:
        """Mark the task as done."""
        self._done = True

    @property
    def done(self) -> bool:
        """Read-only flag: has this task been completed?"""
        return self._done

    def __str__(self) -> str:
        status = "done" if self._done else "pending"
        return f"[{status}] {self.title} (~{self.estimate_minutes():.0f} min)"


class SimpleTask(Task):
    """A task with a fixed, one-off time estimate."""

    def __init__(self, title: str, minutes: float):
        super().__init__(title)
        self.minutes = minutes

    def estimate_minutes(self) -> float:
        return self.minutes


class TimedTask(Task):
    """A task that takes a known number of minutes each time it's done."""

    def __init__(self, title: str, minutes_per_session: float):
        super().__init__(title)
        self.minutes_per_session = minutes_per_session

    def estimate_minutes(self) -> float:
        return self.minutes_per_session


class RecurringTask(TimedTask):
    """A TimedTask that repeats a number of times per week.

    The estimate is the per-session estimate multiplied by how many times
    per week the task recurs.
    """

    def __init__(self, title: str, minutes_per_session: float, times_per_week: int):
        super().__init__(title, minutes_per_session)
        self.times_per_week = times_per_week

    def estimate_minutes(self) -> float:
        return super().estimate_minutes() * self.times_per_week


class TaskList:
    """A collection of Task objects."""

    def __init__(self):
        self._tasks: list[Task] = []

    def add(self, task: Task) -> None:
        if not isinstance(task, Task):
            raise TypeError(f"Expected a Task instance, got {type(task).__name__}")
        self._tasks.append(task)

    def total_estimate(self) -> float:
        """Sum the time estimate over all tasks, polymorphically."""
        return sum(task.estimate_minutes() for task in self._tasks)

    def pending(self) -> list[Task]:
        return [task for task in self._tasks if not task.done]

    def completed(self) -> list[Task]:
        return [task for task in self._tasks if task.done]

    def __len__(self) -> int:
        return len(self._tasks)

    def __str__(self) -> str:
        lines = [f"TaskList ({len(self)} tasks, {self.total_estimate():.0f} min total)"]
        lines += [f"  - {task}" for task in self._tasks]
        return "\n".join(lines)


if __name__ == "__main__":
    tasks = TaskList()

    tasks.add(SimpleTask("Buy groceries", 30))
    tasks.add(TimedTask("Write lab report", 90))
    tasks.add(RecurringTask("Gym workout", 60, times_per_week=3))
    tasks.add(RecurringTask("Language practice", 20, times_per_week=5))

    tasks.add(SimpleTask("Read a chapter", 45))

    # Complete a couple of tasks.
    pending_before = tasks.pending()
    pending_before[0].complete()
    pending_before[2].complete()

    print(tasks)
    print()
    print(f"Pending:   {len(tasks.pending())}")
    print(f"Completed: {len(tasks.completed())}")
    print(f"Total weekly estimate: {tasks.total_estimate():.0f} minutes")

    try:
        tasks.add("not a task")
    except TypeError as exc:
        print(f"\nRejected non-Task value as expected: {exc}")
