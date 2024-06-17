# your_package/core/cache/base/cache.py

from abc import ABC, abstractmethod

class Cache(ABC):
    
    @abstractmethod
    def get_client(self):
        pass
