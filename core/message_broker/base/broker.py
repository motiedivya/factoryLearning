# your_package/core/message_broker/base/broker.py

from abc import ABC, abstractmethod
from typing import Callable

class MessageBroker(ABC):
    
    @abstractmethod
    def publish(self, topic: str, message: str):
        pass

    @abstractmethod
    def subscribe(self, topic: str, handler: Callable[[str], None]):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
