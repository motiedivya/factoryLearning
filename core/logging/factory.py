import importlib
from .base.logger import Logger

def create_logger(logger_type: str, host: str, port: int) -> Logger:
    module_name = f"implementations.{logger_type}_logger"
    class_name = f"{logger_type.capitalize()}Logger"
    
    try:
        module = importlib.import_module(module_name)
        logger_class = getattr(module, class_name)
        return logger_class(host, port)
    except (ImportError, AttributeError) as e:
        raise ValueError(f"Unsupported logger type: {logger_type}") from e
