# your_package/core/security/base/security.py

from abc import ABC, abstractmethod

class Security(ABC):
    
    @abstractmethod
    def start(self):
        pass
