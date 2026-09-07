# a)
from abc import ABC, abstractmethod
from datetime import datetime


class Task(ABC):
    def __init__(self, title, created_at=None):
        self.title = title

        self._done = False

    @abstractmethod
    def estimate_minutes(self):
        pass

    def complete(self):
        self._done = True

    @property
    def done(self):
        return self._done
