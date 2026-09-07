#a)
from abc import ABC, abstractmethod

class Task(ABC):
    def __init__(self, title):
        self.title = title
        self.created_at = None
        self.done = False

    @abstracmethod
    def estimate_minutes(self):
        pass
    def complete(self):
        self._done = True
    @property
    def done(self):
        return self._done
#b)
class SimpleTask(Task):
    def __init__(self, title, minutes):
        super().__init__(title)
        self.minutes = minutes
    def estimate_minutes(Self):
        return self.minutes
class TimedTask(Task):
    def __init__(self,title,minutes):
        super().__init__(title)
        self.minutes = minutes
    def estimate_minutes(self)
        return self.minutes
class RecurringTask(TimedTask):
    def __init__(Self, title, minutes, times_per_week):
        super().__init__(title,minutes)
        self.times_per_week = times_per_week
    def estimate_minutes(Self):
        return self.minutes * self.times_per_week


t1 = SimpleTask("Nauka", 30)
t2 = TimedTask("Trening", 60)
t3 = RecurringTask("Python", 20, 3)

t1.complete()

lista = TaskList()

lista.add(1)
lista.add(2)
lista.add(3)

