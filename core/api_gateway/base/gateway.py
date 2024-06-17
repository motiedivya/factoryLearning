# your_package/core/api_gateway/base/gateway.py

from abc import ABC, abstractmethod

class ApiGateway(ABC):
    
    @abstractmethod
    def add_service(self, name: str, url: str):
        pass

    @abstractmethod
    def add_route(self, service_name: str, paths: list):
        pass
