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
