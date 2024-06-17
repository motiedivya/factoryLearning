import importlib
from .base.gateway import ApiGateway

def create_api_gateway(gateway_type: str, admin_url: str) -> ApiGateway:
    module_name = f"implementations.{gateway_type}_gateway"
    class_name = f"{gateway_type.capitalize()}Gateway"
    
    try:
        module = importlib.import_module(module_name)
        gateway_class = getattr(module, class_name)
        return gateway_class(admin_url)
    except (ImportError, AttributeError) as e:
        raise ValueError(f"Unsupported gateway type: {gateway_type}") from e
