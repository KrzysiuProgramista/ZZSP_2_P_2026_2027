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
