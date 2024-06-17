Yes, you can use an INI file at the application level to manage configuration settings. INI files are simple and easy to read, making them a good choice for configuration. You can use Python's built-in `configparser` module to read from INI files.

Here’s how you can set up your application to use an INI file for configuration while keeping your reusable package focused on abstractions.

### Directory Structure

```
your_project/
├── config/
│   ├── settings.ini
├── implementations/
│   ├── nsq_broker.py
│   ├── kong_gateway.py
│   ├── graylog_logger.py
│   ├── prometheus_security.py
│   ├── fastapi_service.py
│   ├── mysql_database.py
│   ├── redis_cache.py
├── app.py
├── requirements.txt
├── setup.py
└── your_package/
    ├── core/
    │   ├── __init__.py
    │   ├── message_broker/
    │   │   ├── __init__.py
    │   │   ├── base/
    │   │   │   ├── __init__.py
    │   │   │   ├── broker.py
    │   │   ├── factory.py
    │   ├── api_gateway/
    │   │   ├── __init__.py
    │   │   ├── base/
    │   │   │   ├── __init__.py
    │   │   │   ├── gateway.py
    │   │   ├── factory.py
    │   ├── logging/
    │   │   ├── __init__.py
    │   │   ├── base/
    │   │   │   ├── __init__.py
    │   │   │   ├── logger.py
    │   │   ├── factory.py
    │   ├── security/
    │   │   ├── __init__.py
    │   │   ├── base/
    │   │   │   ├── __init__.py
    │   │   │   ├── security.py
    │   │   ├── factory.py
    │   ├── microservice/
    │   │   ├── __init__.py
    │   │   ├── base/
    │   │   │   ├── __init__.py
    │   │   │   ├── service.py
    │   │   ├── factory.py
    │   ├── database/
    │   │   ├── __init__.py
    │   │   ├── base/
    │   │   │   ├── __init__.py
    │   │   │   ├── database.py
    │   │   ├── factory.py
    │   ├── cache/
    │   │   ├── __init__.py
    │   │   ├── base/
    │   │   │   ├── __init__.py
    │   │   │   ├── cache.py
    │   │   ├── factory.py
    ├── README.md
    └── requirements.txt
```

### Example INI File

#### `config/settings.ini`
```ini
[DEFAULT]
BrokerType = nsq
BrokerURL = localhost:4150
DatabaseURL = mysql+pymysql://user:password@localhost/dbname
RedisURL = redis://localhost
GraylogHost = localhost
GraylogPort = 12201
PrometheusPort = 8000
KongAdminURL = http://localhost:8001
```

### Example Implementation Files

#### `implementations/nsq_broker.py`
This file would contain the concrete implementation for NSQ.
```python
# your_project/implementations/nsq_broker.py

import nsq
from your_package.core.message_broker.base.broker import MessageBroker
from typing import Callable

class NsqBroker(MessageBroker):
    
    def __init__(self, nsq_url: str):
        self.nsq_url = nsq_url
        self.writer = nsq.Writer([nsq_url])
        self.reader = None
        self.handlers = {}

    def publish(self, topic: str, message: str):
        self.writer.pub(topic, message.encode('utf-8'), self._pub_callback)

    def subscribe(self, topic: str, handler: Callable[[str], None]):
        if topic not in self.handlers:
            self.handlers[topic] = []
        self.handlers[topic].append(handler)

    def _message_handler(self, message):
        topic = message.get_topic()
        for handler in self.handlers.get(topic, []):
            handler(message.body.decode('utf-8'))

    def _pub_callback(self, conn, data):
        if isinstance(data, Exception):
            print(f"Publish failed: {data}")
        else:
            print("Message published successfully")

    def start(self):
        for topic in self.handlers:
            self.reader = nsq.Reader(
                topic=topic, 
                channel="default", 
                nsqd_tcp_addresses=[self.nsq_url],
                message_handler=self._message_handler,
            )
        nsq.run()

    def stop(self):
        if self.reader:
            self.reader.close()
```

#### `implementations/kong_gateway.py`
This file would contain the concrete implementation for Kong API Gateway.
```python
# your_project/implementations/kong_gateway.py

import requests
from your_package.core.api_gateway.base.gateway import ApiGateway

class KongGateway(ApiGateway):
    def __init__(self, admin_url: str):
        self.admin_url = admin_url

    def add_service(self, name: str, url: str):
        response = requests.post(f"{self.admin_url}/services", json={"name": name, "url": url})
        response.raise_for_status()
        return response.json()

    def add_route(self, service_name: str, paths: list):
        response = requests.post(f"{self.admin_url}/services/{service_name}/routes", json={"paths": paths})
        response.raise_for_status()
        return response.json()
```

