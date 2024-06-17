# your_package/core/logging/base/logger.py

from abc import ABC, abstractmethod

class Logger(ABC):
    
    @abstractmethod
    def setup(self):
        pass
