from abc import ABC, abstractmethod
from datetime import datetime

class Task(ABC):
    def __init__(self, title: str):
        self._done = False
        self.title = title
        self.created_at = datetime.now()

    @abstractmethod
    def estimate_minutes(self) -> int:
        pass

    def complete(self):
        self._done = True

    @property
    def done(self) -> bool:
        return self._done


class SimpleTask(Task):
    def __init__(self, title: str, minutes: int = 15):
        super().__init__(title)
        self.minutes = minutes

    def estimate_minutes(self) -> int:
        return self.minutes


class TimedTask(Task):
    def __init__(self, title: str, minutes: int = 15):
        super().__init__(title)
        self.minutes = minutes

    def estimate_minutes(self) -> int:
        return self.minutes


class RecurringTask(TimedTask):
    def __init__(self, title: str, minutes: int, times_per_week: int):
        super().__init__(title, minutes)
        self.times_per_week = times_per_week

    def estimate_minutes(self) -> int:
        return self.minutes * self.times_per_week


class TaskList:
    def __init__(self):
        self._tasks = []

    def add(self, task: Task):
        if not isinstance(task, Task):
            raise TypeError("Only instances of Task can be added to the TaskList.")
        self._tasks.append(task)

    def total_estimate(self) -> int:
        return sum(task.estimate_minutes() for task in self._tasks)

    def pending(self) -> list:
        return [task for task in self._tasks if not task.done]

    def completed(self) -> list:
        return [task for task in self._tasks if task.done]

    def __len__(self) -> int:
        return len(self._tasks)

    def __str__(self) -> str:
        return f"TaskList(total_tasks={len(self)}, pending={len(self.pending())}, completed={len(self.completed())}, total_estimate={self.total_estimate()} mins)"


if __name__ == "__main__":
    my_tasks = TaskList()

    task1 = SimpleTask("Water the plants", 5)
    task2 = TimedTask("Team sync meeting", 45)
    task3 = RecurringTask("Weekly code review", 60, 2)

    my_tasks.add(task1)
    my_tasks.add(task2)
    my_tasks.add(task3)


    task1.complete()

    print("--- Task List Summary ---")
    print(my_tasks)
    print(f"Total Estimated Time: {my_tasks.total_estimate()} minutes")
    
    print("\nPending Tasks:")
    for t in my_tasks.pending():
        print(f"- {t.title} ({t.estimate_minutes()} mins)")

    print("\nCompleted Tasks:")
    for t in my_tasks.completed():
        print(f"- {t.title} ({t.estimate_minutes()} mins)")