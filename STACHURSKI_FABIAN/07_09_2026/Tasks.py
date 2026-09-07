from abc import ABC, abstract method
from datetime import datetime

# a)

class Task(ABC):
  def__init__(self, title):
    self.title = title
    self.created_at = datetime.now()
    self._done = False

  @property
  def done(self):
    return self._done
  def complete(self):
    self._done = True
@abstractmethod
  def estimate_minutes(self):
    pass

#b)

class SimpleTask(Task):
  def __init__(self, title, minutes):
    super().__init__(title)
    self.minutes = minutes

  def estimate_minutes(self):
    return self.minutes


class TimedTask(Task):
  def __init__(self, title, minutes):
    super().__init__(title)
    self.minutes = minutes

  def estimate_minutes(self):
    return self.minutes

class RecurringTask(TimedTask):
  def __init__(self, title, minutes, times_per_week):
    super().__init__(title, minutes)
    self.times_per_week = times_per_week

  def estimate_minutes(self):
    return self.minutes * self.times_per_week

 
