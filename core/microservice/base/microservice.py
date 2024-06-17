# your_package/core/microservice/base/service.py

from abc import ABC, abstractmethod
from fastapi import FastAPI

class Microservice(ABC):
    
    @abstractmethod
    def create_app(self) -> FastAPI:
        pass
