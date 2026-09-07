from abc import ABC, abstractmethod

class Tasks(ABC):
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

class SimpleTask(Tasks):
    def __init__(self, title, created_at, estimated_minutes):
        super().__init__(title, created_at)
        self.estimated_minutes = estimated_minutes

    def estimate_minutes(self):
        return self.estimated_minutes

class TimedTask(Tasks):
    def __init__(self, title, created_at, estimated_minutes, start_time, end_time):
        super().__init__(title, created_at)
        self.estimated_minutes = estimated_minutes
        self.start_time = start_time
        self.end_time = end_time

    def estimate_minutes(self):
        return self.estimated_minutes

class RecurringTask(Tasks):
    def __init__(self, title, created_at, estimated_minutes, recurrence_interval):
        super().__init__(title, created_at)
        self.estimated_minutes = estimated_minutes
        self.recurrence_interval = recurrence_interval

    def estimate_minutes(self):
        return self.estimated_minutes

class TaskList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        if not isinstance(task, Tasks):
            raise ValueError("Only instances of Tasks or its subclasses can be added.")                
        self.tasks.append(task)

    def total_estimate(self):
        return sum(task.estimate_minutes() for task in self.tasks)

    def pending_tasks(self):
        return [task for task in self.tasks if not task.done]

    def completed_tasks(self):
        return [task for task in self.tasks if task.done]

    def __len__(self):
        return len(self.tasks)

    def __str__(self):
        return "\n".join(
            f"{task.title} - {'Done' if task.done else 'Pending'} - Estimated Minutes: {task.estimate_minutes()}"
            for task in self.tasks
        )

tasks = TaskList()

tasks.add_task(SimpleTask("Write report", "2024-06-01", 120))
tasks.add_task(TimedTask("Team meeting", "2024-06-02", 60, "2024-06-02 10:00", "2024-06-02 11:00"))
tasks.add_task(RecurringTask("Daily standup", "2024-06-01", 15, "daily"))

print(len(tasks))
print(tasks.total_estimate())

tasks.tasks[0].complete()

print("pending tasks:", tasks.pending_tasks())
print("completed tasks:", tasks.completed_tasks())

print(tasks)