#### `implementations/graylog_logger.py`
This file would contain the concrete implementation for Graylog.
```python
# your_project/implementations/graylog_logger.py

import logging
import graypy
from your_package.core.logging.base.logger import Logger

class GraylogLogger(Logger):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def setup(self):
        logger = logging.getLogger()
        handler = graypy.GELFHandler(self.host, self.port)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
```

#### `implementations/prometheus_security.py`
This file would contain the concrete implementation for Prometheus.
```python
# your_project/implementations/prometheus_security.py

from prometheus_client import start_http_server
from your_package.core.security.base.security import Security

class PrometheusSecurity(Security):
    def __init__(self, port: int):
        self.port = port

    def start(self):
        start_http_server(self.port)
```

#### `implementations/fastapi_service.py`
This file would contain the concrete implementation for FastAPI.
```python
# your_project/implementations/fastapi_service.py

from fastapi import FastAPI
from your_package.core.microservice.base.service import Microservice

class FastapiService(Microservice):
    def __init__(self):
        self.app = FastAPI()

    def create_app(self) -> FastAPI:
        return self.app
```

#### `implementations/mysql_database.py`
This file would contain the concrete implementation for MySQL.
```python
# your_project/implementations/mysql_database.py

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from your_package.core.database.base.database import Database

class MysqlDatabase(Database):
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.engine = sqlalchemy.create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()
```

#### `implementations/redis_cache.py`
This file would contain the concrete implementation for Redis.
```python
# your_project/implementations/redis_cache.py

import redis
from your_package.core.cache.base.cache import Cache

class RedisCache(Cache):
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.client = redis.StrictRedis.from_url(redis_url)

    def get_client(self):
        return self.client
```

### Package Files

#### `your_package/core/message_broker/base/broker.py`
Defines the abstract factory interface and abstract product interfaces.
```python
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
```

#### `your_package/core/message_broker/factory.py`
Implements the factory method for creating instances of the message broker.
```python
# your_package/core/message_broker/factory.py

import importlib
from .base.broker import MessageBroker

def create_message_broker(broker_type:

 str, broker_url: str) -> MessageBroker:
    module_name = f"implementations.{broker_type}_broker"
    class_name = f"{broker_type.capitalize()}Broker"
    
    try:
        module = importlib.import_module(module_name)
        broker_class = getattr(module, class_name)
        return broker_class(broker_url)
    except (ImportError, AttributeError) as e:
        raise ValueError(f"Unsupported broker type: {broker_type}") from e
```

#### `your_package/core/api_gateway/base/gateway.py`
Defines the abstract factory interface and abstract product interfaces.
```python
# your_package/core/api_gateway/base/gateway.py

from abc import ABC, abstractmethod

class ApiGateway(ABC):
    
    @abstractmethod
    def add_service(self, name: str, url: str):
        pass

    @abstractmethod
    def add_route(self, service_name: str, paths: list):
        pass
```

#### `your_package/core/api_gateway/factory.py`
Implements the factory method for creating instances of the API gateway.
```python
# your_package/core/api_gateway/factory.py

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
```

#### `your_package/core/logging/base/logger.py`
Defines the abstract factory interface and abstract product interfaces.
```python
# your_package/core/logging/base/logger.py

from abc import ABC, abstractmethod

class Logger(ABC):
    
    @abstractmethod
    def setup(self):
        pass
```

#### `your_package/core/logging/factory.py`
Implements the factory method for creating instances of the logger.
```python
# your_package/core/logging/factory.py

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
```

#### `your_package/core/security/base/security.py`
Defines the abstract factory interface and abstract product interfaces.
```python
# your_package/core/security/base/security.py

from abc import ABC, abstractmethod

class Security(ABC):
    
    @abstractmethod
    def start(self):
        pass
```

#### `your_package/core/security/factory.py`
Implements the factory method for creating instances of the security service.
```python
# your_package/core/security/factory.py

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
```

