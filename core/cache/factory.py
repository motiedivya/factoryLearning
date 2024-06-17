import importlib
from .base.cache import Cache

def create_cache(cache_type: str, cache_url: str) -> Cache:
    module_name = f"implementations.{cache_type}_cache"
    class_name = f"{cache_type.capitalize()}Cache"
    
    try:
        module = importlib.import_module(module_name)
        cache_class = getattr(module, class_name)
        return cache_class(cache_url)
    except (ImportError, AttributeError) as e:
        raise ValueError(f"Unsupported cache type: {cache_type}") from e
