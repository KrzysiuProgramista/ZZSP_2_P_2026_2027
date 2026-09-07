from abc import ABC, abstractmethod

class Task(ABC):
    def __init__(self, title: str, created_at: str):
        self.title = title
        self.created_at = created_at
        self._done = False

    @abstractmethod
    def estimate_minutes(self) -> int:
        pass

    def complete(self):
        self._done = True

    @property
    def done(self) -> bool:
        return self._done



class SimpleTask(Task):
    def __init__(self, title: str, created_at: str, estimated_minutes: int):
        super().__init__(title, created_at)
        self._estimated_minutes = estimated_minutes

    def estimate_minutes(self) -> int:
        return self._estimated_minutes


class TimedTask(Task):
    def __init__(self, title: str, created_at: str, estimated_minutes: int, due_date: str):
        super().__init__(title, created_at)
        self._estimated_minutes = estimated_minutes
        self.due_date = due_date

    def estimate_minutes(self) -> int:
        return self._estimated_minutes


class RecurringTask(TimedTask):
    def __init__(self, title: str, created_at: str, estimated_minutes: int, due_date: str, times_per_week: int):

        super().__init__(title, created_at, estimated_minutes, due_date)
        self.times_per_week = times_per_week

    def estimate_minutes(self) -> int:
        return super().estimate_minutes() * self.times_per_week



class TaskList:
    def __init__(self):
        self._tasks = []

    def add(self, task: Task):

        if not isinstance(task, Task):
            raise TypeError("Only instances of Task (or its subclasses) can be added.")
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
        lines = [f"Task List Summary ({len(self)} tasks total, {self.total_estimate()} mins estimated):"]
        for task in self._tasks:
            status = "Completed" if task.done else "Pending"
            lines.append(f" - [{status}] {task.title} ({task.estimate_minutes()} mins)")
        return "\n".join(lines)



if __name__ == "__main__":

    my_tasks = TaskList()

    task1 = SimpleTask("Read Python docs", "2026-09-01", 15)
    task2 = TimedTask("Submit assignment", "2026-09-02", 45, "2026-09-05")
    task3 = RecurringTask("Gym workout", "2026-09-01", 60, "2026-09-30", 3)


    my_tasks.add(task1)
    my_tasks.add(task2)
    my_tasks.add(task3)


    task1.complete()

    print(my_tasks)
    print("\n--- Detailed Breakdown ---")
    print(f"Total tasks: {len(my_tasks)}")
    print(f"Pending Tasks: {[t.title for t in my_tasks.pending()]}")
    print(f"Completed Tasks: {[t.title for t in my_tasks.completed()]}")
    print(f"Total time required: {my_tasks.total_estimate()} minutes")
    
    try:
        my_tasks.add("Not a task object")
    except TypeError as e:
        print(f"\nType validation working successfully: {e}")