#### `your_package/core/microservice/base/service.py`
Defines the abstract factory interface and abstract product interfaces.
```python
# your_package/core/microservice/base/service.py

from abc import ABC, abstractmethod
from fastapi import FastAPI

class Microservice(ABC):
    
    @abstractmethod
    def create_app(self) -> FastAPI:
        pass
```

#### `your_package/core/microservice/factory.py`
Implements the factory method for creating instances of the microservice.
```python
# your_package/core/microservice/factory.py

import importlib
from .base.service import Microservice

def create_microservice(service_type: str) -> Microservice:
    module_name = f"implementations.{service_type}_service"
    class_name = f"{service_type.capitalize()}Service"
    
    try:
        module = importlib.import_module(module_name)
        service_class = getattr(module, class_name)
        return service_class()
    except (ImportError, AttributeError) as e:
        raise ValueError(f"Unsupported service type: {service_type}") from e
```

#### `your_package/core/database/base/database.py`
Defines the abstract factory interface and abstract product interfaces.
```python
# your_package/core/database/base/database.py

from abc import ABC, abstractmethod

class Database(ABC):
    
    @abstractmethod
    def get_session(self):
        pass
```

#### `your_package/core/database/factory.py`
Implements the factory method for creating instances of the database.
```python
# your_package/core/database/factory.py

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
```

#### `your_package/core/cache/base/cache.py`
Defines the abstract factory interface and abstract product interfaces.
```python
# your_package/core/cache/base/cache.py

from abc import ABC, abstractmethod

class Cache(ABC):
    
    @abstractmethod
    def get_client(self):
        pass
```

#### `your_package/core/cache/factory.py`
Implements the factory method for creating instances of the cache.
```python
# your_package/core/cache/factory.py

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
```

### Main Application

#### `app.py`
Main application code that uses the components from the core package and reads configuration from the INI file.
```python
# your_project/app.py

import configparser
from core.message_broker import create_message_broker, MessageBroker
from core.api_gateway import create_api_gateway, ApiGateway
from core.logging import create_logger, Logger
from core.security import create_security, Security
from core.microservice import create_microservice, Microservice
from core.database import create_database, Database
from core.cache import create_cache, Cache

# Read configuration from INI file
config = configparser.ConfigParser()
config.read('config/settings.ini')

# Create instances using the factory functions
message_broker: MessageBroker = create_message_broker(config['DEFAULT']['BrokerType'], config['DEFAULT']['BrokerURL'])
api_gateway: ApiGateway = create_api_gateway('kong', config['DEFAULT']['KongAdminURL'])
logger: Logger = create_logger('graylog', config['DEFAULT']['GraylogHost'], config['DEFAULT']['GraylogPort'])
security: Security = create_security('prometheus', int(config['DEFAULT']['PrometheusPort']))
microservice: Microservice = create_microservice('fastapi')
database: Database = create_database('mysql', config['DEFAULT']['DatabaseURL'])
cache: Cache = create_cache('redis', config['DEFAULT']['RedisURL'])

# Setup logger
logger.setup()

# Define a message handler
def handle_message(message: str):
    print(f"Received message: {message}")

# Publish and subscribe to a message
message_broker.publish(topic="my_topic", message="Hello, NSQ!")
message_broker.subscribe(topic="my_topic", handler=handle_message)
message_broker.start()

# Example of adding a service and route to Kong
api_gateway.add_service(name="example-service", url="http://example.com")
api_gateway.add_route(service_name="example-service", paths=["/example"])

# Start security service (Prometheus)
security.start()

# Create FastAPI app
app = microservice.create_app()

# Get database session
db_session = database.get_session()

# Get Redis client
redis_client = cache.get_client()

# Stop the message broker when shutting down
message_broker.stop()
```

### `setup.py`
Setup script for the package.
```python
# your_project/setup.py

from setuptools import setup, find_packages

setup(
    name="your_package",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "httpx",
        "nsq-py",
        "graypy",
        "prometheus_client",
        "pydantic",
        "sqlalchemy",
        "pymysql",
        "redis",
        "requests",
    ],
)
```

### `requirements.txt`
List of dependencies for the project.
```
fastapi
httpx
nsq-py
graypy
prometheus_client
pydantic
sqlalchemy
pymysql


redis
requests
configparser
```

This setup ensures that your package (`your_package`) contains only the abstractions and generic functionalities, while the application-level code (in `your_project`) handles configuration and specific implementations. This approach makes your package highly reusable and decouples the configuration and implementation details from the core package.