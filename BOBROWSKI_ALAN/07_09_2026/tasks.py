from abc import ABC, abstractmethod


class Task(ABC):
    def __init__(self, title, created_at=None) -> None:
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
    def __init__(self, title, minutes, created_at=None) -> None:
        super().__init__(title, created_at)
        self.minutes = minutes

    def estimate_minutes(self):
        return self.minutes


class TimedTask(Task):
    def __init__(self, title, minutes, created_at=None) -> None:
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
        result = []

        for task in self.tasks:
            if not task.done:
                result.append(task)

        return result

    def completed(self):
        result = []

        for task in self.tasks:
            if task.done:
                result.append(task)

        return result

    def __len__(self):
        return len(self.tasks)

    def __str__(self):
        if not self.tasks:
            return "TaskList: empty"

        result = "TaskList:\n"

        for task in self.tasks:
            if task.done:
                status = "done"
            else:
                status = "pending"

            result += f"- {task.title} ({task.estimate_minutes()} min) [{status}]\n"

        return result



task_list = TaskList()


task1 = SimpleTask("Read book", 30)
task2 = TimedTask("Write code", 60)
task3 = RecurringTask("Exercise", 45, 3)
task4 = RecurringTask("Study Python", 30, 5)


task1.complete()
task3.complete()


task_list.add(task1)
task_list.add(task2)
task_list.add(task3)
task_list.add(task4)


print(task_list)
print("Number of tasks:", len(task_list))
print("Total estimate:", task_list.total_estimate(), "minutes")
print("Pending:", len(task_list.pending()))
print("Completed:", len(task_list.completed()))
