import importlib
from .base.database import Database

def create_database(database_type: str, db_url: str) -> Database:
    module_name = f"implementations.{database_type}_database"
    class_name = f"{database_type.capitalize()}Database"
    
    try:
        module = importlib.import_module(module_name)
        database_class = getattr(module, class_name)
        return database_class(db_url)
    except (ImportError, AttributeError) as e:
        raise ValueError(f"Unsupported database type: {database_type}") from e
