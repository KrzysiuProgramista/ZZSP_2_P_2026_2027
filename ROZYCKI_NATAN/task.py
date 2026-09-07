from abc import abstractmethod

class Task():
    def init__(self, created_at, title):
        self.created_at = created_at
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