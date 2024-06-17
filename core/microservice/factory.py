import importlib
from .base.microservice import Microservice

def create_microservice(service_type: str) -> Microservice:
    module_name = f"implementations.{service_type}_service"
    class_name = f"{service_type.capitalize()}Service"
    
    try:
        module = importlib.import_module(module_name)
        service_class = getattr(module, class_name)
        return service_class()
    except (ImportError, AttributeError) as e:
        raise ValueError(f"Unsupported service type: {service_type}") from e
