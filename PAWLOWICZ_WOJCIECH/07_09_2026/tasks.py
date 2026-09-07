from abc import ABC, abstractmethod

class Task(ABC):
    def __init__(self, title, created_at):
        self._done = False
        self.title = title
        self.created_at = created_at

    @abstractmethod
    def estimate_minutes(self):
        pass

    def complete(self):
        self._done = True

    @property
    def done(self):
        return self._done


class SimpleTask(Task):
    def estimate_minutes(self):
        return 0


class TimedTask(Task):
    def __init__(self, title, minutes, created_at):
        super().__init__(title, created_at)
        self.minutes = minutes

    def estimate_minutes(self):
        return self.minutes


class RecurringTask(TimedTask):
    def __init__(self, title, minutes, times_per_week, created_at=None):
        super().__init__(title, minutes, created_at)
        self.times_per_week = times_per_week

    def estimate_minutes(self):
        return self.minutes * self.times_per_week


class TaskList:
    def __init__(self):
        self.tasks = []

    def add(self, task):
        if not isinstance(task, Task):
            raise TypeError("Only Task objects can be added.")
        self.tasks.append(task)

    def total_estimate(self):
        total = 0
        for task in self.tasks:
            total += task.estimate_minutes()
        return total

    def pending(self):
        return [task for task in self.tasks if not task.done]

    def completed(self):
        return [task for task in self.tasks if task.done]

    def __len__(self):
        return len(self.tasks)

    def __str__(self):
        lines = []
        for task in self.tasks:
            status = "Done" if task.done else "Pending"
            lines.append(
                f"{task.title} - {status} - "
                f"{task.estimate_minutes()} minutes"
            )
        return "\n".join(lines)

if __name__ == "__main__":
    task_list = TaskList()

    task1 = SimpleTask("Buy groceries", "2026-09-07")
    task2 = TimedTask("Study Python", 60, "2026-09-07")
    task3 = TimedTask("Clean room", 30, "2026-09-07")
    task4 = RecurringTask("Exercise", 45, 3, "2026-09-07")

    task2.complete()

    task_list.add(task1)
    task_list.add(task2)
    task_list.add(task3)
    task_list.add(task4)

    print("Task Summary")
    print("------------")
    print(task_list)
    print()
    print("Number of tasks:", len(task_list))
    print("Total estimated minutes:", task_list.total_estimate())
    print("Pending tasks:", len(task_list.pending()))
    print("Completed tasks:", len(task_list.completed()))
