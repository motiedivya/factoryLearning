import importlib
from .base.broker import MessageBroker

def create_message_broker(broker_type: str, broker_url: str) -> MessageBroker:
    module_name = f"implementations.{broker_type}_broker"
    class_name = f"{broker_type.capitalize()}Broker"
    
    try:
        module = importlib.import_module(module_name)
        broker_class = getattr(module, class_name)
        return broker_class(broker_url)
    except (ImportError, AttributeError) as e:
        raise ValueError(f"Unsupported broker type: {broker_type}") from e
