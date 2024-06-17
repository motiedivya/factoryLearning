import importlib
from .base.security import Security

def create_security(security_type: str, port: int) -> Security:
    module_name = f"implementations.{security_type}_security"
    class_name = f"{security_type.capitalize()}Security"
    
    try:
        module = importlib.import_module(module_name)
        security_class = getattr(module, class_name)
        return security_class(port)
    except (ImportError, AttributeError) as e:
        raise ValueError(f"Unsupported security type: {security_type}") from e
