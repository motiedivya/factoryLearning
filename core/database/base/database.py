# your_package/core/database/base/database.py

from abc import ABC, abstractmethod

class Database(ABC):
    
    @abstractmethod
    def get_session(self):
        pass
